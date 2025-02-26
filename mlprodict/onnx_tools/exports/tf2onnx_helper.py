"""
@file
@brief Helpers to run examples created with function
@see fn export2tf2onnx.
"""
import collections
import inspect
import numpy
from onnx.numpy_helper import from_array
from onnx.helper import (
    make_node, make_graph, make_model, set_model_props, make_tensor)
from onnx import AttributeProto
from ..onnx2py_helper import guess_dtype, guess_proto_dtype
from ..onnx_tools import ensure_topological_order


_make_name_id = 0


def make_name(name):
    "Creates a unique name."
    global _make_name_id  # pylint: disable=W0603
    name = "%s_%d" % (name, _make_name_id)
    _make_name_id += 1
    return name


def make_sure(cond, msg, *args):
    "Raises an exception if cond is not verified."
    if not cond:
        raise RuntimeError(msg % tuple(args))


def map_onnx_to_numpy_type(onnx_dtype):
    "Converts ONNX type into numpy type."
    return guess_dtype(onnx_dtype)


class tf_op:
    """
    Decorator to register any new converter.
    :param name: type of the operator to rewrite
    :param domain: domain
    """
    _OPSETS = collections.OrderedDict()

    def __init__(self, name, domain='', **kwargs):
        if not isinstance(name, list):
            name = [name]
        self.names = name
        self.domain = domain
        self.kwargs = kwargs

    def __call__(self, func):
        for ke, va in inspect.getmembers(func, inspect.ismethod):
            if ke.startswith("version_"):
                version = int(ke.replace("version_", ""))
                self._register_handler(
                    va, version, self.names, self.domain, self.kwargs)
        return func

    def _register_handler(self, func, version, names, domain, kwargs):
        opset = tf_op._OPSETS.get(domain)
        if not opset:
            opset = []
            tf_op._OPSETS[domain] = opset
        while version >= len(opset):
            opset.append({})
        opset_dict = opset[version]
        for name in names:
            opset_dict[name] = (func, kwargs)


