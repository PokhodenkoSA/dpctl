##===---------- test_sycl_queue_manager.py - dpctl  -------*- Python -*----===##
##
##                      Data Parallel Control (dpCtl)
##
## Copyright 2020 Intel Corporation
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##    http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
##===----------------------------------------------------------------------===##
###
### \file
### Defines unit test cases for the SyclQueue.memcpy in sycl_core.pyx.
##===----------------------------------------------------------------------===##

import dpctl
import unittest



class TestQueueMemcpy (unittest.TestCase):

    def _create_memory (self):
        nbytes = 1024
        queue = dpctl.get_current_queue()
        mobj = dpctl._memory.MemoryUSMShared(nbytes, queue)
        return mobj

    def test_memcpy_copy_usm_to_usm (self):
        mobj1 = self._create_memory()
        mobj2 = self._create_memory()
        q = dpctl.get_current_queue()

        mv1 = memoryview(mobj1)
        mv2 = memoryview(mobj2)

        mv1[:3] = b'123'

        q.memcpy(mobj2, mobj1, 3)

        self.assertEqual(mv2[:3], b'123')

    def test_memcpy_type_error (self):
        mobj = self._create_memory()
        q = dpctl.get_current_queue()

        with self.assertRaises(TypeError) as cm:
            q.memcpy(None, mobj, 3)

        self.assertEqual(type(cm.exception), TypeError)
        self.assertEqual(str(cm.exception), "Parameter dest should be Memory.")

        with self.assertRaises(TypeError) as cm:
            q.memcpy(mobj, None, 3)

        self.assertEqual(type(cm.exception), TypeError)
        self.assertEqual(str(cm.exception), "Parameter src should be Memory.")

    def test_memcpy_device_loop (self):
        q = dpctl.get_current_queue()
        nbytes = 1024
        m_host1 = dpctl._memory.MemoryUSMShared(nbytes, q)
        m_device = dpctl._memory.MemoryUSMShared(nbytes, q)
        m_host2 = dpctl._memory.MemoryUSMShared(nbytes, q)

        memoryview(m_host1)[:5] = b"hello"
        q.memcpy(m_device, m_host1, nbytes)
        q.memcpy(m_host2, m_device, nbytes)

        self.assertEqual(memoryview(m_host2)[:5], b'hello')

if __name__ == '__main__':
    unittest.main()
