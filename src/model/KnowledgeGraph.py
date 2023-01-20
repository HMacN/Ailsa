from model.KnownEntity import KnownEntity
from model.KnownRelationship import KnownRelationship


class KnowledgeGraph:

    def __init__(self):
        self.entity_relationships: dict = dict()

    def add(self, entity_1: KnownEntity, relationship: KnownRelationship, entity_2: KnownEntity):
        entity_set: frozenset = frozenset({entity_1, entity_2})
        self.entity_relationships.update({entity_set: relationship})

    def get_relationship(self, entity_1: KnownEntity, entity_2: KnownEntity) -> KnownRelationship:
        entity_set: frozenset = frozenset({entity_1, entity_2})
        return self.entity_relationships[entity_set]

    def get_entity(self, entity: KnownEntity, relationship: KnownRelationship) -> KnownEntity:
        entity_set_for_relationship: set = self.__get_entity_set_from_one_entity_and_relationship(entity, relationship)

        entity_related_to_given_entity: KnownEntity = \
            self.__get_other_entity_from_two_entity_set(entity_set_for_relationship, entity)

        return entity_related_to_given_entity

    def __get_entity_set_from_one_entity_and_relationship(self, entity: KnownEntity,
                                                          relationship: KnownRelationship) -> set:
        for entities in self.entity_relationships:
            if (entity in entities) & (self.entity_relationships[entities] == relationship):
                return entities

    def __get_other_entity_from_two_entity_set(self, entity_set, entity_not_to_get):
        for entity in entity_set:
            if entity != entity_not_to_get:
                return entity