class Tf2OnnxConvert:
    """
    Applies the converter on an ONNX graph.

    :param onnx_model: ONNX graph
    :param tf_op: class which register
    :param verbose: verbosity
    :param target_opset: targetted opsets
    """

    def __init__(self, onnx_model, _tf_op=None, verbose=None,
                 target_opset=None):
        self._onnx_model = onnx_model
        self._tf_op = _tf_op or tf_op
        self.verbose = verbose
        if isinstance(target_opset, int):
            self.target_opsets = {'': target_opset}
        elif isinstance(target_opset, dict):
            self.target_opsets = target_opset
        elif target_opset is None:
            opsets = {}
            for oimp in onnx_model.opset_import:
                if oimp.domain == '':
                    opsets[oimp.domain] = oimp.version
                    opset = oimp.version
                else:
                    opsets[oimp.domain] = opset
            self.target_opsets = opsets
        else:
            raise ValueError(  # pragma: no cover
                "Unexepected value for target_opset=%r." % target_opset)
        self._names = {}
        for node in onnx_model.graph.node:
            self._names[node.name] = node
        for init in onnx_model.graph.initializer:
            self._names[init.name] = init
        # _forbidden_new_names contains current names and deleted names.
        self._forbidden_new_names = set(self._names)
        if '' in self.target_opsets:
            self.opset = self.target_opsets['']
        if not hasattr(self, 'opset'):
            raise RuntimeError(  # pragma: no cover
                "Attribute opset is missing, target_opset=%r." % target_opset)

    def get_node_by_name(self, name):
        """
        Retrieves a node by its name.

        :param name: node name
        :return: node name
        """
        if name not in self._names:
            raise RuntimeError(
                "Unable to find node name %r among %r." % (
                    name, ", ".join(sorted(self._names))))
        return self._names[name]

    def _add_node_name(self, obj):
        """
        Registers an object in in the graph by its name.
        :param name: node or initializer
        """
        if obj.name in self._forbidden_new_names:
            raise RuntimeError(
                "Name %r is already registered." % obj.name)
        self._names[obj.name] = obj
        self._forbidden_new_names.add(obj.name)

    def make_node(self, op_type, inputs, attr=None, outputs=None,
                  name=None, domain='', output_count=1):
        """
        Adds a node to the list of nodes.

        :param op_type: operator type
        :param inputs: list of strings
        :param attr: dictionary of attributes
        :param outputs: None or list of strings
        :param output_count: used if outputs is None to guess
            the number of outputs of this node
        :param name: name of the node
        :param domain: domain
        :return: created node
        """
        if self.verbose:
            print("[Tf2OnnxConvert.make_node] op_type=%r inputs=%r" % (
                op_type, inputs))

        if attr is None:
            attr = {}
        if name is None:
            name = make_name(op_type)
        if name in self._names:
            raise RuntimeError(
                "Node name %r already exists in %r." % (
                    name, ", ".join(sorted(self._names))))

        if outputs is None:
            outputs = [(name + ":" + str(i)) for i in range(output_count)]

        output_count = len(outputs)
        raw_attr = {}
        onnx_attrs = []
        for a, v in attr.items():
            if isinstance(v, AttributeProto):
                onnx_attrs.append(v)
            else:
                raw_attr[a] = v

        onnx_node = make_node(
            op_type, inputs, outputs, name=name, domain=domain, **raw_attr)

        self._add_node_name(onnx_node)
        return onnx_node

    def make_const(self, name, np_val, skip_conversion=False, raw=True):
        """
        Make a new constants in the graph.
        :param name: const node name, must be unique.
        :param np_val: value of type numpy ndarray.
        :param skip_conversion:
            bool, indicate whether this created node would be mapped
            during conversion
        :param raw: whether to store data at field of raw_data or the
            specific field according to its dtype
        :return: create initializer
        """
        if name in self._names:
            raise RuntimeError(
                "Initializer name %r already exists in %r." % (
                    name, ", ".join(sorted(self._names))))
        np_val_flat = np_val.flatten()
        is_bytes = (np_val.dtype == numpy.object and len(np_val_flat) > 0 and
                    isinstance(np_val_flat[0], bytes))
        if raw and not is_bytes:
            onnx_tensor = from_array(np_val, name)
        else:
            onnx_tensor = make_tensor(
                name, guess_proto_dtype(np_val.dtype),
                np_val.shape, np_val_flat, raw=False)

        self._add_node_name(onnx_tensor)
        return onnx_tensor

    def get_dtype(self, input_name):
        """
        Returns the type of one node or None if unknown.
        :param input_name: result name
        :return: numpy dtype
        """
        inputs = self._onnx_model.graph.input
        names = [_.name for _ in inputs]
        if input_name not in names:
            return None  # pragma: no cover
        ind = names.index(input_name)
        return inputs[ind].type.tensor_type.elem_type

    def replace_all_inputs(self, old_name, new_name):
        """
        Every taking *old_name* as inputs will take *new_name* instead.
        Looks in the output as well but in that case, it creates an identity
        node to avoid changing an output name.
        :param old_name: name to replace
        :param new_name: new name
        :return: list of impacted nodes
        """
        res = []
        for node in self._names.values():
            if not hasattr(node, 'input'):
                continue
            if old_name not in node.input:
                continue
            new_inputs = [new_name if i.name == old_name else i.name
                          for i in node.input]
            node.input[:] = new_inputs[:]
            res.append(node)
            if self.verbose:
                print("[Tf2OnnxConvert.replace_all_inputs] replace %r by %r in node %r" % (
                    old_name, new_name, node.name))
        for o in self._onnx_model.graph.output:
            if o.name != old_name:
                continue
            n = self.make_node("Identity", [new_name], outputs=[old_name],
                               name=make_name("IdOutputReplaced"))
            res.append(n)
            if self.verbose:
                print("[Tf2OnnxConvert.replace_all_inputs] add id node from %r to %r "
                      "with node %r." % (
                          old_name, new_name, n.name))  # pylint: disable=E1101
        return res

    def remove_node(self, name):
        """
        Removes a node name from the list.
        """
        if name not in self._names:
            raise RuntimeError(
                "Unable to delete name %r because it does not exists." % name)
        del self._names[name]
        if self.verbose:
            print("[Tf2OnnxConvert.remove_node] delete name %r" % name)

    def get_shape(self, input_name):
        """
        Returns the type of one node or None if unknown.
        :param input_name: result name
        :return: numpy dtype
        """
        inputs = self._onnx_model.graph.input
        names = [_.name for _ in inputs]
        if input_name not in names:
            return None  # pragma: no cover
        ind = names.index(input_name)
        dims = inputs[ind].type.tensor_type.shape.dim
        return tuple(dims)

    def run(self):
        """
        Calls the registered converters on the graph
        held by this instance. Returns the new onnx graph.

        :return: ONNX graph
        """
        if len(self._tf_op._OPSETS) == 0:
            raise RuntimeError(  # pragma: no cover
                "No converter was registered.")
        if self.verbose:
            print("[Tf2OnnxConvert.run]")

        done = {}
        modif = 1
        while modif > 0:
            modif = 0
            # The converter may alter the current list of nodes, we freeze it.
            current_values = list(self._names.values())
            for node in current_values:
                if not hasattr(node, 'domain'):
                    # initializer
                    continue
                if done.get(node.name, False):
                    continue
                domain = node.domain
                if domain not in self._tf_op._OPSETS:
                    continue

                # look for a converter
                rews = self._tf_op._OPSETS[domain]
                target = min(self.target_opsets[domain], len(rews))
                conv = None
                for i in range(len(rews) - 1, -1, -1):
                    if node.op_type in rews[i]:
                        conv = rews[i][node.op_type]
                        break
                if conv is None:
                    continue

                # applies the converter
                if self.verbose:
                    print("[Tf2OnnxConvert.run] convert node type=%r opset=%r name=%r"
                          "" % (node.op_type, target, node.name))
                fct, kwargs = conv
                fct(self, node, target_opset=target, **kwargs)
                modif += 1

        return self.make_model()

    def make_model(self):
        """
        Produces the new ONNX graph with the updated sets of nodes.
        """
        inputs = self._onnx_model.graph.input
        outputs = self._onnx_model.graph.output
        inits = [init[1] for init in sorted(self._names.items())
                 if not hasattr(init[1], 'domain')]
        nodes = [node[1] for node in sorted(self._names.items())
                 if hasattr(node[1], 'domain')]
        nodes = ensure_topological_order(inputs, inits, nodes)

        if self.verbose:
            print(
                "[Tf2OnnxConvert.make_node] %d nodes %d inputs %d "
                "outputs %d initializers"
                "" % (len(nodes), len(inputs), len(outputs), len(inits)))
        graph = make_graph(nodes, self._onnx_model.graph.name,
                           inputs, outputs, inits)
        onnx_model = make_model(graph)
        onnx_model.ir_version = self._onnx_model.ir_version
        onnx_model.producer_name = self._onnx_model.producer_name + "-mlprodict"
        onnx_model.producer_version = self._onnx_model.producer_version
        onnx_model.domain = self._onnx_model.domain
        onnx_model.model_version = self._onnx_model.model_version
        onnx_model.doc_string = self._onnx_model.doc_string
        metadata = {p.key: p.value for p in self._onnx_model.metadata_props}
        set_model_props(onnx_model, metadata)

        # opsets
        del onnx_model.opset_import[:]  # pylint: disable=E1101
        for dom, value in self.target_opsets.items():
            op_set = onnx_model.opset_import.add()  # pylint: disable=E1101
            op_set.domain = dom
            op_set.version = value
        return onnx_model


