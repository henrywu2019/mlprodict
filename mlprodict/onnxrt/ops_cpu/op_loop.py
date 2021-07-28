# -*- encoding: utf-8 -*-
# pylint: disable=E0203,E1101,C0111
"""
@file
@brief Runtime operator.

.. versionadded:: 0.7
"""
import numpy
from ._op import OpRun
from ..shape_object import ShapeObject


class Loop(OpRun):

    atts = {
        'body': None,
    }

    def __init__(self, onnx_node, desc=None, **options):
        OpRun.__init__(self, onnx_node, desc=desc,
                       expected_attributes=Loop.atts,
                       **options)
        if not hasattr(self.body, 'run'):
            raise RuntimeError(  # pragma: no cover
                "Parameter 'body' must have a method 'run', "
                "type {}.".format(type(self.body)))

        self._run_meth = (self.body.run_in_scan
                          if hasattr(self.body, 'run_in_scan')
                          else self.body.run)

    def _run(self, M, cond, v_initial, *args, callback=None):  # pylint: disable=W0221
        inputs = {name: None for name in self.body.input_names}
        inputs[self.body.input_names[2]] = v_initial
        cond_name = self.body.output_names[1]
        if len(args) > 0:
            begin = len(self.body.input_names) - len(args)
            for name, val in zip(self.body.input_names[begin:], args):
                inputs[name] = val
        it = 0
        while cond and it < M:
            inputs[self.body.input_names[0]] = numpy.array(it, dtype=M.dtype)
            inputs[self.body.input_names[1]] = cond
            outputs = self._run_meth(inputs)
            cond = outputs[cond_name]
            for i, o in zip(self.body.input_names[2:],
                            self.body.output_names[1:]):
                inputs[i] = outputs[o]
            if callback is not None:
                callback(inputs)
            it += 1
        if it == 0:
            outputs = {self.body.output_names[1]: cond}
            for i, o in zip(self.body.input_names[2:],
                            self.body.output_names[1:]):
                outputs[o] = inputs[i]
        for o in self.body.output_names:
            if o not in outputs:
                outputs[o] = numpy.empty(shape=tuple())
        return tuple([outputs[name] for name in self.body.output_names[1:]])

    def _infer_shapes(self, M, cond, v_initial, *args):  # pylint: disable=W0221
        res = self.body._set_shape_inference_runtime()
        outputs = {k[0]: k[1:] for k in self.body.output_names_shapes_types}
        
        ret = []
        for name in self.body.output_names[1:]:
            if name in res:
                ret.append(res[name])
            else:
                find = outputs[name]
                ret.append(ShapeObject(find[0], dtype=find[1]))
        return tuple(ret)

    def _infer_types(self, M, cond, v_initial, *args):  # pylint: disable=W0221
        res = self.body._set_type_inference_runtime()
        return tuple([res[name] for name in self.body.output_names[1:]])

    def _infer_sizes(self, M, cond, v_initial, *args):  # pylint: disable=W0221
        store = []

        def callback_(inputs):
            res = self.body.infer_sizes(inputs)
            store.append(res)

        res = self._run(M, cond, v_initial, *args, callback=callback_)
        temp = 0
        for v in store:
            for vv in v.values():
                temp += sum(vv.values())
        return (dict(temp=temp), ) + res
