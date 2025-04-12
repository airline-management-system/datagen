from enum import Enum, auto
from faker import Faker
from datetime import datetime, timedelta
import random
from typing import Dict, Any, List

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
        """Initialize the factory with Turkish locale."""
        self.fake = Faker('tr_TR')
    
    def create_entity(self, entity_type: Entity) -> Dict[str, Any]:
        """Create an entity of the specified type with fake data."""
        factory_method = self._get_factory_method(entity_type)
        return factory_method()

    def create_entities(self, entity_type: Entity, amount: int) -> List[Dict[str, Any]]:
        """Create an entity of the specified type with fake data."""
        factory_method = self._get_factory_method(entity_type)
        return [factory_method() for _ in range(0, amount)]

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
        """Create an employee entity with fake data matching the database schema."""
        now = datetime.now()
        
        return {
            'id': random.randint(1, 1000),
            'employee_id': self.fake.uuid4(),
            'name': self.fake.first_name(),
            'surname': self.fake.last_name(),
            'email': self.fake.email(),
            'phone': self.fake.phone_number()[:15],
            'address': self.fake.address(),
            'gender': random.choice(['male', 'female']),  # Matches gender_enum
            'birth_date': self.fake.date_of_birth(minimum_age=18, maximum_age=65).isoformat(),
            'hire_date': self.fake.date_between(start_date='-10y', end_date='today').isoformat(),
            'position': self.fake.job(),
            'role': random.choice(['hr', 'admin', 'flight_planner', 'passenger_services', 'ground_services']),  # Matches role_enum
            'salary': round(random.uniform(30000, 150000), 2),
            'status': random.choice(['active', 'inactive']),  # Matches status_enum
            'manager_id': random.randint(1, 100) if random.choice([True, False]) else None,
            'emergency_contact': self.fake.name(),
            'emergency_phone': self.fake.phone_number()[:15],
            'profile_image_url': self.fake.image_url(),
            'created_at': now.isoformat(),
            'updated_at': now.isoformat(),
            'password_hash': self.fake.sha256(),
            'salt': self.fake.sha1()
        }
    
    def _create_flight(self) -> Dict[str, Any]:
        """Create a flight entity with fake data matching the schema."""
        departure_time = self.fake.future_datetime(end_date='+30d')
        flight_duration = timedelta(hours=random.randint(1, 12))
        
        return {
            'flight_number': f"{random.choice(['TK', 'PC', 'XQ', 'J2'])}{random.randint(100, 9999)}",  # Turkish airlines codes
            'departure_airport': random.choice(['IST', 'SAW', 'ESB', 'AYT', 'ADB']),  # Major Turkish airports
            'destination_airport': random.choice(['LHR', 'CDG', 'FRA', 'JFK', 'DXB']),  # International airports
            'departure_datetime': departure_time.isoformat(),
            'arrival_datetime': (departure_time + flight_duration).isoformat(),
            'departure_gate_number': f"{random.choice(['A', 'B', 'C', 'D'])}{random.randint(1, 30)}",
            'destination_gate_number': f"{random.choice(['A', 'B', 'C', 'D'])}{random.randint(1, 30)}",
            'plane_registration': f"TC-{self.fake.bothify(text='???').upper()}",  # Turkish aircraft registration
            'status': random.choice(['scheduled', 'delayed', 'cancelled', 'departed', 'arrived']),  # Matches flight_status_enum
            'price': round(random.uniform(100, 2000), 2)
        }
    
    def _create_passenger(self) -> Dict[str, Any]:
        """Create a passenger entity with fake data."""
        return {
            'national_id': self.fake.ssn(),  # Will generate Turkish national ID numbers
            'pnr_no': self.fake.bothify(text='??????'),
            'flight_id': random.randint(1, 1000),
            'payment_id': random.randint(1, 1000),
            'baggage_allowance': random.randint(0, 3),
            'baggage_id': self.fake.bothify(text='??########'),
            'fare_type': random.choice(['economy', 'business', 'first']),
            'seat': random.randint(1, 300),
            'meal': random.choice(['vegetarian', 'non-vegetarian', 'vegan', 'halal', 'kosher']),
            'extra_baggage': random.randint(0, 2),
            'check_in': random.choice([True, False]),
            'name': self.fake.first_name(),
            'surname': self.fake.last_name(),
            'email': self.fake.email(),
            'phone': self.fake.phone_number(),  # Will generate Turkish phone numbers
            'gender': random.choice(['male', 'female']),
            'birth_date': self.fake.date_of_birth(minimum_age=1, maximum_age=100),
            'cip_member': random.choice([True, False]),
            'vip_member': random.choice([True, False]),
            'disabled': random.choice([True, False]),
            'child': random.choice([True, False])
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
            'registration': f"TC-{random.randint(10000, 99999)}",  # Turkish aircraft registration prefix
            'model': random.choice(['737', '747', '777', '787', 'A320', 'A330', 'A350', 'A380']),
            'manufacturer': random.choice(['Boeing', 'Airbus']),
            'capacity': random.randint(100, 500),
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
            'phone': self._generate_phone_number(),
            'gender': random.choice(['male', 'female']),
            'birth_date': self._format_datetime(self.fake.date_time_between(start_date='-100y', end_date='-18y')),
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

    def _generate_phone_number(self) -> str:
        """Generate a phone number in the format +905XXXXXXXX."""
        return f"+905{random.randint(10000000, 99999999)}"
