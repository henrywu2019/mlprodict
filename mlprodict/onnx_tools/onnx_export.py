"""
@file
@brief Exports an ONNX graph in a way it can we created again
with a python script. It relies on :epkg:`jinja2` and :epkg:`autopep8`.

.. versionadded:: 0.7
"""
from textwrap import dedent
import numpy
from jinja2 import Template
import autopep8
import onnx
from onnx import numpy_helper
from .onnx2py_helper import _var_as_dict


_onnx_templates = dedent("""
    import numpy
    from onnx import numpy_helper
    from onnx.helper import (
        make_model, make_node, set_model_props, make_tensor, make_graph,
        make_tensor_value_info)


    def create_model():
        '''
        Converted ``{{ name }}``.

        * producer: {{ producer_name }}
        * version: {{ model_version }}
        * description: {{ doc_string }}
        {%- for key, val in sorted(metadata.items()): -%}
        * {{ key }}: {{ val }}
        {%- endfor %}
        '''
        # containers
        print('[containers]')   # verbose
        initializers = []
        nodes = []
        inputs = []
        outputs = []

        # opsets
        print('[opsets]')   # verbose
        opsets = {{ opsets }}
        target_opset = {{ target_opset }}

        # initializers
        print('[initializers]')   # verbose
        {% for name, value in initializers: %}
        {% if len(value.shape) == 0: %}
        value = numpy.array({{ value }}, dtype=numpy.{{ value.dtype }})
        {% else %}
        list_value = {{ value.ravel().tolist() }}
        value = numpy.array(list_value, dtype=numpy.{{ value.dtype }}){% if len(value.shape) > 1: %}.reshape({{ value.shape }}){% endif %}
        {% endif %}
        tensor = numpy_helper.from_array(value, name='{{ name }}')
        initializers.append(tensor)
        {% endfor %}

        # inputs
        print('[inputs]')   # verbose
        {% for name, type, shape in inputs: %}
        value = make_tensor_value_info('{{ name }}', {{ type }}, {{ shape }})
        inputs.append(value)
        {% endfor %}

        # outputs
        print('[outputs]')   # verbose
        {% for name, type, shape in outputs: %}
        value = make_tensor_value_info('{{ name }}', {{ type }}, {{ shape }})
        outputs.append(value)
        {% endfor %}

        # nodes
        print('[nodes]')   # verbose
        {% for node in nodes: %}
        node = make_node(
            '{{ node['op_type'] }}',
            {{ node['inputs'] }},
            {{ node['outputs'] }},
            {% if node['name']: %}name='{{ node['name'] }}',{% endif %}
            {%- for name, value in node['attributes']: -%}
            {{ name }}={{ value }},
            {%- endfor -%}
            domain='{{ node['domain'] }}')
        nodes.append(node)
        {% endfor %}

        # graph
        print('[graph]')   # verbose
        graph = make_graph(nodes, '{{ name }}', inputs, outputs, initializers)
        onnx_model = make_model(graph)
        onnx_model.ir_version = {{ ir_version }}
        onnx_model.producer_name = '{{ producer_name }}'
        onnx_model.producer_version = '{{ producer_version }}'
        onnx_model.domain = '{{ domain }}'
        onnx_model.model_version = {{ model_version }}
        onnx_model.doc_string = '{{ doc_string }}'
        set_model_props(onnx_model, {{ metadata }})

        # opsets
        print('[opset]')   # verbose
        del onnx_model.opset_import[:]  # pylint: disable=E1101
        for dom, value in opsets.items():
            op_set = onnx_model.opset_import.add()
            op_set.domain = dom
            op_set.version = value

        return onnx_model


    onnx_model = create_model()
""")


