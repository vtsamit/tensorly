import ivy
from ivy.functional.frontends.numpy.linalg.norms_and_other_numbers import matrix_rank

from .core import (
    Backend,
    backend_types,
    backend_basic_math,
    backend_array,
)

import numpy as np


class ivyBackend(Backend, backend_name="ivy"):
    @staticmethod
    def context(tensor):
        return {"dtype": tensor.dtype}

    @staticmethod
    def tensor(data, dtype=None, **kwargs):
        return ivy.array(data, dtype=dtype)

    @staticmethod
    def lstsq(a, b, rcond="warn"):
        solution = ivy.matmul(
            ivy.pinv(a, rtol=1e-15).astype(ivy.float64), b.astype(ivy.float64)
        )
        svd = ivy.svd(a, compute_uv=False)
        rank = matrix_rank(a).astype(ivy.int32)
        residuals = ivy.sum((b - ivy.matmul(a, solution)) ** 2).astype(ivy.float64)
        return (solution, residuals)

    # Array Manipulation
    @staticmethod
    def clip(tensor, a_min=None, a_max=None):
        return ivy.clip(tensor, a_min, a_max)

    @staticmethod
    def concatenate(tensors, axis=0):
        return ivy.concat(tensors, axis=axis)

    @staticmethod
    def copy(tensor, order="k", subok=False):
        return ivy.copy_array(tensor, to_ivy_array=False)

    @staticmethod
    def reshape(tensor, newshape, order="c"):
        return ivy.reshape(tensor, shape=newshape, order=order)

    # transpose

    @staticmethod
    def to_numpy(tensor):
        return ivy.to_numpy(tensor)

    def transpose(self, tensor, axes=None):
        axes = axes or list(range(self.ndim(tensor)))[::-1]
        return ivy.permute_dims(tensor, axes)

    @staticmethod
    def sum(tensor, axis=None, dtype=None, keepdims=False):
        return ivy.sum(tensor, axis=axis, dtype=dtype, keepdims=keepdims)

    # complex(sqrt)

    @staticmethod
    def stack(arrays, axis=0):
        return ivy.stack(arrays, axis=axis)

    @staticmethod
    def sort(tensor, axis=-1):
        if axis is None:
            tensor = tensor.flatten()
            axis = -1

        return ivy.sort(tensor, axis=axis, descending=False, stable=True)

    @staticmethod
    def prod(tensor, axis=None, dtype=None, keepdims=False):
        return ivy.prod(tensor, axis=axis, dtype=dtype, keepdims=keepdims)

    # complex (sign)
    @staticmethod
    def sign(tensor):
        return ivy.sign(tensor)

    @staticmethod
    def abs(tensor, where=True):
        return ivy.abs(tensor, where=where)

    @staticmethod
    def mean(tensor, axis=None):
        if axis is None:
            return ivy.mean(tensor)
        else:
            return ivy.mean(tensor, axis=axis)

    @staticmethod
    def all(tensor, axis=None, keepdims=False):
        return ivy.all(tensor, axis=axis, keepdims=keepdims)

    @staticmethod
    def argmin(tensor, axis=None, keepdims=False):
        return ivy.argmin(tensor, axis=axis, keepdims=keepdims)

    @staticmethod
    def argmax(tensor, axis=None, keepdims=False):
        return ivy.argmax(tensor, axis=axis, keepdims=keepdims)

    @staticmethod
    def max(tensor, axis=None, keepdims=False):
        return ivy.max(tensor, axis=axis, keepdims=keepdims)

    @staticmethod
    def min(tensor, axis=None, keepdims=False):
        return ivy.min(tensor, axis=axis, keepdims=keepdims)

    @staticmethod
    def conj(tensor):
        return ivy.conj(tensor)

    @staticmethod
    def arange(start=0, stop=None, step=1.0, dtype=None):
        return ivy.arange(start, stop=stop, step=step, dtype=dtype)

    @staticmethod
    def moveaxis(array, source, destination):
        return ivy.moveaxis(array, source, destination)

    @staticmethod
    def shape(tensor):
        return tuple(ivy.shape(tensor, as_array=False))

    @staticmethod
    def ndim(tensor):
        return ivy.get_num_dims(tensor)

    # Algebraic Operations

    @staticmethod
    def dot(a, b):
        if a.ndim > 2 and b.ndim > 2:
            return ivy.tensordot(a, b, axes=([-1], [-2]))
        if not a.ndim or not b.ndim:
            return a * b
        return ivy.matmul(
            a, b, transpose_a=False, transpose_b=False, adjoint_a=False, adjoint_b=False
        )

    @staticmethod
    def matmul(a, b):
        return ivy.matmul(
            a, b, transpose_a=False, transpose_b=False, adjoint_a=False, adjoint_b=False
        )

    @staticmethod
    def kron(a, b):
        return ivy.kron(a, b)

    @staticmethod
    def solve(a, b):
        return ivy.solve(a, b)

    @staticmethod
    def qr(a, mode="reduced"):
        return ivy.qr(a, mode=mode)

    # Array Creation

    @staticmethod
    def ones(shape, dtype=None):
        return ivy.ones(shape, dtype=dtype)

    @staticmethod
    def zeros(shape, dtype=float):
        return ivy.zeros(shape, dtype=dtype)

    @staticmethod
    def zeros_like(a, dtype=None):
        return ivy.zeros_like(a, dtype=dtype)

    @staticmethod
    def eye(n, m=None, k=0, dtype="float"):
        return ivy.eye(n, m, k=k, dtype=dtype)

    @staticmethod
    def diag(v, k=0):
        return ivy.diag(v, k=k)

    @staticmethod
    def eigh(tensor):
        return ivy.eigh(tensor)

    @staticmethod
    def is_tensor(tensor):
        return ivy.is_array(tensor)

    @staticmethod
    def argsort(input, axis=None):
        return ivy.argsort(input, axis=axis, descending=False, stable=True)

    @staticmethod
    def log(x):
        return ivy.log(x)

    @staticmethod
    def log2(x):
        return ivy.log2(x)

    @staticmethod
    def finfo(x):
        return ivy.finfo(x)

    @staticmethod
    def log2(x):
        return ivy.log2(x)

    @staticmethod
    def tensordot(a, b, axes=2):
        return ivy.tensordot(a, b, axes=axes)

    @staticmethod
    def logsumexp(input, dim, keepdim=False, *, out=None):
        c = ivy.max(input, axis=dim, keepdims=True)
        if ivy.get_num_dims(c) > 0:
            c = ivy.where(ivy.isinf(c), ivy.zeros_like(c), c)
        elif not ivy.isinf(c):
            c = 0
        exponential = ivy.exp(input - c)
        sum = ivy.sum(exponential, axis=dim, keepdims=keepdim)
        ret = ivy.log(sum)
        if not keepdim:
            c = ivy.squeeze(c, axis=dim)
        ret = ivy.add(ret, c, out=out)
        return ret

    @staticmethod
    def flip(tensor, axis=None):
        if isinstance(axis, int):
            axis = [axis]

        if axis is None:
            return ivy.flip(tensor, axis=[i for i in range(ivy.get_num_dims(tensor))])
        else:
            return ivy.flip(tensor, axis=axis)


for name in (
    backend_types
    + backend_basic_math
    + backend_array
    + [
        "nan",
        "trace",
    ]
):
    ivyBackend.register_method(name, getattr(ivy, name))


for name in ["svd"]:
    ivyBackend.register_method(name, getattr(ivy.linear_algebra, name))