import pytest
from entity import Entity, EntityFactory
from router import Router
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

@pytest.fixture
def setup():
    # Setup code for integration tests
    base_url = os.getenv('BASE_URL')
    factory = EntityFactory()
    router = Router(base_url)
    yield factory, router

    # Cleanup code for integration tests go after this line
    pass

@pytest.mark.parametrize("entity_type", list(Entity))
def test_router_post(setup, entity_type):
    factory, router = setup
    try:
        entity = factory.create_entity(entity_type)
        response = router.post(entity_type, [entity])
        assert response.status_code == 200, f"Failed with status code {response.status_code}: {response.text}"
    except Exception as e:
        pytest.fail(str(e))
