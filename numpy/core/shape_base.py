from __future__ import division, absolute_import, print_function

import itertools

__all__ = ['atleast_1d', 'atleast_2d', 'atleast_3d', 'block', 'hstack',
           'stack', 'vstack']


from . import numeric as _nx
from .numeric import array, asanyarray, newaxis
from .multiarray import normalize_axis_index

def atleast_1d(*arys):
    """
    Convert inputs to arrays with at least one dimension.

    Scalar inputs are converted to 1-dimensional arrays, whilst
    higher-dimensional inputs are preserved.

    Parameters
    ----------
    arys1, arys2, ... : array_like
        One or more input arrays.

    Returns
    -------
    ret : ndarray
        An array, or list of arrays, each with ``a.ndim >= 1``.
        Copies are made only if necessary.

    See Also
    --------
    atleast_2d, atleast_3d

    Examples
    --------
    >>> np.atleast_1d(1.0)
    array([ 1.])

    >>> x = np.arange(9.0).reshape(3,3)
    >>> np.atleast_1d(x)
    array([[ 0.,  1.,  2.],
           [ 3.,  4.,  5.],
           [ 6.,  7.,  8.]])
    >>> np.atleast_1d(x) is x
    True

    >>> np.atleast_1d(1, [3, 4])
    [array([1]), array([3, 4])]

    """
    res = []
    for ary in arys:
        ary = asanyarray(ary)
        if ary.ndim == 0:
            result = ary.reshape(1)
        else:
            result = ary
        res.append(result)
    if len(res) == 1:
        return res[0]
    else:
        return res

def atleast_2d(*arys):
    """
    View inputs as arrays with at least two dimensions.

    Parameters
    ----------
    arys1, arys2, ... : array_like
        One or more array-like sequences.  Non-array inputs are converted
        to arrays.  Arrays that already have two or more dimensions are
        preserved.

    Returns
    -------
    res, res2, ... : ndarray
        An array, or list of arrays, each with ``a.ndim >= 2``.
        Copies are avoided where possible, and views with two or more
        dimensions are returned.

    See Also
    --------
    atleast_1d, atleast_3d

    Examples
    --------
    >>> np.atleast_2d(3.0)
    array([[ 3.]])

    >>> x = np.arange(3.0)
    >>> np.atleast_2d(x)
    array([[ 0.,  1.,  2.]])
    >>> np.atleast_2d(x).base is x
    True

    >>> np.atleast_2d(1, [1, 2], [[1, 2]])
    [array([[1]]), array([[1, 2]]), array([[1, 2]])]

    """
    res = []
    for ary in arys:
        ary = asanyarray(ary)
        if ary.ndim == 0:
            result = ary.reshape(1, 1)
        elif ary.ndim == 1:
            result = ary[newaxis,:]
        else:
            result = ary
        res.append(result)
    if len(res) == 1:
        return res[0]
    else:
        return res

def atleast_3d(*arys):
    """
    View inputs as arrays with at least three dimensions.

    Parameters
    ----------
    arys1, arys2, ... : array_like
        One or more array-like sequences.  Non-array inputs are converted to
        arrays.  Arrays that already have three or more dimensions are
        preserved.

    Returns
    -------
    res1, res2, ... : ndarray
        An array, or list of arrays, each with ``a.ndim >= 3``.  Copies are
        avoided where possible, and views with three or more dimensions are
        returned.  For example, a 1-D array of shape ``(N,)`` becomes a view
        of shape ``(1, N, 1)``, and a 2-D array of shape ``(M, N)`` becomes a
        view of shape ``(M, N, 1)``.

    See Also
    --------
    atleast_1d, atleast_2d

    Examples
    --------
    >>> np.atleast_3d(3.0)
    array([[[ 3.]]])

    >>> x = np.arange(3.0)
    >>> np.atleast_3d(x).shape
    (1, 3, 1)

    >>> x = np.arange(12.0).reshape(4,3)
    >>> np.atleast_3d(x).shape
    (4, 3, 1)
    >>> np.atleast_3d(x).base is x.base  # x is a reshape, so not base itself
    True

    >>> for arr in np.atleast_3d([1, 2], [[1, 2]], [[[1, 2]]]):
    ...     print(arr, arr.shape)
    ...
    [[[1]
      [2]]] (1, 2, 1)
    [[[1]
      [2]]] (1, 2, 1)
    [[[1 2]]] (1, 1, 2)

    """
    res = []
    for ary in arys:
        ary = asanyarray(ary)
        if ary.ndim == 0:
            result = ary.reshape(1, 1, 1)
        elif ary.ndim == 1:
            result = ary[newaxis,:, newaxis]
        elif ary.ndim == 2:
            result = ary[:,:, newaxis]
        else:
            result = ary
        res.append(result)
    if len(res) == 1:
        return res[0]
    else:
        return res


