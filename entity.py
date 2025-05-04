from enum import Enum, auto
from datetime import datetime, timedelta
import random
from typing import Dict, Any, List
from fake import DatagenFaker

class Entity(Enum):
    BANK = auto()
    EMPLOYEE = auto()
    FLIGHT = auto()
    PASSENGER = auto()
    PAYMENT = auto()
    PLANE = auto()
    REFUND = auto()
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
        return {**entity_data, **kwargs}

    def create_entities(self, entity_type: Entity, amount: int, **kwargs) -> List[Dict[str, Any]]:
        """Create an entity of the specified type with fake data."""
        factory_method = self._get_factory_method(entity_type)
        return [{**factory_method(), **kwargs} for _ in range(0, amount)]

    def _get_factory_method(self, entity_type: Entity):
        """Return the corresponding factory method for entity type."""
        factory_map = {
            Entity.BANK: self._create_bank,
            Entity.EMPLOYEE: self._create_employee,
            Entity.FLIGHT: self._create_flight,
            Entity.PASSENGER: self._create_passenger,
            Entity.PAYMENT: self._create_payment,
            Entity.PLANE: self._create_plane,
            Entity.REFUND: self._create_refund,
            Entity.USER: self._create_user
        }

        factory_method = factory_map.get(entity_type)

        if factory_method is None:
            raise ValueError(f"No factory method found for entity type: {entity_type.name}")
            
        return factory_method
    
    def _create_bank(self) -> Dict[str, Any]:
        """Create a bank entity with fake data matching the Go struct."""
        card_type = random.choice(['visa', 'mastercard'])
        card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
        cvv = ''.join([str(random.randint(0, 9)) for _ in range(3)])
        
        return {
            'id': self.fake.uuid4(),
            'card_number': card_number,
            'card_holder_name': self.fake.first_name(),
            'card_holder_surname': self.fake.last_name(),
            'expiration_month': random.randint(1, 12),
            'expiration_year': datetime.now().year + random.randint(1, 5),
            'cvv': cvv,
            'card_type': card_type,
            'amount': round(random.uniform(1000, 100000), 2),
            'currency': 'TRY',
            'issuer_bank': self.fake.company(),
            'status': random.choice(['active', 'inactive']),
            'created_at': datetime.now().isoformat()
        }
    
    def _create_employee(self) -> Dict[str, Any]:
        """Create an employee entity with fake data matching the specified format."""
        return {
            "national_id": self.fake.ssn(),
            "name": self.fake.first_name(),
            "surname": self.fake.last_name(),
            "email": self.fake.email(),
            "phone": self.fake.phone_number(),
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
            'flight_number': self.fake.flight_number(),
            'departure_airport': departure_airport,
            'destination_airport': destination_airport,
            'departure_datetime': self._format_datetime(departure_time),
            'arrival_datetime': self._format_datetime(departure_time + flight_duration),
            'departure_gate_number': self.fake.gate_number(),
            'destination_gate_number': self.fake.gate_number(),
            'plane_registration': self.fake.plane_registration(),
            'status': self.fake.flight_status(),
            'price': self.fake.flight_price()
        }
    
    def _create_passenger(self) -> Dict[str, Any]:
        """Create a passenger entity with fake data."""
        return {
            'national_id': self.fake.ssn(),
            'pnr_no': self.fake.pnr(),
            'flight_id': self.fake.flight_id(),
            'payment_id': self.fake.payment_id(),
            'baggage_allowance': self.fake.baggage_allowance(),
            'baggage_id': self.fake.baggage_id(),
            'fare_type': self.fake.fare_type(), 
            'seat': self.fake.seat_number(),
            'meal': self.fake.meal(),
            'extra_baggage': self.fake.extra_baggage(),
            'check_in': self.fake.boolean(),
            'name': self.fake.first_name(),
            'surname': self.fake.last_name(),
            'email': self.fake.email(),
            'phone': self.fake.phone_number(),
            'gender': self.fake.gender(), 
            'birth_date': self._format_datetime(self.fake.birth_date()),
            'cip_member': False,
            'vip_member': False,
            'disabled': False,
            'child': False
        }
    
    def _create_payment(self) -> Dict[str, Any]:
        """Create a payment entity with fake data."""
        return {
            'payment_id': self.fake.uuid4(),
            'user_id': self.fake.uuid4(),
            'amount': round(random.uniform(10, 5000), 2),
            'currency': 'TRY',  # Changed to Turkish Lira
            'payment_method': random.choice(['credit_card', 'debit_card', 'bank_transfer', 'paypal']),
            'status': random.choice(['active', 'inactive'])
        }
    
    def _create_plane(self) -> Dict[str, Any]:
        """Create a plane entity with fake data."""
        return {
            'registration': self.fake.bothify("TC-###"),
            'model': random.choice(['A320', 'A330', 'A350', 'A380']),
            'manufacturer': 'Airbus',
            'capacity': self.fake.random_int(150, 200),
            'status': random.choice(['active', 'inactive'])
        }
    
    def _create_refund(self) -> Dict[str, Any]:
        """Create a refund entity with fake data."""
        return {
            'refund_id': self.fake.uuid4(),
            'payment_id': self.fake.uuid4(),
            'amount': round(random.uniform(10, 5000), 2),
            'currency': 'TRY',
            'reason': self.fake.text(max_nb_chars=200),
            'status': random.choice(['active', 'inactive'])
        }
    
    def _create_user(self) -> Dict[str, Any]:
        """Create a user entity with fake data."""
        now = datetime.now()
        return {
            'name': self.fake.first_name(),
            'surname': self.fake.last_name(),
            'username': self.fake.user_name(),
            'email': self.fake.email(),
            'password_hash': self.fake.sha256(),
            'salt': self.fake.sha1(),
            'phone': self.fake.phone_number(),
            'gender': self.fake.gender(),
            'birth_date': self._format_datetime(self.fake.birth_date()),
            'last_login': self._format_datetime(now),
            'last_password_change': self._format_datetime(now)
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

