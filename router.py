import logging
import requests
from typing import List, Dict, Any
from entity import Entity

class Router:
    def __init__(self, base_url: str):
        """
        Initialize the Router with a base URL.
        
        Args:
            base_url (str): The base URL for all API requests
        """
        self.base_url = base_url.rstrip('/')
        self.endpoints = {
            Entity.CREDITCARD: "/creditcards",
            Entity.EMPLOYEE: "/employees",
            Entity.FLIGHT: "/flights",
            Entity.PASSENGER: "/passengers",
            Entity.PLANE: "/planes",
            Entity.USER: "/users",
        }

    def post(self, entity_type: Entity, data: List[Dict[str, Any]]) -> requests.Response:
        """
        Send a POST request to the corresponding entity endpoint with the provided data.
        
        Args:
            entity_type (Entity): The type of entity to post
            data (List[Dict[str, Any]]): Array of JSON objects to send
            
        Returns:
            requests.Response: The response from the server
            
        Raises:
            ValueError: If the entity type is not supported
            requests.exceptions.RequestException: If the request fails
        """
        endpoint = self.endpoints.get(entity_type)
        if endpoint is None:
            raise ValueError(f"No endpoint found for entity: {entity_type.name}")
            
        url = f"{self.base_url}{endpoint}"

        logging.info(f"Sending POST request to {url}")

        response = requests.post(url, json=data, params={'batch': 'true'})
        response.raise_for_status()  # Raise an exception for bad status codes

        logging.info(f"POST {url} request successful")

        return response