def vstack(tup):
    """
    Stack arrays in sequence vertically (row wise).

    This is equivalent to concatenation along the first axis after 1-D arrays
    of shape `(N,)` have been reshaped to `(1,N)`. Rebuilds arrays divided by
    `vsplit`.

    This function makes most sense for arrays with up to 3 dimensions. For
    instance, for pixel-data with a height (first axis), width (second axis),
    and r/g/b channels (third axis). The functions `concatenate`, `stack` and
    `block` provide more general stacking and concatenation operations.

    Parameters
    ----------
    tup : sequence of ndarrays
        The arrays must have the same shape along all but the first axis.
        1-D arrays must have the same length.

    Returns
    -------
    stacked : ndarray
        The array formed by stacking the given arrays, will be at least 2-D.

    See Also
    --------
    stack : Join a sequence of arrays along a new axis.
    hstack : Stack arrays in sequence horizontally (column wise).
    dstack : Stack arrays in sequence depth wise (along third dimension).
    concatenate : Join a sequence of arrays along an existing axis.
    vsplit : Split array into a list of multiple sub-arrays vertically.
    block : Assemble arrays from blocks.

    Examples
    --------
    >>> a = np.array([1, 2, 3])
    >>> b = np.array([2, 3, 4])
    >>> np.vstack((a,b))
    array([[1, 2, 3],
           [2, 3, 4]])

    >>> a = np.array([[1], [2], [3]])
    >>> b = np.array([[2], [3], [4]])
    >>> np.vstack((a,b))
    array([[1],
           [2],
           [3],
           [2],
           [3],
           [4]])

    """
    return _nx.concatenate([atleast_2d(_m) for _m in tup], 0)

def hstack(tup):
    """
    Stack arrays in sequence horizontally (column wise).

    This is equivalent to concatenation along the second axis, except for 1-D
    arrays where it concatenates along the first axis. Rebuilds arrays divided
    by `hsplit`.

    This function makes most sense for arrays with up to 3 dimensions. For
    instance, for pixel-data with a height (first axis), width (second axis),
    and r/g/b channels (third axis). The functions `concatenate`, `stack` and
    `block` provide more general stacking and concatenation operations.

    Parameters
    ----------
    tup : sequence of ndarrays
        The arrays must have the same shape along all but the second axis,
        except 1-D arrays which can be any length.

    Returns
    -------
    stacked : ndarray
        The array formed by stacking the given arrays.

    See Also
    --------
    stack : Join a sequence of arrays along a new axis.
    vstack : Stack arrays in sequence vertically (row wise).
    dstack : Stack arrays in sequence depth wise (along third axis).
    concatenate : Join a sequence of arrays along an existing axis.
    hsplit : Split array along second axis.
    block : Assemble arrays from blocks.

    Examples
    --------
    >>> a = np.array((1,2,3))
    >>> b = np.array((2,3,4))
    >>> np.hstack((a,b))
    array([1, 2, 3, 2, 3, 4])
    >>> a = np.array([[1],[2],[3]])
    >>> b = np.array([[2],[3],[4]])
    >>> np.hstack((a,b))
    array([[1, 2],
           [2, 3],
           [3, 4]])

    """
    arrs = [atleast_1d(_m) for _m in tup]
    # As a special case, dimension 0 of 1-dimensional arrays is "horizontal"
    if arrs and arrs[0].ndim == 1:
        return _nx.concatenate(arrs, 0)
    else:
        return _nx.concatenate(arrs, 1)


