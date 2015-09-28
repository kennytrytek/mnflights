import os
from unittest import TestCase

from google.appengine.datastore import datastore_stub_util
from google.appengine.ext import testbed


class DatastoreBaseCase(TestCase):
    testbed = None

    @classmethod
    def _setup_gae(cls):
        cls.testbed = testbed.Testbed()
        cls.testbed.activate()
        cls.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(
            probability=1.0)

        cls.testbed.init_datastore_v3_stub(
            consistency_policy=cls.policy,
            require_indexes=True,
            root_path=os.path.dirname(__file__))

        cls.testbed.init_memcache_stub()
        cls.testbed.init_user_stub()

    @classmethod
    def _teardown_gae(cls):
        cls.testbed.deactivate()


class DatastoreTestCase(DatastoreBaseCase):
    def setUp(self):
        self._setup_gae()
        self.addCleanup(self._teardown_gae)
