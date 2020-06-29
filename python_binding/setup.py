#! /usr/bin/env python
#*******************************************************************************
# Copyright 2019-2020x Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#******************************************************************************/
import sys
import numpy as np
import os
import versioneer
from setuptools import setup, Extension
from Cython.Build import cythonize

requirements = [
    'cffi>=1.0.0',
    'cython',
]

IS_WIN = False
IS_MAC = False
IS_LIN = False

if 'linux' in sys.platform:
    IS_LIN = True
elif sys.platform == 'darwin':
    IS_MAC = True
elif sys.platform in ['win32', 'cygwin']:
    IS_WIN = True
else:
    assert False, sys.platform + ' not supported'

dppy_oneapi_interface_lib     = os.environ['DPPY_ONEAPI_INTERFACE_LIBDIR']
dppy_oneapi_interface_include = os.environ['DPPY_ONEAPI_INTERFACE_INCLDIR']
sycl_lib = os.environ['ONEAPI_ROOT']+"\compiler\latest\windows\lib"

def get_sdl_cflags():
    if IS_LIN or IS_MAC:
        return ['-fstack-protector', '-fPIC',
                '-D_FORTIFY_SOURCE=2', '-Wformat', '-Wformat-security',]
    elif IS_WIN:
        return []

def get_sdl_ldflags():
    if IS_LIN:
        return ['-Wl,-z,noexecstack,-z,relro,-z,now',]
    elif IS_MAC:
        return []
    elif IS_WIN:
        return ['/NXCompat', '/DynamicBase']

def get_other_cxxflags():
    if IS_LIN:
        return ['-O3', '-fsycl', '-std=c++17']
    elif IS_MAC:
        return []
    elif IS_WIN:
        # FIXME: These are specific to MSVC and we should first make sure
        # what compiler we are using.
        return ['/Ox', '/std:c++17']

def getpyexts():
    # Security flags
    eca = get_sdl_cflags()
    ela = get_sdl_ldflags()
    libs = []
    librarys = []

    if IS_LIN:
        libs += ['rt', 'DPPYOneapiInterface']
    elif IS_MAC:
        pass
    elif IS_WIN:
        libs += ['DPPYOneapiInterface', 'sycl']

    if IS_LIN:
        librarys = [dppy_oneapi_interface_lib]
    elif IS_WIN:
        librarys = [dppy_oneapi_interface_lib, sycl_lib]
    elif IS_MAC:
        librarys = [dppy_oneapi_interface_lib]

    exts = cythonize(Extension('dppy._oneapi_interface',
                               [os.path.abspath('dppy/oneapi_interface.pyx'),],
                                depends=[dppy_oneapi_interface_include,],
                                include_dirs=[np.get_include(),
                                              dppy_oneapi_interface_include],
                                extra_compile_args=eca + get_other_cxxflags(),
                                extra_link_args=ela,
                                libraries=libs,
                                library_dirs=librarys,
                                language='c++'))
    return exts

setup(
    name='dppy',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="A lightweight Python wrapper for a subset of OpenCL and SYCL API.",
    license="Apache 2.0",
    author="Intel Corporation",
    url='https://github.intel.com/SAT/dppy',
    packages=['dppy'],
    ext_modules = getpyexts(),
    setup_requires=requirements,
    #cffi_modules=[
    #    "./dppy/driverapi.py:ffi"
    #],
    install_requires=requirements,
    keywords='dppy',
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
