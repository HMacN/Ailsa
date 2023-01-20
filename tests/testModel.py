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

    def test_knowledge_graph_get_set_relationship(self):
        kg: KnowledgeGraph = KnowledgeGraph()
        entity_1: KnownEntity = KnownEntity()
        entity_2: KnownEntity = KnownEntity()
        given_relationship: KnownRelationship = KnownRelationship()

        kg.add(entity_1, given_relationship, entity_2)
        found_relationship: KnownRelationship = kg.get_relationship(entity_1, entity_2)

        self.assertEqual(given_relationship, found_relationship)

    def test_knowledge_graph_get_set_multiple_relationships(self):
        kg: KnowledgeGraph = KnowledgeGraph()
        entity_1: KnownEntity = KnownEntity()
        entity_2: KnownEntity = KnownEntity()
        entity_3: KnownEntity = KnownEntity()
        relationship_1_2: KnownRelationship = KnownRelationship()
        relationship_1_3: KnownRelationship = KnownRelationship()

        kg.add(entity_1, relationship_1_2, entity_2)
        kg.add(entity_1, relationship_1_3, entity_3)
        found_relationship_1_2: KnownRelationship = kg.get_relationship(entity_1, entity_2)
        found_relationship_1_3: KnownRelationship = kg.get_relationship(entity_1, entity_3)

        self.assertEqual(relationship_1_2, found_relationship_1_2)
        self.assertEqual(relationship_1_3, found_relationship_1_3)

    def test_knowledge_graph_get_set_relationships_with_disordered_entities(self):
        kg: KnowledgeGraph = KnowledgeGraph()
        entity_1: KnownEntity = KnownEntity()
        entity_2: KnownEntity = KnownEntity()
        entity_3: KnownEntity = KnownEntity()
        relationship_1_2: KnownRelationship = KnownRelationship()
        relationship_1_3: KnownRelationship = KnownRelationship()

        kg.add(entity_1, relationship_1_2, entity_2)
        kg.add(entity_1, relationship_1_3, entity_3)
        found_relationship_1_2: KnownRelationship = kg.get_relationship(entity_2, entity_1)
        found_relationship_1_3: KnownRelationship = kg.get_relationship(entity_3, entity_1)

        self.assertEqual(relationship_1_2, found_relationship_1_2)
        self.assertEqual(relationship_1_3, found_relationship_1_3)

    def test_knowledge_graph_get_connected_entities_by_relationship(self):
        kg: KnowledgeGraph = KnowledgeGraph()
        entity_1: KnownEntity = KnownEntity()
        entity_2: KnownEntity = KnownEntity()
        given_relationship: KnownRelationship = KnownRelationship()

        kg.add(entity_1, given_relationship, entity_2)
        found_entity: KnownEntity = kg.get_entity(entity_1, given_relationship)

        self.assertEqual(entity_2, found_entity)
