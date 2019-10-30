"""
@brief      test log(time=2s)
"""
import unittest
from logging import getLogger
import platform
import warnings
import numpy
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR, SVC, LinearSVC, OneClassSVM
from sklearn.exceptions import ConvergenceWarning
try:
    from sklearn.utils._testing import ignore_warnings
except ImportError:
    from sklearn.utils.testing import ignore_warnings
import skl2onnx
from pyquickhelper.pycode import ExtTestCase, unittest_require_at_least
from mlprodict.onnxrt import OnnxInference
from mlprodict.onnx_conv import register_rewritten_operators, to_onnx


class TestOnnxrtPythonRuntimeMlSVM(ExtTestCase):

    def setUp(self):
        logger = getLogger('skl2onnx')
        logger.disabled = True
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            register_rewritten_operators()

    def test_openmp_compilation_float(self):
        from mlprodict.onnxrt.ops_cpu.op_svm_regressor_ import RuntimeSVMRegressorFloat  # pylint: disable=E0611
        ru = RuntimeSVMRegressorFloat()
        r = ru.runtime_options()
        if platform.system().lower() == 'darwin':
            # openmp disabled
            self.assertEqual('', r)
        else:
            self.assertEqual('OPENMP', r)
            nb = ru.omp_get_max_threads()
            self.assertGreater(nb, 0)

    def test_openmp_compilation_double(self):
        from mlprodict.onnxrt.ops_cpu.op_svm_regressor_ import RuntimeSVMRegressorDouble  # pylint: disable=E0611
        ru = RuntimeSVMRegressorDouble()
        r = ru.runtime_options()
        if platform.system().lower() == 'darwin':
            # openmp disabled
            self.assertEqual('', r)
        else:
            self.assertEqual('OPENMP', r)
            nb = ru.omp_get_max_threads()
            self.assertGreater(nb, 0)

    @ignore_warnings(category=(UserWarning, ConvergenceWarning, RuntimeWarning))
    def test_onnxrt_python_SVR(self):
        iris = load_iris()
        X, y = iris.data, iris.target
        X_train, X_test, y_train, _ = train_test_split(X, y, random_state=11)
        clr = SVR()
        clr.fit(X_train, y_train)

        model_def = to_onnx(clr, X_train.astype(numpy.float32))
        oinf = OnnxInference(model_def)
        text = "\n".join(map(lambda x: str(x.ops_), oinf.sequence_))
        self.assertIn("SVMRegressor", text)
        y = oinf.run({'X': X_test.astype(numpy.float32)})
        self.assertEqual(list(sorted(y)), ['variable'])
        lexp = clr.predict(X_test)
        self.assertEqual(lexp.shape, y['variable'].shape)
        self.assertEqualArray(lexp, y['variable'], decimal=5)

    @unittest_require_at_least(skl2onnx, '1.5.9999')
    @ignore_warnings(category=(UserWarning, ConvergenceWarning, RuntimeWarning))
    def test_onnxrt_python_SVC_proba(self):
        iris = load_iris()
        X, y = iris.data, iris.target
        X_train, X_test, y_train, _ = train_test_split(X, y, random_state=11)
        clr = SVC(probability=True)
        clr.fit(X_train, y_train)

        model_def = to_onnx(clr, X_train.astype(numpy.float32))
        oinf = OnnxInference(model_def)
        text = "\n".join(map(lambda x: str(x.ops_), oinf.sequence_))
        self.assertIn("SVMClassifier", text)
        y = oinf.run({'X': X_test.astype(numpy.float32)})
        self.assertEqual(list(sorted(y)), [
                         'output_label', 'output_probability'])
        lexp = clr.predict(X_test)
        lprob = clr.predict_proba(X_test)
        got = y['output_probability'].values
        self.assertEqual(lexp.shape, y['output_label'].shape)
        self.assertEqual(lprob.shape, got.shape)
        self.assertEqualArray(lexp, y['output_label'], decimal=5)
        self.assertEqualArray(lprob, got, decimal=5)

    @ignore_warnings(category=(UserWarning, ConvergenceWarning, RuntimeWarning))
    def test_onnxrt_python_SVC_proba_linear(self):
        iris = load_iris()
        X, y = iris.data, iris.target
        X_train, X_test, y_train, _ = train_test_split(X, y, random_state=11)
        clr = LinearSVC()
        clr.fit(X_train, y_train)

        model_def = to_onnx(clr, X_train.astype(numpy.float32))
        oinf = OnnxInference(model_def)
        text = "\n".join(map(lambda x: str(x.ops_), oinf.sequence_))
        self.assertIn("LinearClassifier", text)
        y = oinf.run({'X': X_test.astype(numpy.float32)})
        self.assertEqual(list(sorted(y)), ['label', 'probabilities'])
        lexp = clr.predict(X_test)
        lprob = clr.decision_function(X_test)
        self.assertEqual(lexp.shape, y['label'].shape)
        self.assertEqual(lprob.shape, y['probabilities'].shape)
        self.assertEqualArray(lexp, y['label'], decimal=5)
        self.assertEqualArray(lprob, y['probabilities'], decimal=5)

    @unittest_require_at_least(skl2onnx, '1.5.9999')
    @ignore_warnings(category=(UserWarning, ConvergenceWarning, RuntimeWarning))
    def test_onnxrt_python_SVC_proba_bin(self):
        iris = load_iris()
        X, y = iris.data, iris.target
        y[y == 2] = 1
        X_train, X_test, y_train, _ = train_test_split(X, y, random_state=11)
        clr = SVC(probability=True)
        clr.fit(X_train, y_train)

        model_def = to_onnx(clr, X_train.astype(numpy.float32))
        oinf = OnnxInference(model_def)
        text = "\n".join(map(lambda x: str(x.ops_), oinf.sequence_))
        self.assertIn("SVMClassifier", text)
        y = oinf.run({'X': X_test.astype(numpy.float32)})
        self.assertEqual(list(sorted(y)), [
                         'output_label', 'output_probability'])
        lexp = clr.predict(X_test)
        lprob = clr.predict_proba(X_test)
        got = y['output_probability'].values
        self.assertEqual(lexp.shape, y['output_label'].shape)
        self.assertEqual(lprob.shape, got.shape)
        self.assertEqualArray(lexp, y['output_label'], decimal=5)
        self.assertEqualArray(lprob, got, decimal=5)

    @unittest_require_at_least(skl2onnx, '1.5.9999')
    @ignore_warnings(category=(UserWarning, ConvergenceWarning, RuntimeWarning))
    def test_onnxrt_python_one_class_svm(self):
        X = numpy.array([[0, 1, 2], [44, 36, 18],
                         [-45, -78, -46]], dtype=numpy.float32)

        for kernel in ['linear', 'sigmoid', 'rbf', 'poly']:
            model = OneClassSVM(kernel=kernel).fit(X)
            X32 = X.astype(numpy.float32)
            model_onnx = to_onnx(model, X32)
            oinf = OnnxInference(model_onnx, runtime='python')
            res = oinf.run({'X': X32})
            scores = res['scores']
            dec = model.decision_function(X32)
            self.assertEqualArray(scores, dec, decimal=4)
            # print("32", kernel + ("-" * (7 - len(kernel))), scores - dec, "skl", dec)

        for kernel in ['linear', 'sigmoid', 'rbf', 'poly']:
            model = OneClassSVM(kernel=kernel).fit(X)
            X64 = X.astype(numpy.float64)
            model_onnx = to_onnx(model, X64, dtype=numpy.float64)
            self.assertIn("SVMRegressorDouble", str(model_onnx))
            oinf = OnnxInference(model_onnx, runtime='python')
            res = oinf.run({'X': X64})
            scores = res['scores']
            dec = model.decision_function(X64)
            self.assertEqualArray(scores, dec, decimal=4)
            # print("64", kernel + ("-" * (7 - len(kernel))), scores - dec, "skl", dec)


if __name__ == "__main__":
    unittest.main()
