#!/usr/bin/env python

# enable some python3 compatibility options:
# (unicode_literals not compatible with python2 uuid module)
from __future__ import absolute_import, print_function

import uuid
import unittest

# module being tested:
import scheduler_request_manager.common as common

TEST_UUID_STR = '01234567-89ab-cdef-0123-456789abcdef'
TEST_UUID = uuid.UUID(TEST_UUID_STR)

class TestCommonModule(unittest.TestCase):
    """Unit tests for scheduler request manager common module.

    These tests do not require a running ROS core.
    """

    def test_feedback_default_topic(self):
        self.assertEqual(common.feedback_topic(TEST_UUID),
                         common.SCHEDULER_TOPIC + '_' + TEST_UUID_STR)

    def test_feedback_topic(self):
        topic = common.feedback_topic(TEST_UUID, scheduler_topic='xxx')
        self.assertEqual(topic, 'xxx_' + TEST_UUID_STR)

if __name__ == '__main__':
    import rosunit
    rosunit.unitrun('scheduler_request_manager_common',
                    'test_common_module',
                    TestCommonModule)
