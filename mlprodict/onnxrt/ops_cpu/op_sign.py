# -*- encoding: utf-8 -*-
# pylint: disable=E0203,E1101,C0111
"""
@file
@brief Runtime operator.
"""
import numpy
from ._op import OpRunUnaryNum


class Sign(OpRunUnaryNum):
    """
    Runtime for operator `Sign
    <https://github.com/onnx/onnx/blob/master/docs/
    Operators.md#Sign>`_.
    """

    def __init__(self, onnx_node, desc=None, **options):
        OpRunUnaryNum.__init__(self, onnx_node, desc=desc,
                               **options)

    def _run(self, x):  # pylint: disable=W0221
        if self.inplaces.get(0, False):
            return self._run_inplace(x)
        return (numpy.sign(x), )

    def _run_inplace(self, x):
        return (numpy.sign(x, out=x), )

    def to_python(self, inputs):
        return self._to_python_numpy(inputs, self.__class__.__name__.lower())
