"""
@brief      test log(time=5s)
"""
import os
import unittest
import collections
import inspect
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import numpy
from onnx import numpy_helper, helper
from onnx.helper import (
    make_model, make_node, set_model_props, make_tensor, make_graph,
    make_tensor_value_info)
from pyquickhelper.pycode import ExtTestCase
from mlprodict.onnx_tools.onnx_export import export2onnx, export2tf2onnx
from mlprodict.testing.verify_code import verify_code
from mlprodict.onnxrt import OnnxInference
from mlprodict.onnx_tools.exports.tf2onnx_helper import make_sure, make_name
from mlprodict.tools.code_helper import print_code


class ConvertFFT2DOp:

    supported_dtypes = [
        numpy.float32,
    ]

    @classmethod
    def any_version(cls, opset, ctx, node, **kwargs):  # pylint: disable=R0915
        '''
        Converter for ``FFT2D``.

        * producer: skl2onnx
        * version: 0
        * description:
        '''
        oldnode = node
        input_name = node.input[0]
        onnx_dtype = ctx.get_dtype(input_name)
        make_sure(onnx_dtype in ConvertFFT2DOp.supported_dtypes,
                  "Unsupported input type.")
        vars = {x: x for x in node.input}  # pylint: disable=W0622

        # initializers
        if getattr(ctx, 'verbose', False):
            print('[initializers] %r' % cls)

        list_value = [1.0, 0.0]
        value = numpy.array(list_value, dtype=numpy.float32).reshape((2, 1, 1))

        r_Un_Unsqueezecst = ctx.make_const(
            name=make_name('init_Un_Unsqueezecst'), np_val=value)
        vars['Un_Unsqueezecst'] = r_Un_Unsqueezecst.name

        list_value = [0]
        value = numpy.array(list_value, dtype=numpy.int64)

        r_Un_Unsqueezecst1 = ctx.make_const(
            name=make_name('init_Un_Unsqueezecst1'), np_val=value)
        vars['Un_Unsqueezecst1'] = r_Un_Unsqueezecst1.name

        list_value = [1.0, 1.0, 1.0, 1.0, 1.0, 6.123234262925839e-17,
                      -1.0, -1.8369701465288538e-16, 1.0, -1.0, 1.0, -1.0, 1.0,
                      -1.8369701465288538e-16, -1.0, 5.510910704284357e-16, 0.0,
                      0.0, 0.0, 0.0, 0.0, -1.0, -1.2246468525851679e-16, 1.0, 0.0,
                      -1.2246468525851679e-16, 2.4492937051703357e-16,
                      -3.6739402930577075e-16, 0.0, 1.0, -3.6739402930577075e-16, -1.0]
        value = numpy.array(list_value, dtype=numpy.float32).reshape((2, 4, 4))

        r_Un_Unsqueezecst2 = ctx.make_const(
            name=make_name('init_Un_Unsqueezecst2'), np_val=value)
        vars['Un_Unsqueezecst2'] = r_Un_Unsqueezecst2.name

        list_value = [-1]
        value = numpy.array(list_value, dtype=numpy.int64)

        r_Co_Concatcst = ctx.make_const(
            name=make_name('init_Co_Concatcst'), np_val=value)
        vars['Co_Concatcst'] = r_Co_Concatcst.name

        list_value = [-2]
        value = numpy.array(list_value, dtype=numpy.int64)

        r_Sl_Slicecst = ctx.make_const(
            name=make_name('init_Sl_Slicecst'), np_val=value)
        vars['Sl_Slicecst'] = r_Sl_Slicecst.name

        value = numpy.array(0, dtype=numpy.int64)

        r_Ga_Gathercst = ctx.make_const(
            name=make_name('init_Ga_Gathercst'), np_val=value)
        vars['Ga_Gathercst'] = r_Ga_Gathercst.name

        list_value = [0, 0]
        value = numpy.array(list_value, dtype=numpy.int64)

        r_Sl_Slicecst2 = ctx.make_const(
            name=make_name('init_Sl_Slicecst2'), np_val=value)
        vars['Sl_Slicecst2'] = r_Sl_Slicecst2.name

        list_value = [1, 4]
        value = numpy.array(list_value, dtype=numpy.int64)

        r_Sl_Slicecst3 = ctx.make_const(
            name=make_name('init_Sl_Slicecst3'), np_val=value)
        vars['Sl_Slicecst3'] = r_Sl_Slicecst3.name

        list_value = [1, 2]
        value = numpy.array(list_value, dtype=numpy.int64)

        r_Sl_Slicecst4 = ctx.make_const(
            name=make_name('init_Sl_Slicecst4'), np_val=value)
        vars['Sl_Slicecst4'] = r_Sl_Slicecst4.name

        list_value = [4]
        value = numpy.array(list_value, dtype=numpy.int64)

        r_Sl_Slicecst6 = ctx.make_const(
            name=make_name('init_Sl_Slicecst6'), np_val=value)
        vars['Sl_Slicecst6'] = r_Sl_Slicecst6.name

        list_value = [1]
        value = numpy.array(list_value, dtype=numpy.int64)

        r_Sl_Slicecst7 = ctx.make_const(
            name=make_name('init_Sl_Slicecst7'), np_val=value)
        vars['Sl_Slicecst7'] = r_Sl_Slicecst7.name

        list_value = [3]
        value = numpy.array(list_value, dtype=numpy.int64)

        r_Sl_Slicecst9 = ctx.make_const(
            name=make_name('init_Sl_Slicecst9'), np_val=value)
        vars['Sl_Slicecst9'] = r_Sl_Slicecst9.name

        value = numpy.array(1, dtype=numpy.int64)

        r_Ga_Gathercst2 = ctx.make_const(
            name=make_name('init_Ga_Gathercst2'), np_val=value)
        vars['Ga_Gathercst2'] = r_Ga_Gathercst2.name

        list_value = [2]
        value = numpy.array(list_value, dtype=numpy.int64)

        r_Sl_Slicecst18 = ctx.make_const(
            name=make_name('init_Sl_Slicecst18'), np_val=value)
        vars['Sl_Slicecst18'] = r_Sl_Slicecst18.name

        list_value = [1, 3]
        value = numpy.array(list_value, dtype=numpy.int64)

        r_Sl_Slicecst24 = ctx.make_const(
            name=make_name('init_Sl_Slicecst24'), np_val=value)
        vars['Sl_Slicecst24'] = r_Sl_Slicecst24.name

        list_value = [2, 3]
        value = numpy.array(list_value, dtype=numpy.int64)

        r_Sl_Slicecst25 = ctx.make_const(
            name=make_name('init_Sl_Slicecst25'), np_val=value)
        vars['Sl_Slicecst25'] = r_Sl_Slicecst25.name

        # nodes
        if getattr(ctx, 'verbose', False):
            print('[nodes] %r' % cls)

        attr = dict()
        inputs = [vars['Un_Unsqueezecst'], vars['Un_Unsqueezecst1'], ]
        node = ctx.make_node(
            'Unsqueeze', inputs=inputs, attr=attr,
            name=make_name('Un_Unsqueeze'))
        vars['Un_expanded0'] = node.output[0]

        attr = dict()
        inputs = [vars['Un_Unsqueezecst2'], vars['Un_Unsqueezecst1'], ]
        node = ctx.make_node(
            'Unsqueeze', inputs=inputs, attr=attr,
            name=make_name('Un_Unsqueeze1'))
        vars['Un_expanded03'] = node.output[0]

        attr = dict()
        inputs = [vars['x'], ]
        node = ctx.make_node(
            'Shape', inputs=inputs, attr=attr,
            name=make_name('Sh_Shape'))
        vars['Sh_shape0'] = node.output[0]

        attr = dict()
        inputs = [vars['Sh_shape0'], ]
        node = ctx.make_node(
            'Shape', inputs=inputs, attr=attr,
            name=make_name('Sh_Shape1'))
        vars['Sh_shape01'] = node.output[0]

        attr = dict(axis=0,)
        inputs = [vars['Sh_shape01'], vars['Ga_Gathercst'], ]
        node = ctx.make_node(
            'Gather', inputs=inputs, attr=attr,
            name=make_name('Ga_Gather'))
        vars['Ga_output01'] = node.output[0]

        attr = dict()
        inputs = [vars['Ga_output01'], vars['Un_Unsqueezecst1'], ]
        node = ctx.make_node(
            'Unsqueeze', inputs=inputs, attr=attr,
            name=make_name('Un_Unsqueeze2'))
        vars['Un_expanded05'] = node.output[0]

        attr = dict(axis=0,)
        inputs = [vars['Un_expanded05'], ]
        node = ctx.make_node(
            'Concat', inputs=inputs, attr=attr,
            name=make_name('Co_Concat'))
        vars['Co_concat_result01'] = node.output[0]

        attr = dict()
        inputs = [vars['Sh_shape0'], vars['Sl_Slicecst'],
                  vars['Co_concat_result01'], vars['Un_Unsqueezecst1'], ]
        node = ctx.make_node(
            'Slice', inputs=inputs, attr=attr,
            name=make_name('Sl_Slice'))
        vars['Sl_output05'] = node.output[0]

        attr = dict(axis=0,)
        inputs = [vars['Co_Concatcst'], vars['Sl_output05'], ]
        node = ctx.make_node(
            'Concat', inputs=inputs, attr=attr,
            name=make_name('Co_Concat1'))
        vars['Co_concat_result0'] = node.output[0]

        attr = dict()
        inputs = [vars['x'], vars['Co_concat_result0'], ]
        node = ctx.make_node(
            'Reshape', inputs=inputs, attr=attr,
            name=make_name('Re_Reshape'))
        vars['Re_reshaped0'] = node.output[0]

        attr = dict()
        inputs = [vars['Re_reshaped0'], vars['Sl_Slicecst2'],
                  vars['Sl_Slicecst3'], vars['Sl_Slicecst4'], ]
        node = ctx.make_node(
            'Slice', inputs=inputs, attr=attr,
            name=make_name('Sl_Slice1'))
        vars['Sl_output04'] = node.output[0]

        attr = dict(perm=[0, 2, 1],)
        inputs = [vars['Sl_output04'], ]
        node = ctx.make_node(
            'Transpose', inputs=inputs, attr=attr,
            name=make_name('Tr_Transpose'))
        vars['Tr_transposed02'] = node.output[0]

        attr = dict()
        inputs = [vars['Tr_transposed02'], vars['Un_Unsqueezecst1'],
                  vars['Sl_Slicecst6'], vars['Sl_Slicecst7'], ]
        node = ctx.make_node(
            'Slice', inputs=inputs, attr=attr,
            name=make_name('Sl_Slice2'))
        vars['Sl_output03'] = node.output[0]

        attr = dict()
        inputs = [vars['Sl_output03'], vars['Sl_Slicecst7'], ]
        node = ctx.make_node(
            'Unsqueeze', inputs=inputs, attr=attr,
            name=make_name('Un_Unsqueeze3'))
        vars['Un_expanded04'] = node.output[0]

        attr = dict()
        inputs = [vars['Un_expanded03'], vars['Un_expanded04'], ]
        node = ctx.make_node(
            'MatMul', inputs=inputs, attr=attr,
            name=make_name('Ma_MatMul'))
        vars['Ma_Y01'] = node.output[0]

        attr = dict()
        inputs = [vars['Ma_Y01'], vars['Un_Unsqueezecst1'],
                  vars['Sl_Slicecst9'], vars['Sl_Slicecst7'], ]
        node = ctx.make_node(
            'Slice', inputs=inputs, attr=attr,
            name=make_name('Sl_Slice3'))
        vars['Sl_output02'] = node.output[0]

        attr = dict(perm=[1, 0, 3, 2],)
        inputs = [vars['Sl_output02'], ]
        node = ctx.make_node(
            'Transpose', inputs=inputs, attr=attr,
            name=make_name('Tr_Transpose1'))
        vars['Tr_transposed01'] = node.output[0]

        attr = dict(axis=0,)
        inputs = [vars['Tr_transposed01'], vars['Ga_Gathercst'], ]
        node = ctx.make_node(
            'Gather', inputs=inputs, attr=attr,
            name=make_name('Ga_Gather1'))
        vars['Ga_output0'] = node.output[0]

        attr = dict()
        inputs = [vars['Ga_output0'], vars['Un_Unsqueezecst1'],
                  vars['Sl_Slicecst7'], vars['Sl_Slicecst7'], ]
        node = ctx.make_node(
            'Slice', inputs=inputs, attr=attr,
            name=make_name('Sl_Slice4'))
        vars['Sl_output01'] = node.output[0]

        attr = dict()
        inputs = [vars['Sl_output01'], vars['Sl_Slicecst7'], ]
        node = ctx.make_node(
            'Unsqueeze', inputs=inputs, attr=attr,
            name=make_name('Un_Unsqueeze4'))
        vars['Un_expanded02'] = node.output[0]

        attr = dict()
        inputs = [vars['Un_expanded0'], vars['Un_expanded02'], ]
        node = ctx.make_node(
            'MatMul', inputs=inputs, attr=attr,
            name=make_name('Ma_MatMul1'))
        vars['Ma_Y0'] = node.output[0]

        attr = dict(perm=[1, 0, 2, 3],)
        inputs = [vars['Ma_Y0'], ]
        node = ctx.make_node(
            'Transpose', inputs=inputs, attr=attr,
            name=make_name('Tr_Transpose2'))
        vars['Tr_transposed0'] = node.output[0]

        attr = dict(axis=0,)
        inputs = [vars['Tr_transposed01'], vars['Ga_Gathercst2'], ]
        node = ctx.make_node(
            'Gather', inputs=inputs, attr=attr,
            name=make_name('Ga_Gather2'))
        vars['Ga_output03'] = node.output[0]

        attr = dict()
        inputs = [vars['Ga_output03'], vars['Un_Unsqueezecst1'],
                  vars['Sl_Slicecst7'], vars['Sl_Slicecst7'], ]
        node = ctx.make_node(
            'Slice', inputs=inputs, attr=attr,
            name=make_name('Sl_Slice5'))
        vars['Sl_output07'] = node.output[0]

        attr = dict()
        inputs = [vars['Sl_output07'], vars['Sl_Slicecst7'], ]
        node = ctx.make_node(
            'Unsqueeze', inputs=inputs, attr=attr,
            name=make_name('Un_Unsqueeze6'))
        vars['Un_expanded07'] = node.output[0]

        attr = dict()
        inputs = [vars['Un_expanded0'], vars['Un_expanded07'], ]
        node = ctx.make_node(
            'MatMul', inputs=inputs, attr=attr,
            name=make_name('Ma_MatMul2'))
        vars['Ma_Y03'] = node.output[0]

        attr = dict(perm=[1, 0, 2, 3],)
        inputs = [vars['Ma_Y03'], ]
        node = ctx.make_node(
            'Transpose', inputs=inputs, attr=attr,
            name=make_name('Tr_Transpose3'))
        vars['Tr_transposed04'] = node.output[0]

        attr = dict()
        inputs = [vars['Tr_transposed04'], vars['Sl_Slicecst7'],
                  vars['Sl_Slicecst18'], vars['Un_Unsqueezecst1'], ]
        node = ctx.make_node(
            'Slice', inputs=inputs, attr=attr,
            name=make_name('Sl_Slice6'))
        vars['Sl_output06'] = node.output[0]

        attr = dict()
        inputs = [vars['Sl_output06'], ]
        node = ctx.make_node(
            'Neg', inputs=inputs, attr=attr,
            name=make_name('Ne_Neg'))
        vars['Ne_Y0'] = node.output[0]

        attr = dict()
        inputs = [vars['Tr_transposed04'], vars['Un_Unsqueezecst1'],
                  vars['Sl_Slicecst7'], vars['Un_Unsqueezecst1'], ]
        node = ctx.make_node(
            'Slice', inputs=inputs, attr=attr,
            name=make_name('Sl_Slice7'))
        vars['Sl_output08'] = node.output[0]

        attr = dict(axis=0,)
        inputs = [vars['Ne_Y0'], vars['Sl_output08'], ]
        node = ctx.make_node(
            'Concat', inputs=inputs, attr=attr,
            name=make_name('Co_Concat2'))
        vars['Co_concat_result03'] = node.output[0]

        attr = dict()
        inputs = [vars['Tr_transposed0'], vars['Co_concat_result03'], ]
        node = ctx.make_node(
            'Add', inputs=inputs, attr=attr,
            name=make_name('Ad_Add'))
        vars['Ad_C0'] = node.output[0]

        attr = dict()
        inputs = [vars['Ad_C0'], vars['Sl_Slicecst2'],
                  vars['Sl_Slicecst24'], vars['Sl_Slicecst25'], ]
        node = ctx.make_node(
            'Slice', inputs=inputs, attr=attr,
            name=make_name('Sl_Slice8'))
        vars['Sl_output0'] = node.output[0]

        attr = dict()
        inputs = [vars['Sh_shape0'], vars['Un_Unsqueezecst1'],
                  vars['Sl_Slicecst'], vars['Un_Unsqueezecst1'], ]
        node = ctx.make_node(
            'Slice', inputs=inputs, attr=attr,
            name=make_name('Sl_Slice9'))
        vars['Sl_output010'] = node.output[0]

        attr = dict()
        inputs = [vars['Sl_output0'], ]
        node = ctx.make_node(
            'Shape', inputs=inputs, attr=attr,
            name=make_name('Sh_Shape3'))
        vars['Sh_shape03'] = node.output[0]

        attr = dict()
        inputs = [vars['Sh_shape03'], ]
        node = ctx.make_node(
            'Shape', inputs=inputs, attr=attr,
            name=make_name('Sh_Shape4'))
        vars['Sh_shape04'] = node.output[0]

        attr = dict(axis=0,)
        inputs = [vars['Sh_shape04'], vars['Ga_Gathercst'], ]
        node = ctx.make_node(
            'Gather', inputs=inputs, attr=attr,
            name=make_name('Ga_Gather3'))
        vars['Ga_output04'] = node.output[0]

        attr = dict()
        inputs = [vars['Ga_output04'], vars['Un_Unsqueezecst1'], ]
        node = ctx.make_node(
            'Unsqueeze', inputs=inputs, attr=attr,
            name=make_name('Un_Unsqueeze7'))
        vars['Un_expanded08'] = node.output[0]

        attr = dict(axis=0,)
        inputs = [vars['Un_expanded08'], ]
        node = ctx.make_node(
            'Concat', inputs=inputs, attr=attr,
            name=make_name('Co_Concat3'))
        vars['Co_concat_result05'] = node.output[0]

        attr = dict()
        inputs = [vars['Sh_shape03'], vars['Sl_Slicecst'],
                  vars['Co_concat_result05'], vars['Un_Unsqueezecst1'], ]
        node = ctx.make_node(
            'Slice', inputs=inputs, attr=attr,
            name=make_name('Sl_Slice10'))
        vars['Sl_output012'] = node.output[0]

        attr = dict(axis=0,)
        inputs = [vars['Sl_Slicecst18'],
                  vars['Sl_output010'], vars['Sl_output012'], ]
        node = ctx.make_node(
            'Concat', inputs=inputs, attr=attr,
            name=make_name('Co_Concat4'))
        vars['Co_concat_result04'] = node.output[0]

        attr = dict()
        inputs = [vars['Sl_output0'], vars['Co_concat_result04'], ]
        node = ctx.make_node(
            'Reshape', inputs=inputs, attr=attr,
            name=make_name('Re_Reshape1'))
        vars['y'] = node.output[0]

        # finalize
        if getattr(ctx, 'verbose', False):
            print('[replace_all_inputs] %r' % cls)
        ctx.replace_all_inputs(oldnode.output[0], node.output[0])
        ctx.remove_node(oldnode.name)

    @classmethod
    def version_13(cls, ctx, node, **kwargs):
        return cls.any_version(13, ctx, node, **kwargs)


