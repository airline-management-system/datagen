import random
from typing import Iterator, List, Dict, Any
from entity import Entity, EntityFactory
from router import Router
import logging

class BaseScheme:
    def __init__(self):
        self.scheme = self.build()

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.scheme)

    def build(self):
        raise NotImplementedError("Subclasses should implement this method.") 

    def execute(self):
        raise NotImplementedError("Subclasses should implement this method.") 


class StandardScheme(BaseScheme):
    def __init__(self, factory: EntityFactory, router: Router):
        super().__init__()
        self.factory = factory
        self.router = router

    def build(self):
        # yield Entity.USER, self.factory.create_entities(Entity.USER, 0)
        yield Entity.EMPLOYEE, self.factory.create_entities(Entity.EMPLOYEE, 0)

        planes = self.factory.create_entities(Entity.PLANE, 2)
        yield Entity.PLANE, planes

        NUM_FLIGHTS = 4
        flights = []
        for _ in range(0, NUM_FLIGHTS):
            registration = random.choice(planes)['registration']
            flight = self.factory.create_entity(Entity.FLIGHT, plane_registration=registration)
            flights.append(flight)

        yield Entity.FLIGHT, flights

    def execute(self) -> None:
        for entity, data in self:
            logging.info(f"Posting {len(data)} number of {entity.name} generated with scheme")
            self.router.post(entity, data)