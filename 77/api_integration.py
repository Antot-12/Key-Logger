import requests

import config


def on_external_api_event():
    api_endpoints = config.get('api_endpoints', [])
    if not api_endpoints:
        print("No API endpoints configured.")
        return

    for endpoint in api_endpoints:
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                print(f"Data from {endpoint}: {response.json()}")
            else:
                print(f"Failed to reach {endpoint}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error calling API {endpoint}: {e}")
