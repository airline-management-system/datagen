import argparse
from enum import Enum, auto
from typing import Callable, Dict
import requests
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

class Entity(Enum):
    BANK = auto()
    EMPLOYEE = auto()
    FLIGHT = auto()
    PASSENGER = auto()
    PAYMENT = auto()
    PLANE = auto()
    REFUND = auto()
    REQUEST = auto()
    USER = auto()

    @classmethod
    def from_string(cls, value: str) -> 'Entity':
        try:
            return cls[value.upper()]
        except KeyError:
            raise ValueError(f"Invalid entity: {value}. Must be one of: {', '.join(e.name.lower() for e in cls)}")


# Base URL for the API from environment variables
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8080')


def process_bank(amount: int) -> None:
    """Process bank-related operations with the specified amount."""
    logger.info(f"Processing bank operations with amount {amount}")
    # TODO: Implement bank-specific logic


def process_employee(amount: int) -> None:
    """Process employee-related operations with the specified amount."""
    logger.info(f"Processing employee operations with amount {amount}")
    # TODO: Implement employee-specific logic


def process_flight(amount: int) -> None:
    """Process flight-related operations with the specified amount."""
    logger.info(f"Processing flight operations with amount {amount}")
    # TODO: Implement flight-specific logic


def process_passenger(amount: int) -> None:
    """Process passenger-related operations with the specified amount."""
    logger.info(f"Processing passenger operations with amount {amount}")
    # TODO: Implement passenger-specific logic


def process_payment(amount: int) -> None:
    """Process payment-related operations with the specified amount."""
    logger.info(f"Processing payment operations with amount {amount}")
    # TODO: Implement payment-specific logic


def process_plane(amount: int) -> None:
    """Process plane-related operations with the specified amount."""
    logger.info(f"Processing plane operations with amount {amount}")
    # TODO: Implement plane-specific logic


def process_refund(amount: int) -> None:
    """Process refund-related operations with the specified amount."""
    logger.info(f"Processing refund operations with amount {amount}")
    # TODO: Implement refund-specific logic


def process_request(amount: int) -> None:
    """Process request-related operations with the specified amount."""
    logger.info(f"Processing request operations with amount {amount}")
    # TODO: Implement request-specific logic


def process_user(amount: int) -> None:
    """Process user-related operations with the specified amount."""
    logger.info(f"Processing user operations with amount {amount}")
    # TODO: Implement user-specific logic


# Map each entity to its corresponding processing function
ENTITY_HANDLERS: Dict[Entity, Callable[[int], None]] = {
    Entity.BANK: process_bank,
    Entity.EMPLOYEE: process_employee,
    Entity.FLIGHT: process_flight,
    Entity.PASSENGER: process_passenger,
    Entity.PAYMENT: process_payment,
    Entity.PLANE: process_plane,
    Entity.REFUND: process_refund,
    Entity.REQUEST: process_request,
    Entity.USER: process_user,
}

# Map each entity to its corresponding endpoint URL
ENTITY_ENDPOINTS: Dict[Entity, str] = {
    Entity.BANK: "/banks",
    Entity.EMPLOYEE: "/employees",
    Entity.FLIGHT: "/flights",
    Entity.PASSENGER: "/passengers",
    Entity.PAYMENT: "/payments",
    Entity.PLANE: "/planes",
    Entity.REFUND: "/refunds",
    Entity.REQUEST: "/requests",
    Entity.USER: "/users",
}


def process_entity(entity: Entity, amount: int) -> None:
    """
    Process the given entity with the specified amount by calling the appropriate handler function
    and making an HTTP request to the corresponding endpoint.
    """
    handler = ENTITY_HANDLERS.get(entity)
    if handler is None:
        logger.error(f"No handler found for entity: {entity.name}")
        raise ValueError(f"No handler found for entity: {entity.name}")
    
    # Process the entity using the handler
    handler(amount)
    
    # Get the endpoint for the entity
    endpoint = ENTITY_ENDPOINTS.get(entity)
    if endpoint is None:
        logger.error(f"No endpoint found for entity: {entity.name}")
        raise ValueError(f"No endpoint found for entity: {entity.name}")
    
    # Construct the full URL
    url = f"{BASE_URL}{endpoint}"
    
    try:
        # Make the HTTP request
        response = requests.post(url, json={"amount": amount})
        response.raise_for_status()  # Raise an exception for bad status codes
        logger.info(f"Successfully sent request to {url}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to {url}: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description='Process entities with specified amounts')

    parser.add_argument(
        '-e', '--entity',
        type=str,
        required=True,
        help='Entity to process (bank|employee|flight|passenger|payment|plane|refund|request|user)'
    )

    parser.add_argument(
        '-a', '--amount',
        type=int,
        required=True,
        help='Amount to process'
    )

    args = parser.parse_args()

    try:
        entity = Entity.from_string(args.entity)
        process_entity(entity, args.amount)
    except ValueError as e:
        logger.error(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())