_tf2onnx_templates = dedent("""
    import inspect
    import collections
    import numpy
    from onnx import AttributeProto
    from onnx.helper import (
        make_model, make_node, set_model_props, make_tensor, make_graph,
        make_tensor_value_info)
    # from utils import make_name, make_sure
    from mlprodict.onnx_tools.exports.tf2onnx_helper import (
        make_name, make_sure)
    # from tf2onnx.handler import tf_op
    from mlprodict.onnx_tools.exports.tf2onnx_helper import tf_op
    from mlprodict.onnx_tools.exports.tf2onnx_helper import Tf2OnnxConvert


    @tf_op("{{ name }}")
    class Convert{{ name }}Op:

        supported_dtypes = [
            numpy.float32,
        ]

        @classmethod
        def any_version(cls, opset, ctx, node, **kwargs):
            '''
            Converter for ``{{ name }}``.

            * producer: {{ producer_name }}
            * version: {{ model_version }}
            * description: {{ doc_string }}
            {%- for key, val in sorted(metadata.items()): -%}
            * {{ key }}: {{ val }}
            {%- endfor %}
            '''
            oldnode = node
            input_name = node.input[0]
            onnx_dtype = ctx.get_dtype(input_name)
            make_sure(onnx_dtype in Convert{{ name }}Op.supported_dtypes, "Unsupported input type.")
            shape = ctx.get_shape(input_name)
            varx = {x: x for x in node.input}

            # initializers
            if getattr(ctx, 'verbose', False):
                print('[initializers] %r' % cls)
            {% for name, value in initializers: %}
            {% if len(value.shape) == 0: %}
            value = numpy.array({{ value }}, dtype=numpy.{{ value.dtype }})
            {% else %}
            list_value = {{ value.ravel().tolist() }}
            value = numpy.array(list_value, dtype=numpy.{{ value.dtype }}){% if len(value.shape) > 1: %}.reshape({{ value.shape }}){% endif %}
            {% endif %}
            r_{{ name }} = ctx.make_const(name=make_name('init_{{ name }}'), np_val=value)
            varx['{{ name }}'] = r_{{ name }}.name
            {% endfor %}

            # nodes
            if getattr(ctx, 'verbose', False):
                print('[nodes] %r' % cls)
            {% for node in nodes: %}
            attr = dict(
                {%- for name, value in node['attributes']: -%}
                {{ name }}={{ value }},
                {%- endfor -%})
            inputs = [{% for name in node['inputs']: -%}varx['{{ name }}'], {%- endfor %}]
            node = ctx.make_node(
                '{{ node['op_type'] }}', inputs=inputs, attr=attr,{% if node['domain']: -%} domain='{{ node['domain'] }}', {% endif %}
                name=make_name('{{ node['name'] }}'))
            {% for i, name in enumerate(node['outputs']): -%}
            varx['{{ name }}'] = node.output[{{ i }}]
            {%- endfor %}
            {% endfor %}

            # finalize
            if getattr(ctx, 'verbose', False):
                print('[replace_all_inputs] %r' % cls)
            ctx.replace_all_inputs(oldnode.output[0], node.output[0])
            ctx.remove_node(oldnode.name)

        @classmethod
        def version_13(cls, ctx, node, **kwargs):
            return cls.any_version(13, ctx, node, **kwargs)


    def create_model():
        inputs = []
        outputs = []

        # inputs
        print('[inputs]')   # verbose
        {% for name, type, shape in inputs: %}
        value = make_tensor_value_info('{{ name }}', {{ type }}, {{ shape }})
        inputs.append(value)
        {% endfor %}

        # outputs
        print('[outputs]')   # verbose
        {% for name, type, shape in outputs: %}
        value = make_tensor_value_info('{{ name }}', {{ type }}, {{ shape }})
        outputs.append(value)
        {% endfor %}

        inames = [i.name for i in inputs]
        onames = [i.name for i in outputs]
        node = make_node('{{ name }}', inames, onames, name='{{ name }}')

        # graph
        print('[graph]')   # verbose
        graph = make_graph([node], '{{ name }}', inputs, outputs)
        onnx_model = make_model(graph)
        onnx_model.ir_version = {{ ir_version }}
        onnx_model.producer_name = '{{ producer_name }}'
        onnx_model.producer_version = '{{ producer_version }}'
        onnx_model.domain = '{{ domain }}'
        onnx_model.model_version = {{ model_version }}
        onnx_model.doc_string = '{{ doc_string }}'
        set_model_props(onnx_model, {{ metadata }})

        # opsets
        print('[opset]')   # verbose
        opsets = {{ opsets }}
        del onnx_model.opset_import[:]  # pylint: disable=E1101
        for dom, value in opsets.items():
            op_set = onnx_model.opset_import.add()
            op_set.domain = dom
            op_set.version = value

        return onnx_model


    onnx_raw = create_model()
    onnx_model = Tf2OnnxConvert(onnx_raw, tf_op).run()
""")


_numpy_templates = dedent("""
    import numpy
    from mlprodict.onnx_tools.exports.numpy_helper import make_slice


    def numpy_{{name}}({{ inputs[0][0] }}{% for i in inputs[1:]: %}, {{ i[0] }}{% endfor %}):
        '''
        Numpy function for ``{{ name }}``.

        * producer: {{ producer_name }}
        * version: {{ model_version }}
        * description: {{ doc_string }}
        {%- for key, val in sorted(metadata.items()): -%}
        * {{ key }}: {{ val }}
        {%- endfor %}
        '''
        # initializers
        {% for name, value in initializers: %}
        {% if len(value.shape) == 0: %}
        {{ name }} = numpy.array({{ value }}, dtype=numpy.{{ value.dtype }})
        {% else %}
        list_value = {{ value.ravel().tolist() }}
        {{ name }} = numpy.array(list_value, dtype=numpy.{{ value.dtype }}){% if len(value.shape) > 1: %}.reshape({{ value.shape }}){% endif %}
        {% endif %}
        {% endfor %}

        # nodes
        {% for node in nodes: %}
        {{ make_numpy_code(target_opset, **node) }}{% endfor %}

        return {{ outputs[0][0] }}{% for o in outputs[1:]: %}, {{ o[0] }}{% endfor %}
""")


