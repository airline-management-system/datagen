from enum import Enum, auto
from datetime import datetime, timedelta
import random
from typing import Dict, Any, List
from fake import DatagenFaker
from mergedeep import merge, Strategy
import airportsdata
from geopy.distance import geodesic

# Group airports in turkey by city
tr_airports = {iata: data for iata, data in airportsdata.load('IATA').items()  if data['country'] == 'TR' and iata in {'ADB', 'IST', 'SAW', 'AYT', 'COV', 'ESB'}}
airports_by_city = {}
for airport_data in tr_airports.values():
    city = airport_data['city']
    if city not in airports_by_city:
        airports_by_city[city] = []
    airports_by_city[city].append(airport_data)

def get_two_airports_in_distinct_cities_in_turkey() -> tuple[str, str]:
    # Get list of cities that have airports
    cities = list(airports_by_city.keys())

    assert len(cities) > 2

    # Randomly select two different cities
    city1, city2 = random.sample(cities, 2)

    # Randomly select one airport from each city
    airport1 = random.choice(airports_by_city[city1])
    airport2 = random.choice(airports_by_city[city2])

    return airport1['iata'], airport2['iata']

def calculate_flight_distance(departure_airport: str, arrival_airport: str) -> geodesic:
    if departure_airport not in tr_airports or arrival_airport not in tr_airports:
        raise ValueError("Invalid airport IATA code")

    # Get airport coordinates
    dep = tr_airports[departure_airport]
    arr = tr_airports[arrival_airport]

    # Create coordinate tuples
    dep_coords = (dep['lat'], dep['lon'])
    arr_coords = (arr['lat'], arr['lon'])

    # Calculate distance in kilometers
    return geodesic(dep_coords, arr_coords)

def calculate_flight_duration(departure_airport: str, arrival_airport: str, cruising_kmh: float = 920.0, fixed_time: float = timedelta(minutes=45)) -> timedelta:
    distance = calculate_flight_distance(departure_airport, arrival_airport)
    airtime = timedelta(hours=(distance.kilometers / cruising_kmh))
    return airtime + fixed_time

def calculate_flight_price(departure_airport: str, arrival_airport: str, base_price: float = 100.0, price_per_km: float = 5.52) -> float:
    # Calculate distance
    distance = calculate_flight_distance(departure_airport, arrival_airport)

    # Calculate price: base_price + (distance * price_per_km)
    price = base_price + (distance.kilometers * price_per_km)

    # Round to 2 decimal places
    return round(price, 2)

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
            "password": "123",
            "title": self.fake.title(),
            "role": self.fake.role(),
        }

    def _create_flight(self) -> Dict[str, Any]:
        """Create a flight entity with fake data matching the schema."""
        departure_airport, destination_airport = get_two_airports_in_distinct_cities_in_turkey()
        flight_duration = calculate_flight_duration(departure_airport, destination_airport)
        price = calculate_flight_price(departure_airport, destination_airport)
        departure_datetime = self.fake.departure_datetime()
        arrival_datetime = departure_datetime + flight_duration

        return {
            'flight_number': self.fake.unique.flight_number(),
            'departure_airport': departure_airport,
            'destination_airport': destination_airport,
            'departure_datetime': self._format_datetime(departure_datetime),
            'arrival_datetime': self._format_datetime(arrival_datetime),
            'departure_gate_number': self.fake.gate_number(),
            'destination_gate_number': self.fake.gate_number(),
            'plane_registration': self.fake.unique.plane_registration(),
            'price': price,
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
                'birth_date': self.fake.birth_date().strftime('%Y-%m-%d'),
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
            'model': '787',
            'manufacturer': 'Boeing',
            'capacity': 270,
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
