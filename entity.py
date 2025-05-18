from enum import Enum, auto
from datetime import datetime, timedelta
import random
from typing import Dict, Any, List
from fake import DatagenFaker
from mergedeep import merge, Strategy

class Entity(Enum):
    CREDITCARD = auto()
    EMPLOYEE = auto()
    FLIGHT = auto()
    PASSENGER = auto()
    PLANE = auto()
    USER = auto()

    @classmethod
    def from_string(cls, value: str) -> 'Entity':
        try:
            return cls[value.upper()]
        except KeyError:
            raise ValueError(f"Invalid entity: {value}. Must be one of: {', '.join(e.name.lower() for e in cls)}")

class EntityFactory:
    """A factory class for creating different types of entities with fake data."""
    
    def __init__(self):
        """Initialize the factory"""
        self.fake = DatagenFaker()
    
    def create_entity(self, entity_type: Entity, **kwargs) -> Dict[str, Any]:
        """Create an entity of the specified type with fake data."""
        factory_method = self._get_factory_method(entity_type)
        entity_data = factory_method()
        return merge(entity_data, kwargs, strategy = Strategy.REPLACE)

    def create_entities(self, entity_type: Entity, amount: int, **kwargs) -> List[Dict[str, Any]]:
        """Create an entity of the specified type with fake data."""
        factory_method = self._get_factory_method(entity_type)
        return [merge(factory_method(), kwargs, strategy = Strategy.REPLACE) for _ in range(0, amount)]

    def _get_factory_method(self, entity_type: Entity):
        """Return the corresponding factory method for entity type."""
        factory_map = {
            Entity.CREDITCARD: self._create_creditcard,
            Entity.EMPLOYEE: self._create_employee,
            Entity.FLIGHT: self._create_flight,
            Entity.PASSENGER: self._create_passenger,
            Entity.PLANE: self._create_plane,
            Entity.USER: self._create_user
        }

        factory_method = factory_map.get(entity_type)

        if factory_method is None:
            raise ValueError(f"No factory method found for entity type: {entity_type.name}")
            
        return factory_method
    
    def _create_employee(self) -> Dict[str, Any]:
        """Create an employee entity with fake data matching the specified format."""
        return {
            "national_id": self.fake.unique.ssn(),
            "name": self.fake.first_name(),
            "surname": self.fake.last_name(),
            "email": self.fake.unique.email(),
            "phone": self.fake.unique.phone_number(),
            "gender": self.fake.gender(),
            "birth_date": self._format_datetime(self.fake.birth_date()),
            "password": self.fake.password(),
            "title": self.fake.title(),
            "role": self.fake.role(),
        }
    
    def _create_flight(self) -> Dict[str, Any]:
        """Create a flight entity with fake data matching the schema."""
        departure_time = self.fake.future_datetime(end_date='+30d')
        flight_duration = timedelta(hours=random.randint(1, 12))
        departure_airport = self.fake.iata()
        destination_airport = self.fake.iata(exclude=[departure_airport])
        
        return {
            'flight_number': self.fake.unique.flight_number(),
            'departure_airport': departure_airport,
            'destination_airport': destination_airport,
            'departure_datetime': self._format_datetime(departure_time),
            'arrival_datetime': self._format_datetime(departure_time + flight_duration),
            'departure_gate_number': self.fake.gate_number(),
            'destination_gate_number': self.fake.gate_number(),
            'plane_registration': self.fake.unique.plane_registration(),
            'price': self.fake.flight_price()
        }
    
    def _create_passenger(self) -> Dict[str, Any]:
        """Create a passenger entity with fake data."""
        return {
            "passenger": {
                'flight_number': self.fake.flight_number(),
                'fare_type': self.fake.fare_type(), 
                'national_id': self.fake.unique.ssn(),
                'name': self.fake.first_name(),
                'surname': self.fake.last_name(),
                'email': self.fake.unique.email(),
                'phone': self.fake.unique.phone_number(),
                'gender': self.fake.gender(), 
                'disabled': False,
                'seat': self.fake.seat_number(),
                'birth_date': self._format_datetime(self.fake.birth_date()),
                'child': False
            },
            "credit_card": self._create_creditcard(),
        }
    
    def _create_creditcard(self) -> Dict[str, Any]:
        """Create a credit card entity with fake data."""
        return {
            "card_number": self.fake.unique.credit_card_number()[:16],
            "card_type": 'visa',
            "card_holder_name": self.fake.first_name(),
            "card_holder_surname": self.fake.last_name(),
            "expiration_month": random.randint(1, 12),
            "expiration_year": random.randint(28, 40),
            "cvv": self.fake.credit_card_security_code(),
        }
    
    def _create_plane(self) -> Dict[str, Any]:
        """Create a plane entity with fake data."""
        return {
            'registration': self.fake.unique.bothify("TC-###"),
            'model': random.choice(['A320', 'A330', 'A350', 'A380']),
            'manufacturer': 'Airbus',
            'capacity': self.fake.random_int(150, 200),
            'status': random.choice(['active', 'inactive'])
        }

    def _create_user(self) -> Dict[str, Any]:
        """Create a user entity with fake data."""
        now = datetime.now()
        return {
            'name': self.fake.first_name(),
            'surname': self.fake.last_name(),
            'email': self.fake.unique.email(),
            'password': self.fake.password(),
            'phone': self.fake.unique.phone_number(),
            'gender': self.fake.gender(),
            'birth_date': self._format_datetime(self.fake.birth_date()),
        }

    def _format_datetime(self, dt: datetime) -> str:
        """Formats the given datetime to the accepted one by AMS."""
        dt = datetime(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
        )

        return dt.isoformat('T', "seconds") + 'Z'

