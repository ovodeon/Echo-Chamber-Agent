import os
import requests
from typing import Dict, Any

PARALLEL_MCP_URL = "https://search.parallel.ai/mcp"

class ParallelMCPClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("PARALLEL_API_KEY")
        if not self.api_key:
            raise ValueError("PARALLEL_API_KEY is required.")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def search_subculture(self, objective: str, query: str) -> Dict[str, Any]:
        """Calls Parallel MCP web_search tool to pull live cultural discourse."""
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "web_search",
                "arguments": {
                    "objective": objective,
                    "search_queries": [query]
                }
            },
            "id": 1
        }
        try:
            response = requests.post(PARALLEL_MCP_URL, headers=self.headers, json=payload, timeout=15)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Parallel MCP Call Failed: {str(e)}"}
