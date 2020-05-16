"""
@file
@brief Inspired from skl2onnx, handles two backends.
"""
from onnxruntime import InferenceSession
from pyquickhelper.pycode import is_travis_or_appveyor
from .utils_backend_common_compare import compare_runtime_session


def _capture_output(fct, kind):
    if is_travis_or_appveyor():
        return fct(), None, None
    from cpyquickhelper.io import capture_output
    return capture_output(fct, kind)


class InferenceSession2:
    """
    Overwrites class *InferenceSession* to capture
    the standard output and error.
    """

    def __init__(self, *args, **kwargs):
        "Overwrites the constructor."
        self.sess, self.outi, self.erri = _capture_output(
            lambda: InferenceSession(*args, **kwargs), 'c')

    def run(self, *args, **kwargs):
        "Overwrites method *run*."
        res, self.outr, self.errr = _capture_output(
            lambda: self.sess.run(*args, **kwargs), 'c')
        return res

    def get_inputs(self, *args, **kwargs):
        "Overwrites method *get_inputs*."
        return self.sess.get_inputs(*args, **kwargs)

    def get_outputs(self, *args, **kwargs):
        "Overwrites method *get_outputs*."
        return self.sess.get_outputs(*args, **kwargs)


def compare_runtime(test, decimal=5, options=None,
                    verbose=False, context=None, comparable_outputs=None,
                    intermediate_steps=False, classes=None):
    """
    The function compares the expected output (computed with
    the model before being converted to ONNX) and the ONNX output
    produced with module :epkg:`onnxruntime` or :epkg:`mlprodict`.

    :param test: dictionary with the following keys:
        - *onnx*: onnx model (filename or object)
        - *expected*: expected output (filename pkl or object)
        - *data*: input data (filename pkl or object)
    :param decimal: precision of the comparison
    :param options: comparison options
    :param context: specifies custom operators
    :param verbose: in case of error, the function may print
        more information on the standard output
    :param comparable_outputs: compare only these outputs
    :param intermediate_steps: displays intermediate steps
        in case of an error
    :param classes: classes names (if option 'nocl' is used)
    :return: tuple (outut, lambda function to run the predictions)

    The function does not return anything but raises an error
    if the comparison failed.
    """
    return compare_runtime_session(
        InferenceSession2, test, decimal=decimal, options=options,
        verbose=verbose, context=context,
        comparable_outputs=comparable_outputs,
        intermediate_steps=intermediate_steps,
        classes=classes)
