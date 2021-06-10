# include parent path
import os
import sys
import numpy as np
import math
import ctypes

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import oglang as og

og.init()
og.config.verify_cuda = True

@og.kernel
def test_rename(n: int):

    a = 0
    b = 1

    a = b
    a = 2

    og.expect_eq(a, 2)
    og.expect_eq(b, 1)

@og.kernel
def test_inplace(n: int):

    a = 1.0
    
    a += 2.0
    
    og.expect_eq(a, 3.0)

@og.kernel
def test_constant(c: float):

    a = 0.0
    a = c + 1.0

    og.expect_eq(a, 2.0)

@og.kernel
def test_dynamic_for_rename(n: int):

    f0 = int(0.0)
    f1 = int(1.0)

    for i in range(0, n):
        
        f = f0 + f1
        
        f0 = f1
        f1 = f

    og.expect_eq(f1, 89)

@og.kernel
def test_dynamic_for_inplace(n: int):

    a = float(0.0)

    for i in range(0, n):
        a += 1.0

    og.expect_eq(n, 10)



device = "cpu"

print("test_inplace")
og.launch(test_inplace, dim=1, inputs=[], device=device)

print("test_rename")
og.launch(test_rename, dim=1, inputs=[], device=device)

print("test_constant")
og.launch(test_constant, dim=1, inputs=[1.0], device=device)

print("test_dynamic_for_rename")
og.launch(test_dynamic_for_rename, dim=1, inputs=[10], device=device)

print("test_dynamic_for_inplace")
og.launch(test_dynamic_for_inplace, dim=1, inputs=[10], device=device)


# print("transform_vec3")
# og.launch(transform_vec3, dim=n, inputs=[dest, m, c], device=device)
# print(dest)


