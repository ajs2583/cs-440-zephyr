from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Microservice URLs 
AUTH_SERVICE = "http://auth-service:5001"
FLIGHT_SERVICE = "http://flight-service:5002"
SAVED_SERVICE = "http://saved-service:5003"

# Route to Auth-Service
@app.route("/auth/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def auth_service(path):
    try:
        # Make the request to the auth service
        response = requests.request(
            method=request.method,
            url=f"{AUTH_SERVICE}/{path}",
            headers=request.headers,
            json=request.get_json()  # Pass the JSON body if any
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to flight-Service
@app.route("/flight/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def flight_service(path):
    try:
        # Make the request to the flight service
        response = requests.request(
            method=request.method,
            url=f"{FLIGHT_SERVICE}/{path}",
            headers=request.headers,
            json=request.get_json()  # Pass the JSON body if any
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to saved-Service
@app.route("/saved/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def saved_service(path):
    try:
        # Make the request to the saved service
        response = requests.request(
            method=request.method,
            url=f"{SAVED_SERVICE}/{path}",
            headers=request.headers,
            json=request.get_json()  # Pass the JSON body if any
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # API Gateway listening on port 5000
