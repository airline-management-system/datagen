import argparse
import logging
from dotenv import load_dotenv
import os
import json

from entity import Entity, EntityFactory
from router import Router
from scheme import StandardScheme

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Base URL for the API from environment variables
BASE_URL = os.getenv('BASE_URL')

factory = EntityFactory()
router = Router(BASE_URL)
scheme = StandardScheme(factory, router)

def run_generate_dry_run(entity_type: Entity, amount: int):
    logging.info("Dry run mode - displaying generated data:")
    entities = factory.create_entities(entity_type, amount)
    print(json.dumps(entities, indent=2, ensure_ascii=False))

def run_generate(entity_type: Entity, amount: int) -> None:
    logging.info(f"Generating f{amount} entities of {entity_type}")
    entities = factory.create_entities(entity_type, amount)
    router.post(entity_type, entities)

def run_scheme_dry_run():
    logging.info("Dry run mode - displaying the scheme generation:")
    all_flights = []
    for entity, data in scheme:
        logging.info(f"Generated entity: {entity.name}, data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        if entity.name.lower() == "flight":
            all_flights.extend(data if isinstance(data, list) else [data])
    if all_flights:
        print("All generated flights:")
        print(json.dumps(all_flights, indent=2, ensure_ascii=False))

def run_scheme():
    logging.info("Executing the standard generation scheme.")
    scheme.execute()


def main():
    parser = argparse.ArgumentParser(description='Entity processing CLI')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subcommand: scheme
    scheme_parser = subparsers.add_parser('scheme', help='Execute the generation scheme')

    # Subcommand: generate
    generate_parser = subparsers.add_parser('generate', help='Generate entities')

    generate_parser.add_argument(
        '-e', '--entity',
        type=str,
        required=True,
        help=f'Entity to process ({"|".join([e.name.lower() for e in Entity])})'
    )
    generate_parser.add_argument(
        '-a', '--amount',
        type=int,
        required=True,
        help='Amount to process'
    )
    generate_parser.add_argument(
        '-d', '--dry-run',
        action='store_true',
        help='Generate data without making HTTP requests'
    )

    scheme_parser.add_argument(
        '-d', '--dry-run',
        action='store_true',
        help='Execute scheme without making HTTP requests'
    )

    args = parser.parse_args()

    try:
        if args.command == 'scheme':
            if args.dry_run:
                run_scheme_dry_run()
            else:
                run_scheme()
        elif args.command == 'generate':
            entity = Entity.from_string(args.entity)
            if args.dry_run:
                run_generate_dry_run(entity, args.amount)
            else:
                run_generate(entity, args.amount)
    except ValueError as e:
        logging.error(f"Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())