class TestExportOnnx(ExtTestCase):

    def verify(self, content):
        try:
            left, __ = verify_code(content, exc=False)
        except SyntaxError as e:
            raise AssertionError(
                "Unable to analyse a script due to %r. "
                "\n--CODE--\n%s"
                "" % (e, content)) from e

        # execution
        try:
            obj = compile(content, '<string>', 'exec')
        except SyntaxError as e:
            raise AssertionError(
                "Unable to compile a script due to %r. "
                "\n--CODE--\n%s"
                "" % (e, print_code(content))) from e
        glo = globals().copy()
        loc = {'numpy_helper': numpy_helper,
               'make_model': make_model,
               'make_node': make_node,
               'set_model_props': set_model_props,
               'make_tensor': make_tensor,
               'make_graph': make_graph,
               'make_tensor_value_info': make_tensor_value_info,
               'print': print, 'sorted': sorted,
               'collections': collections, 'inspect': inspect}
        out = StringIO()
        err = StringIO()
        if len(left) >= 5:
            raise AssertionError(
                "Too many unknown symbols: %r." % left)

        with redirect_stdout(out):
            with redirect_stderr(err):
                try:
                    exec(obj, glo, loc)  # pylint: disable=W0122
                except Exception as e:
                    raise AssertionError(
                        "Unable to execute a script due to %r. "
                        "\n--OUT--\n%s\n--ERR--\n%s\n--CODE--\n%s"
                        "" % (e, out.getvalue(), err.getvalue(),
                              print_code(content))) from e
        return glo, loc

    def test_export_onnx(self):
        this = os.path.dirname(__file__)
        folder = os.path.join(this, "data")
        names = ["fft2d_any.onnx"]
        for name in names:
            with self.subTest(name=name):
                oinf0 = OnnxInference(os.path.join(folder, name))

                x = numpy.random.randn(3, 1, 4).astype(numpy.float32)
                y = oinf0.run({'x': x})

                new_onnx = export2onnx(
                    os.path.join(folder, name), name="FFT2D")
                _, loc = self.verify(new_onnx)
                model = loc['onnx_model']
                oinf = OnnxInference(model)
                y1 = oinf.run({'x': x})

                new_onnx = export2onnx(
                    os.path.join(folder, name), verbose=False)
                _, loc = self.verify(new_onnx)
                model = loc['onnx_model']
                oinf = OnnxInference(model)
                y2 = oinf.run({'x': x})

                self.assertEqualArray(y['y'], y1['y'])
                self.assertEqualArray(y['y'], y2['y'])

    def verify_tf(self, content):
        try:
            left, __ = verify_code(content, exc=False)
        except SyntaxError as e:
            raise AssertionError(
                "Unable to analyse a script due to %r. "
                "\n--CODE--\n%s"
                "" % (e, content)) from e

        # execution
        try:
            obj = compile(content, '<string>', 'exec')
        except SyntaxError as e:
            raise AssertionError(
                "Unable to compile a script due to %r. "
                "\n--CODE--\n%s"
                "" % (e, print_code(content))) from e
        glo = globals().copy()
        loc = {'numpy': numpy, 'dict': dict, 'list': list,
               'print': print, 'sorted': sorted,
               'collections': collections, 'inspect': inspect,
               'helper': helper, "make_sure": make_sure,
               'ConvertFFT2DOp': ConvertFFT2DOp, "make_name": make_name}
        out = StringIO()
        err = StringIO()
        if len(left) >= 14:
            raise AssertionError(
                "Too many unknown symbols: %r." % left)

        with redirect_stdout(out):
            with redirect_stderr(err):
                try:
                    exec(obj, glo, loc)  # pylint: disable=W0122
                except Exception as e:
                    raise AssertionError(
                        "Unable to execute a script due to %r. "
                        "\n--OUT--\n%s\n--ERR--\n%s\n--CODE--\n%s"
                        "" % (e, out.getvalue(), err.getvalue(),
                              print_code(content))) from e
        return glo, loc

    def test_export2tf2onnx(self):
        this = os.path.dirname(__file__)
        folder = os.path.join(this, "data")
        names = ["fft2d_any.onnx"]
        for name in names:
            with self.subTest(name=name):
                oinf0 = OnnxInference(os.path.join(folder, name))

                x = numpy.random.randn(3, 1, 4).astype(numpy.float32)
                y = oinf0.run({'x': x})

                new_onnx = export2tf2onnx(
                    os.path.join(folder, name), name="FFT2D")
                _, loc = self.verify_tf(new_onnx)
                model = loc['onnx_raw']
                self.assertIn('op_type: "FFT2D"', str(model))
                model = loc['onnx_model']
                self.assertNotIn('op_type: "FFT2D"', str(model))

                oinf = OnnxInference(model)
                y1 = oinf.run({'x': x})

                new_onnx = export2tf2onnx(
                    os.path.join(folder, name), name="FFT2D")
                _, loc = self.verify_tf(new_onnx)
                model = loc['onnx_model']
                self.assertNotIn('op_type: "FFT2D"', str(model))
                oinf = OnnxInference(model)
                y2 = oinf.run({'x': x})

                self.assertEqualArray(y['y'], y1['y'])
                self.assertEqualArray(y['y'], y2['y'])


if __name__ == "__main__":
    unittest.main()
