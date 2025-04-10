import argparse
import logging
from dotenv import load_dotenv
import os
import json

from entity import Entity, EntityFactory
from router import Router

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

# Base URL for the API from environment variables
BASE_URL = os.getenv('BASE_URL')

factory = EntityFactory()
router = Router(BASE_URL)

def dry_run(entity_type: Entity, amount: int):
    logger.info("Dry run mode - displaying generated data:")
    entities = factory.create_entities(entity_type, amount)
    print(json.dumps(entities, indent=2, ensure_ascii=False))

def run(entity_type: Entity, amount: int) -> None:
    logger.info(f"Generating f{amount} entities of {entity_type}")
    entities = factory.create_entities(entity_type, amount)
    router.post(entity_type, entities)

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

    parser.add_argument(
        '-d', '--dry-run',
        action='store_true',
        help='Generate data without making HTTP requests'
    )

    args = parser.parse_args()

    try:
        entity = Entity.from_string(args.entity)
        if args.dry_run:
            dry_run(entity, args.amount)
        else:
            run(entity, args.amount)
    except ValueError as e:
        logger.error(f"Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())