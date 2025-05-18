import random
from typing import Iterator, List, Dict, Any
from entity import Entity, EntityFactory
from router import Router
import logging
from collections import defaultdict

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
    NUM_USERS = 1000 
    NUM_CREDITCARDS = NUM_USERS
    NUM_PLANES = 500 
    NUM_FLIGHTS = 5000
    NUM_PASSENGERS = NUM_FLIGHTS

    # NUM_USERS = 1
    # NUM_CREDITCARDS = NUM_USERS
    # NUM_PLANES = 1 
    # NUM_FLIGHTS = 1
    # NUM_PASSENGERS = NUM_FLIGHTS * 100

    def __init__(self, factory: EntityFactory, router: Router):
        super().__init__()
        self.factory = factory
        self.router = router

    def build(self):
        # Create employees
        # yield Entity.EMPLOYEE, self.factory.create_entities(Entity.EMPLOYEE, 0)

        # Create users
        user_overrides = { 'password': '123' }
        users = self.factory.create_entities(Entity.USER, StandardScheme.NUM_USERS, **user_overrides)
        yield Entity.USER, users

        # Create credit cards
        credit_cards = []
        for i in range(0, StandardScheme.NUM_CREDITCARDS):
            credit_card_overrides = { 'card_holder_name': users[i]['name'], 'card_holder_surname': users[i]['surname'] }
            credit_card = self.factory.create_entity(Entity.CREDITCARD, **credit_card_overrides)
            credit_cards.append(credit_card)

        yield Entity.CREDITCARD, credit_cards

        # Create planes
        planes = self.factory.create_entities(Entity.PLANE, StandardScheme.NUM_PLANES)
        yield Entity.PLANE, planes

        # Create flights
        flights = []
        for _ in range(0, StandardScheme.NUM_FLIGHTS):
            flight_overrides = { 'plane_registration': random.choice(planes)['registration'] }
            flight = self.factory.create_entity(Entity.FLIGHT, **flight_overrides)
            flights.append(flight)

        yield Entity.FLIGHT, flights

        # Create passengers
        all_seats = defaultdict(lambda: iter(range(0, 200)))
        passengers = []
        for _ in range(0, StandardScheme.NUM_PASSENGERS):
            credit_card = random.choice(credit_cards)
            flight = random.choice(flights)
            seats = all_seats[flight['flight_number']]
            seat = next(seats)

            passenger_overrides = {
                'passenger': {
                    'flight_number': flight['flight_number'],
                    'seat': seat
                },
                'credit_card': credit_card
            }

            passenger = self.factory.create_entity(Entity.PASSENGER, **passenger_overrides)
            passengers.append(passenger)

        yield Entity.PASSENGER, passengers

    def execute(self) -> None:
        for entity, data in self:
            logging.info(f"Posting {len(data)} number of {entity.name} generated with scheme")
            self.router.post(entity, data)