def make_numpy_code(opset, name=None, op_type=None, domain='',
                    inputs=None, outputs=None, attributes=None):
    """
    Converts an ONNX operators into :epkg:`numpy` code.

    :param name: node name
    :param op_type: operator type
    :param domain: domain
    :param inputs: inputs
    :param outputs: outputs
    :param attributes: attributes:
    :return: code as str
    """
    def make_sure_inputs(n):
        if len(inputs) != n:
            raise RuntimeError(  # pragma: no cover
                "Expecting %d inputs for operator %r not %r." % (
                    n, op_type, inputs))

    def make_sure_opsets(mi, ma=None):
        if mi is not None and opset < mi:
            raise RuntimeError(  # pragma: no cover
                "Cannot convert operator type %d, opset %d < %d." % (
                    op_type, opset, mi))
        if ma is not None and opset > ma:
            raise RuntimeError(  # pragma: no cover
                "Cannot convert operator type %d, opset %d > %d." % (
                    op_type, opset, mi))

    def getat(name, defval=None):
        for n, val in attributes:
            if name == n:
                return val
        return defval

    if domain != '':
        raise NotImplementedError(
            "Unable to convert any operator from domain %r." % domain)

    binary_ops = dict(Add='+', Sub='-', Div='/', Mul='*', MatMul='@',
                      Pow='**')
    unary_ops = dict(Neg='-')

    outs = ", ".join(outputs)

    if op_type in binary_ops:
        make_sure_inputs(2)
        return "%s = %s %s %s" % (outs, inputs[0], binary_ops[op_type], inputs[1])

    if op_type in unary_ops:
        make_sure_inputs(1)
        return "%s = %s %s" % (outs, unary_ops[op_type], inputs[0])

    if op_type == 'Concat':
        axis = getat('axis', 0)
        return "%s = numpy.concatenate([%s], %s)" % (outs, ", ".join(inputs), axis)

    if op_type == 'Gather':
        make_sure_opsets(11)
        make_sure_inputs(2)
        axis = getat('axis', 0)
        return "%s = numpy.take(%s, %s, axis=%s)" % (outs, inputs[0], inputs[1], axis)

    if op_type == 'Reshape':
        make_sure_inputs(2)
        return "%s = %s.reshape(tuple(%s))" % (outs, inputs[0], inputs[1])

    if op_type == 'Shape':
        make_sure_inputs(1)
        return "%s = numpy.array(%s.shape, dtype=numpy.int64)" % (outs, inputs[0])

    if op_type == 'Slice':
        return "%s = make_slice(%s)" % (outs, ", ".join(inputs))

    if op_type == 'Transpose':
        make_sure_inputs(1)
        perm = getat('perm', None)
        return "%s = numpy.transpose(%s, axes=tuple(%s))" % (outs, inputs[0], perm)

    if op_type == 'Unsqueeze':
        make_sure_opsets(13)
        make_sure_inputs(2)
        return "%s = numpy.expand_dims(%s, axis=tuple(%s))" % ((outs, ) + tuple(inputs))

    raise NotImplementedError(
        "Unable to convert operator type %r name=%r." % (op_type, name))


