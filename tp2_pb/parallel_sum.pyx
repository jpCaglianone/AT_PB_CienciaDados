
from cython.parallel cimport prange
import cython

@cython.boundscheck(False)
@cython.wraparound(False)
def parallel_sum(int[:] arr):
    cdef long total = 0
    cdef int i
    for i in prange(arr.shape[0], nogil=True, schedule='static'):
        total += arr[i]
    return total