def stack(arrays, axis=0, out=None):
    """
    Join a sequence of arrays along a new axis.

    The `axis` parameter specifies the index of the new axis in the dimensions
    of the result. For example, if ``axis=0`` it will be the first dimension
    and if ``axis=-1`` it will be the last dimension.

    .. versionadded:: 1.10.0

    Parameters
    ----------
    arrays : sequence of array_like
        Each array must have the same shape.
    axis : int, optional
        The axis in the result array along which the input arrays are stacked.
    out : ndarray, optional
        If provided, the destination to place the result. The shape must be
        correct, matching that of what stack would have returned if no
        out argument were specified.

    Returns
    -------
    stacked : ndarray
        The stacked array has one more dimension than the input arrays.

    See Also
    --------
    concatenate : Join a sequence of arrays along an existing axis.
    split : Split array into a list of multiple sub-arrays of equal size.
    block : Assemble arrays from blocks.

    Examples
    --------
    >>> arrays = [np.random.randn(3, 4) for _ in range(10)]
    >>> np.stack(arrays, axis=0).shape
    (10, 3, 4)

    >>> np.stack(arrays, axis=1).shape
    (3, 10, 4)

    >>> np.stack(arrays, axis=2).shape
    (3, 4, 10)

    >>> a = np.array([1, 2, 3])
    >>> b = np.array([2, 3, 4])
    >>> np.stack((a, b))
    array([[1, 2, 3],
           [2, 3, 4]])

    >>> np.stack((a, b), axis=-1)
    array([[1, 2],
           [2, 3],
           [3, 4]])

    """
    arrays = [asanyarray(arr) for arr in arrays]
    if not arrays:
        raise ValueError('need at least one array to stack')

    shapes = set(arr.shape for arr in arrays)
    if len(shapes) != 1:
        raise ValueError('all input arrays must have the same shape')

    result_ndim = arrays[0].ndim + 1
    axis = normalize_axis_index(axis, result_ndim)

    sl = (slice(None),) * axis + (_nx.newaxis,)
    expanded_arrays = [arr[sl] for arr in arrays]
    return _nx.concatenate(expanded_arrays, axis=axis, out=out)

import functools
import operator

def _block_format_index(index):
    """
    Convert a list of indices ``[0, 1, 2]`` into ``"arrays[0][1][2]"``.
    """
    idx_str = ''.join('[{}]'.format(i) for i in index if i is not None)
    return 'arrays' + idx_str


def _block_info_recursion(arrays, depth=0, parent_index=()):
    """
    Recursive function checking that the depths of nested lists in `arrays`
    all match. Mismatch raises a ValueError as described in the block
    docstring below.

    It also returns the shape of the final array, along with a list
    of slices and a slice of arrays that can be used for assignment inside the
    new array

    The entire index (rather than just the depth) needs to be calculated
    for each innermost list, in case an error needs to be raised, so that
    the index of the offending list can be printed as part of the error.

    Parameters
    ----------
    arrays : nested list of arrays
        The arrays to check
    parent_index : list of int
        The full index of `arrays` within the nested lists passed to
        `_block_info_recursion` at the top of the recursion.

    Returns
    -------
    first_index : list of int
        The full index of an element from the bottom of the nesting in
        `arrays`. If any element at the bottom is an empty list, this will
        refer to it, and the last index along the empty axis will be `None`.
    shape : tuple of int
        The shape that the final array will take on.
    slices: list of slices
        The slices into the full array required for assignment. These are
        required to be prepended with ``(Ellipsis, )`` to obtain to correct
        final index.
    arrays: list of ndarray
        The data to assign to each slice of the full array
    dtype: dtype
        The dtype of the resulting array.
    ndim: int
        Cache computation of the number of dimensions for the final array.

    """
    if isinstance(arrays, tuple):
        # not strictly necessary, but saves us from:
        #  - more than one way to do things - no point treating tuples like
        #    lists
        #  - horribly confusing behaviour that results when tuples are
        #    treated like ndarray
        raise TypeError(
            '{} is a tuple. '
            'Only lists can be used to arrange blocks, and np.block does '
            'not allow implicit conversion from tuple to ndarray.'.format(
                _block_format_index(parent_index)
            )
        )
    elif isinstance(arrays, list):
        if len(arrays) > 0:
            list_indices, shapes, slices, arrays, dtype, ndim_min = zip(
                    *[_block_info_recursion(arr, depth+1, parent_index + (i,))
                      for i, arr in enumerate(arrays)]
                )
            first_index = list_indices[0]
            list_ndim = len(first_index)
            if any([len(index) != list_ndim for index in list_indices]):
                for index in list_indices[1:]:
                    if len(index) != list_ndim:
                        raise ValueError(
                            "List depths are mismatched. First element was at depth "
                            "{}, but there is an element at depth {} ({})".format(
                            len(first_index),
                            len(index),
                            _block_format_index(index)
                            )
                        )

            if None in (index[-1] for index in list_indices):
                # propagate our flag that indicates an empty list at the bottom
                bad_index = [index[-1] for index in list_indices].index(None)
                return list_indices[bad_index], None, None, None, None, None

            result_ndim = max(ndim_min)
            # Axis where we will concatenate
            axis = result_ndim - list_ndim + depth
            # Broadcast the shapes to the required dim
            # Concatenating tuples is expensive, don't do it if you don't have to
            shapes = [shape if ndim == result_ndim else (1,) * (result_ndim - ndim) + shape
                      for shape, ndim in zip(shapes, ndim_min)]
            # concatenate the shapes along the desired axis
            shape, shape_on_axis = _concatenate_shapes(shapes, axis)

            # `slices` and `arrays` contain lists that have the information
            # from the inner lists provided to the concatenation function.
            # To create the correct offset, one needs to prepend the appropriate
            # offset to each of them. Each list (containing one or more arrays)
            # will require the matching offset (computed above with accumulate)
            slice_prefixes = _concatenate_as_slices(shape_on_axis)
            # Prepend the slice prefix and flatten the slices
            slices = [slice_prefix + the_slice
                      for slice_prefix, inner_slices in zip(slice_prefixes, slices)
                      for the_slice in inner_slices]

            # Flatten the arrays
            arrays = functools.reduce(operator.add, arrays)
            dtype = _nx.result_type(*dtype)

            return first_index, shape, slices, arrays, dtype, result_ndim
        else:  # len == 0
            # We've 'bottomed out' on an empty list
            # It doesn't mater what we return for shape, slices, arrays
            # they are all ignored because of the flag [None] at the
            # end of the parent_index
            return parent_index + (None,), None, None, None, None, None
    else:
        # Base case
        # cast as array
        arr = array(arrays, copy=False, subok=True)
        # We don't know the number of dimensions yet, but we know it is at
        # least this many
        ndim_min = max(len(parent_index), arr.ndim)
        # Return the slice and the array inside a list to be consistent with
        # the recursive case.
        return parent_index, (1,) * (ndim_min - arr.ndim) + arr.shape, [()], [arr], arr.dtype, ndim_min

