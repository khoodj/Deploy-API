import json
import os
import ssl

import requests

# Define the URL of the API endpoint
# url = "http://localhost:8080//optimize"
url = "http://localhost:7071/optimize"

# Define a dictionary to store data under different headers
data = {"num_products": 100, "num_resources": 10}

try:
    # Make the POST request
    response = requests.post(url, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response JSON
        response_json = response.json()
        production_quantities = response_json.get("production_quantities")
        print("Production Quantities:")
        for i, quantity in enumerate(production_quantities):
            print(f"Product {i+1}: {quantity}")
    else:
        print(f"POST request failed with status code {response.status_code}")
        print("Response:")
        print(response.text)  # Print the error message from the API, if any

except requests.exceptions.RequestException as e:
    print("Error making POST request:", e)