def export_template(model_onnx, templates, opset=None, verbose=True, name=None):
    """
    Exports an ONNX model to the onnx syntax.

    :param model_onnx: string or ONNX graph
    :param templates: exporting templates
    :param opset: opset to export to
        (None to select the one from the graph)
    :param verbose: insert prints
    :param name: to overwrite onnx name
    :return: python code
    """
    # containers
    context = {}

    # opset
    opsets = {}
    for oimp in model_onnx.opset_import:
        if oimp.domain == '' and opset is None:
            opsets[oimp.domain] = oimp.version
            opset = oimp.version
        else:
            opsets[oimp.domain] = opset
    context['opsets'] = opsets
    context['target_opset'] = opset

    # inits
    initializers = []
    for init in model_onnx.graph.initializer:
        value = numpy_helper.to_array(init)
        initializers.append((init.name, value))
    context['initializers'] = initializers

    # inputs
    inputs = []
    for inp in model_onnx.graph.input:
        t = inp.type.tensor_type
        dims = tuple(t.shape.dim)
        inputs.append((inp.name, t.elem_type, dims))
    context['inputs'] = inputs

    # outputs
    outputs = []
    for inp in model_onnx.graph.output:
        t = inp.type.tensor_type
        dims = tuple(t.shape.dim)
        outputs.append((inp.name, t.elem_type, dims))
    context['outputs'] = outputs

    # node
    nodes = []
    for node in model_onnx.graph.node:
        attributes = []
        for at in node.attribute:
            temp = _var_as_dict(at)
            value = temp['value']
            if isinstance(value, str):
                attributes.append((at.name, "%r" % value))
            else:
                if isinstance(value, numpy.ndarray):
                    attributes.append((at.name, repr(value.tolist())))
                else:
                    attributes.append((at.name, repr(value)))
        d = dict(name=node.name, op_type=node.op_type,
                 domain=node.domain, inputs=node.input,
                 outputs=node.output, attributes=attributes)
        nodes.append(d)
    context['nodes'] = nodes

    # graph
    context['name'] = name or model_onnx.graph.name
    context['ir_version'] = model_onnx.ir_version
    context['producer_name'] = model_onnx.producer_name
    context['domain'] = model_onnx.domain
    context['model_version'] = model_onnx.model_version
    context['doc_string'] = model_onnx.doc_string
    context['metadata'] = {p.key: p.value for p in model_onnx.metadata_props}

    # final
    template = Template(templates)
    final = template.render(
        enumerate=enumerate, sorted=sorted, len=len,
        make_numpy_code=make_numpy_code, **context)

    if not verbose:
        rows = final.split("\n")
        final = "\n".join(_ for _ in rows if not _.endswith("#  verbose"))
    return autopep8.fix_code(final)


def export2onnx(model_onnx, opset=None, verbose=True, name=None):
    """
    Exports an ONNX model to the :epkg:`onnx` syntax.

    :param model_onnx: string or ONNX graph
    :param opset: opset to export to
        (None to select the one from the graph)
    :param verbose: inserts prints
    :param name: to overwrite onnx name
    :return: python code

    The following example shows what a python code creating a graph
    implementing the KMeans would look like.

    .. runpython::
        :showcode:

        import numpy
        from sklearn.cluster import KMeans
        from skl2onnx import to_onnx
        from mlprodict.onnx_tools.onnx_export import export2onnx

        X = numpy.arange(20).reshape(10, 2).astype(numpy.float32)
        tr = KMeans(n_clusters=2)
        tr.fit(X)

        onx = to_onnx(tr, X, target_opset=14)
        code = export2onnx(onx)

        print(code)
    """
    if isinstance(model_onnx, str):
        model_onnx = onnx.load(model_onnx)

    return export_template(model_onnx, templates=_onnx_templates,
                           opset=opset, verbose=verbose, name=name)


def export2tf2onnx(model_onnx, opset=None, verbose=True, name=None):
    """
    Exports an ONNX model to the :epkg:`tensorflow-onnx` syntax.

    :param model_onnx: string or ONNX graph
    :param opset: opset to export to
        (None to select the one from the graph)
    :param verbose: inserts prints
    :param name: to overwrite onnx name
    :return: python code

    .. runpython::
        :showcode:

        import numpy
        from sklearn.cluster import KMeans
        from skl2onnx import to_onnx
        from mlprodict.onnx_tools.onnx_export import export2tf2onnx

        X = numpy.arange(20).reshape(10, 2).astype(numpy.float32)
        tr = KMeans(n_clusters=2)
        tr.fit(X)

        onx = to_onnx(tr, X, target_opset=14)
        code = export2tf2onnx(onx)

        print(code)
    """
    if isinstance(model_onnx, str):
        model_onnx = onnx.load(model_onnx)

    return export_template(model_onnx, templates=_tf2onnx_templates,
                           opset=opset, verbose=verbose, name=name)


def export2numpy(model_onnx, opset=None, verbose=True, name=None):
    """
    Exports an ONNX model to the :epkg:`numpy` syntax.
    The exports does not work with all operators.

    :param model_onnx: string or ONNX graph
    :param opset: opset to export to
        (None to select the one from the graph)
    :param verbose: inserts prints
    :param name: to overwrite onnx name
    :return: python code

    .. runpython::
        :showcode:

        import numpy
        from sklearn.cluster import KMeans
        from skl2onnx import to_onnx
        from mlprodict.onnx_tools.onnx_export import export2numpy

        X = numpy.arange(20).reshape(10, 2).astype(numpy.float32)
        tr = KMeans(n_clusters=2)
        tr.fit(X)

        onx = to_onnx(tr, X, target_opset=14)
        code = export2numpy(onx)

        print(code)
    """
    if isinstance(model_onnx, str):
        model_onnx = onnx.load(model_onnx)

    return export_template(model_onnx, templates=_numpy_templates,
                           opset=opset, verbose=verbose, name=name)