def _concatenate_shapes(shapes, axis):
    """Given array shapes, return the resulting shape that would occur
    after array concatenation.

    concatenate(arrs, axis).shape == _concatenate_shapes([a.shape for a in arrs], axis)
    """
    # Take a shape, any shape

    shape_on_axis = [shape[axis] for shape in shapes]
    # shape_on_axis, shape_off_axis = zip(*[(shape[axis], shape[:axis] + shape[axis+1:])
    #                                       for shape in shapes])
    first_shape = shapes[0]
    first_shape_pre = first_shape[:axis]
    if any(shape[:axis] !=  first_shape_pre for shape in shapes):
        raise ValueError('Mismatched array shapes in block.')
    return (first_shape_pre + (sum(shape_on_axis),) + first_shape[axis+1:]), shape_on_axis


def _atleast_nd(a, ndim):
    # Ensures `a` has at least `ndim` dimensions by prepending
    # ones to `a.shape` as necessary
    return array(a, ndmin=ndim, copy=False, subok=True)


def _accumulate(values):
    # Helper function because Python 2.7 doesn't have
    # itertools.accumulate
    value = 0
    accumulated = []
    for v in values:
        value += v
        accumulated.append(value)

    return tuple(accumulated)


def _concatenate_as_slices(shape_on_axis):
    """
    Produce the slices that match the destination each array would end up
    along axis.

    For the following situation::

        ret = concatenate([a, b, c], axis=0)
        sl_a, sl_b, sl_c = concatenate_slices([a, b, c], axis=0)

    The result will be that ``ret[sl_a] == a``, ``ret[sl_b] == b``, and
    ``ret[sl_c] == c``.
    Similar properties hold for other values of ``axis``.

    """
    offsets = (0,) + _accumulate(shape_on_axis[:-1])
    return [(slice(offset, offset + shape),)
            for offset, shape in zip(offsets, shape_on_axis)]


