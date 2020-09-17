//===--- dppl_sycl_usm_interface.cpp - DPPL-SYCL interface --*- C++ -*---===//
//
//               Python Data Parallel Processing Library (PyDPPL)
//
// Copyright 2020 Intel Corporation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
//===----------------------------------------------------------------------===//
///
/// \file
/// TODO
///
//===----------------------------------------------------------------------===//

#include "dppl_sycl_usm_interface.h"
#include "Support/CBindingWrapping.h"

#include <CL/sycl.hpp>                /* SYCL headers   */

using namespace cl::sycl;

// TODO: move it to one header for not duplicate in many cpp files
namespace
{
// Create wrappers for C Binding types (see CBindingWrapping.h).
 DEFINE_SIMPLE_CONVERSION_FUNCTIONS(queue, DPPLSyclQueueRef)
 DEFINE_SIMPLE_CONVERSION_FUNCTIONS(void, DPPLMemoryUSMSharedRef)

} /* end of anonymous namespace */

__dppl_give DPPLMemoryUSMSharedRef
DPPLmalloc_shared (size_t size, __dppl_keep const DPPLSyclQueueRef QRef)
{
    auto Q = unwrap(QRef);
    auto Ptr = malloc_shared(size, *Q);
    return reinterpret_cast<DPPLMemoryUSMSharedRef>(Ptr);
}

void DPPLfree (DPPLMemoryUSMSharedRef MRef, __dppl_keep const DPPLSyclQueueRef QRef)
{
    auto Ptr = unwrap(MRef);
    auto Q = unwrap(QRef);
    free(Ptr, *Q);
}
