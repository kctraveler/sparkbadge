import os
import json
import requests
from requests.models import Response
from typing import Dict, Any
from dotenv import load_dotenv

#load_dotenv()

class Metrics:
    """Longitudinal metrics data. Contains desired metrics."""

    def __init__(self, 
                 start_time: str, 
                 end_time: str, 
                 metrics: Dict
    ):
        """Initialize a Metrics object. 

        Args:
            start_time: 
            end_time:
            metrics:

        The metrics dict accepts the following:
            runner: get metrics related to workflows on user infra.
            workflows: get metrics related to workflows.
            workflow_jobs: get metrics on jobs within a workflow.
            workflow_runs: get metrics on execution of workflows.
        """
        self.start_time = start_time
        self.end_time = end_time
        self.metrics = metrics
    

    def bearer_oauth(self, r: Response) -> Response:
        """Method required by bearer token authentication.

        Args:
            r: The response. 

        Returns:
            The response with the headers appended.
        """
        # NOTE: This function is here if we need API authentication
        bearer_token = os.getenv("GITLAB_API_TOKEN")
        r.headers["Authorization"] = f"Bearer {bearer_token}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r


    def connect_to_endpoint(self, url: str, params: Dict[str, Any]) -> Dict:
        """Connect to API endpoint.

        Args:
            url: The base url.
            params: The query params to retrieve.
            
        Returns:
            The json response. 
        """

        access_token = os.getenv("GITLAB_API_TOKEN")
        headers = { "Private-Token": access_token }
        response = requests.get(url, headers=headers, params=params)
        # print(response.url)
            
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

