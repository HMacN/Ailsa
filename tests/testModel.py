import unittest

from model.KnownRelationship import KnownRelationship
from model.KnownEntity import KnownEntity
from model.KnowledgeGraph import KnowledgeGraph
from mocks.MockController import MockController
from model.Model import Model


class ModelTests(unittest.TestCase):

    def test_get_set_controller(self):
        controller = MockController()
        model = Model(controller)

        self.assertEqual(controller, model.get_controller())