class GraphBuilder:
    """
    Helpers to build graph.
    :param graph!
    """

    def __init__(self, graph):
        self._g = graph

    @property
    def graph(self):
        "Returns the graph."
        return self._g

    def make_slice(self, kwargs, name=None, shapes=None, dtypes=None, return_node=False):
        """
        slice changes its schema at opset 10: it treats some attributes as dynamic input
        so this function has to process inputs according to graph's opset version
        to get "inputs" and "attr" to feed "make_node"
        kwargs: key could be ["data", "starts", "ends", "axes", "steps", "outputs"].
        """
        outputs = kwargs.pop("outputs", None)

        if self.graph.opset < 10:
            # "data" is string
            # "starts", "ends" and "axes" are attributes, and "axes" is optional.
            data = kwargs.pop("data")
            starts = self._convert_to_attribute(kwargs.pop("starts"))
            ends = self._convert_to_attribute(kwargs.pop("ends"))
            axes = self._convert_to_attribute(
                kwargs.pop("axes", None), is_optional=True)
            attr = {"starts": starts, "ends": ends, "axes": axes}
            inputs = [data]
        else:
            # slice-10 has 3 required inputs "data", "starts", "ends"l
            # and 2 optional inputs "axes", "steps"
            # input sequence should be "data", "starts", "ends", "axes", "steps"
            attr = {}
            data = kwargs.pop("data")
            starts = self._convert_to_input(kwargs.pop(
                "starts"), "const_starts", dtype=numpy.int64)
            ends = self._convert_to_input(kwargs.pop(
                "ends"), "const_ends", dtype=numpy.int64)
            axes = self._convert_to_input(kwargs.pop(
                "axes", None), "const_axes", is_optional=True, dtype=numpy.int64)
            steps = self._convert_to_input(kwargs.pop(
                "steps", None), "const_steps", is_optional=True, dtype=numpy.int64)
            inputs = [data, starts.name, ends.name, axes.name, steps.name]

        # pro-process inputs and attr
        make_sure(not kwargs, "kwargs contains un-used key")

        new_attr = {}
        for key, val in attr.items():
            if val is not None:
                new_attr[key] = val
        attr = new_attr

        for ind, val in enumerate(inputs):
            if val is None:
                inputs[ind] = ""  # empty string means no connection in ONNX
        # remove tailing ""
        while inputs[-1] == "":
            inputs = inputs[:-1]

        if self.graph.opset >= 10:
            dtype = self.graph.get_dtype(inputs[1])
            for input_data in inputs[1:]:
                if input_data != "":
                    make_sure(dtype == self.graph.get_dtype(
                        input_data), "dtype should be same")

        node = self.graph.make_node(op_type="Slice", inputs=inputs, attr=attr, name=name,
                                    outputs=outputs, shapes=shapes, dtypes=dtypes)
        if return_node:
            return node
        raise NotImplementedError("return_node must be True")

    def make_squeeze(self, kwargs, name=None, shapes=None, dtypes=None, return_node=False, op_name_scope=None):
        """
        Squeeze changes its schema at opset 13: it treats axes as a dynamic input
        kwargs: key could be ["data", "axes"].
        """
        outputs = kwargs.pop("outputs", None)

        if self.graph.opset < 13:
            data = kwargs.pop("data")
            axes = self._convert_to_attribute(
                kwargs.pop("axes", None), is_optional=True)
            attr = {"axes": axes}
            inputs = [data]
        else:
            data = kwargs.pop("data")
            axes = self._convert_to_input(kwargs.pop(
                "axes", None), "const_axes", is_optional=True, dtype=numpy.int64)
            attr = {}
            inputs = [data, axes.name]

        make_sure(not kwargs, "kwargs contains un-used key")

        new_attr = {}
        for key, val in attr.items():
            if val is not None:
                new_attr[key] = val
        attr = new_attr

        for ind, val in enumerate(inputs):
            if val is None:
                inputs[ind] = ""  # empty string means no connection in ONNX
        # remove tailing ""
        while inputs[-1] == "":
            inputs = inputs[:-1]

        node = self.graph.make_node(op_type="Squeeze", inputs=inputs, attr=attr, name=name,
                                    outputs=outputs)
        if return_node:
            return node
        raise NotImplementedError("return_node must be True")

    def make_unsqueeze(self, kwargs, name=None, shapes=None, dtypes=None, return_node=False, op_name_scope=None):
        """
        Unsqueeze changes its schema at opset 13: it treats axes as a dynamic input
        kwargs: key could be ["data", "axes"].
        """
        outputs = kwargs.pop("outputs", None)

        if self.graph.opset < 13:
            data = kwargs.pop("data")
            axes = self._convert_to_attribute(
                kwargs.pop("axes", None), is_optional=True)
            attr = {"axes": axes}
            inputs = [data]
        else:
            data = kwargs.pop("data")
            axes = self._convert_to_input(kwargs.pop(
                "axes", None), "const_axes", is_optional=True, dtype=numpy.int64)
            attr = {}
            inputs = [data, axes.name]

        make_sure(not kwargs, "kwargs contains un-used key")

        new_attr = {}
        for key, val in attr.items():
            if val is not None:
                new_attr[key] = val
        attr = new_attr

        for ind, val in enumerate(inputs):
            if val is None:
                inputs[ind] = ""  # empty string means no connection in ONNX
        # remove tailing ""
        while inputs[-1] == "":
            inputs = inputs[:-1]

        node = self.graph.make_node(op_type="Unsqueeze", inputs=inputs, attr=attr, name=name,
                                    outputs=outputs)
        if return_node:
            return node
        raise NotImplementedError("return_node must be True")

    def _convert_to_input(self, tensor, const_name, is_optional=False, dtype=None):
        """in ONNX, input shold come from node, so it must be a string"""
        if is_optional and tensor is None:
            return None

        make_sure(tensor is not None,
                  "input is required so it couldn't be None")

        res = tensor
        if isinstance(tensor, list):
            res = self.graph.make_const(
                make_name(const_name), numpy.array(tensor, dtype))
        return res

    def _convert_to_attribute(self, tensor, is_optional=False):
        if is_optional and tensor is None:
            return None

        make_sure(tensor is not None,
                  "input is required so it couldn't be None")

        res = tensor
        if isinstance(tensor, str):
            const_node = self.graph.get_node_by_output(tensor)
            res = const_node.get_tensor_value(as_list=True)

        make_sure(isinstance(res, list),
                  "input is an attr, so a list is needed")

        return res
