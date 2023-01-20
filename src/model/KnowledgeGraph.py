from model.KnownEntity import KnownEntity
from model.KnownRelationship import KnownRelationship


class KnowledgeGraph:

    def __init__(self):
        self.entity_1: KnownEntity = None
        self.entity_2: KnownEntity = None
        self.relationship: KnownRelationship = None

    def add(self, entity_1, relationship, entity_2):
        self.relationship = relationship

    def get_relationship(self, entity_1, entity_2):
        return self.relationship