def block(arrays):
    """
    Assemble an nd-array from nested lists of blocks.

    Blocks in the innermost lists are concatenated (see `concatenate`) along
    the last dimension (-1), then these are concatenated along the
    second-last dimension (-2), and so on until the outermost list is reached.

    Blocks can be of any dimension, but will not be broadcasted using the normal
    rules. Instead, leading axes of size 1 are inserted, to make ``block.ndim``
    the same for all blocks. This is primarily useful for working with scalars,
    and means that code like ``np.block([v, 1])`` is valid, where
    ``v.ndim == 1``.

    When the nested list is two levels deep, this allows block matrices to be
    constructed from their components.

    .. versionadded:: 1.13.0

    Parameters
    ----------
    arrays : nested list of array_like or scalars (but not tuples)
        If passed a single ndarray or scalar (a nested list of depth 0), this
        is returned unmodified (and not copied).

        Elements shapes must match along the appropriate axes (without
        broadcasting), but leading 1s will be prepended to the shape as
        necessary to make the dimensions match.

    Returns
    -------
    block_array : ndarray
        The array assembled from the given blocks.

        The dimensionality of the output is equal to the greatest of:
        * the dimensionality of all the inputs
        * the depth to which the input list is nested

    Raises
    ------
    ValueError
        * If list depths are mismatched - for instance, ``[[a, b], c]`` is
          illegal, and should be spelt ``[[a, b], [c]]``
        * If lists are empty - for instance, ``[[a, b], []]``

    See Also
    --------
    concatenate : Join a sequence of arrays together.
    stack : Stack arrays in sequence along a new dimension.
    hstack : Stack arrays in sequence horizontally (column wise).
    vstack : Stack arrays in sequence vertically (row wise).
    dstack : Stack arrays in sequence depth wise (along third dimension).
    vsplit : Split array into a list of multiple sub-arrays vertically.

    Notes
    -----

    When called with only scalars, ``np.block`` is equivalent to an ndarray
    call. So ``np.block([[1, 2], [3, 4]])`` is equivalent to
    ``np.array([[1, 2], [3, 4]])``.

    This function does not enforce that the blocks lie on a fixed grid.
    ``np.block([[a, b], [c, d]])`` is not restricted to arrays of the form::

        AAAbb
        AAAbb
        cccDD

    But is also allowed to produce, for some ``a, b, c, d``::

        AAAbb
        AAAbb
        cDDDD

    Since concatenation happens along the last axis first, `block` is _not_
    capable of producing the following directly::

        AAAbb
        cccbb
        cccDD

    Matlab's "square bracket stacking", ``[A, B, ...; p, q, ...]``, is
    equivalent to ``np.block([[A, B, ...], [p, q, ...]])``.

    Examples
    --------
    The most common use of this function is to build a block matrix

    >>> A = np.eye(2) * 2
    >>> B = np.eye(3) * 3
    >>> np.block([
    ...     [A,               np.zeros((2, 3))],
    ...     [np.ones((3, 2)), B               ]
    ... ])
    array([[ 2.,  0.,  0.,  0.,  0.],
           [ 0.,  2.,  0.,  0.,  0.],
           [ 1.,  1.,  3.,  0.,  0.],
           [ 1.,  1.,  0.,  3.,  0.],
           [ 1.,  1.,  0.,  0.,  3.]])

    With a list of depth 1, `block` can be used as `hstack`

    >>> np.block([1, 2, 3])              # hstack([1, 2, 3])
    array([1, 2, 3])

    >>> a = np.array([1, 2, 3])
    >>> b = np.array([2, 3, 4])
    >>> np.block([a, b, 10])             # hstack([a, b, 10])
    array([1, 2, 3, 2, 3, 4, 10])

    >>> A = np.ones((2, 2), int)
    >>> B = 2 * A
    >>> np.block([A, B])                 # hstack([A, B])
    array([[1, 1, 2, 2],
           [1, 1, 2, 2]])

    With a list of depth 2, `block` can be used in place of `vstack`:

    >>> a = np.array([1, 2, 3])
    >>> b = np.array([2, 3, 4])
    >>> np.block([[a], [b]])             # vstack([a, b])
    array([[1, 2, 3],
           [2, 3, 4]])

    >>> A = np.ones((2, 2), int)
    >>> B = 2 * A
    >>> np.block([[A], [B]])             # vstack([A, B])
    array([[1, 1],
           [1, 1],
           [2, 2],
           [2, 2]])

    It can also be used in places of `atleast_1d` and `atleast_2d`

    >>> a = np.array(0)
    >>> b = np.array([1])
    >>> np.block([a])                    # atleast_1d(a)
    array([0])
    >>> np.block([b])                    # atleast_1d(b)
    array([1])

    >>> np.block([[a]])                  # atleast_2d(a)
    array([[0]])
    >>> np.block([[b]])                  # atleast_2d(b)
    array([[1]])


    """
    bottom_index, shape, slices, arrs, dtype, _ = _block_info_recursion(arrays)
    if bottom_index and bottom_index[-1] is None:
        raise ValueError(
            'List at {} cannot be empty'.format(
                _block_format_index(bottom_index)
            )
        )
    result = _nx.empty(shape=shape, dtype=dtype)
    for the_slice, arr in zip(slices, arrs):
        result[(Ellipsis,) + the_slice] = arr
    return result
