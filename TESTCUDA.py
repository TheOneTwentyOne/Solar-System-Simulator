import numpy as np
import cupy as cp
import math
import sys
import random
import time
from cupyx.scipy import fft as fft_gpu
from scipy import fft


array_cpu = np.random.uniform(-1E10, 1E10, size=(4000, 4000))
#print(array_cpu.nbytes/1E6)
array_gpu = cp.asarray(array_cpu)



st = time.perf_counter()
#fft.fftn(array_cpu)
fft_gpu.fftn(array_gpu)
en = time.perf_counter()
print(en-st)













#st = time.perf_counter()
#en = time.perf_counter()

#print(en-st)

