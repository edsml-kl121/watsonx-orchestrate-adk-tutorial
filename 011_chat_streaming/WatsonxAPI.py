import requests
import json
from typing import Iterator, Dict, Any

class WatsonxAPI:
    def __init__(self, config: dict):
        self.api_key = config["orchestrate_config"]["api_key"]
        self.base_url = config["orchestrate_config"]["base_url"]
        self.agent_id = config["orchestrate_config"]["agent_id"]
        self.environment_id = config["orchestrate_config"]["environment_id"]
        # Remove all the old foundation model parameters
        
    def chat_with_agent_stream(self, message: str, thread_id: str = None) -> Iterator[Dict[str, Any]]:
        """Stream chat with Watson Orchestrate agent"""
        url = f"{self.base_url}/api/v1/orchestrate/runs/stream"
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "message": {
                "role": "user",
                "content": [{"response_type": "conversational_search"}],
                "assistant_id": self.agent_id
            },
            "thread_id": thread_id,
            "agent_id": self.agent_id,
            "environment_id": self.environment_id,
            # Add your OpenAPI spec reference here
            "context_variables": {}
        }
        
        response = requests.post(url, headers=headers, json=payload, stream=True)
        
        for line in response.iter_lines():
            if line:
                yield json.loads(line.decode('utf-8'))