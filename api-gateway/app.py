from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Microservice URLs (make sure these are correct based on your docker-compose)
AUTH_SERVICE = "http://auth-service:5001"
INVENTORY_SERVICE = "http://inventory-service:5002"
ORDER_SERVICE = "http://order-service:5003"

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

# Route to Inventory-Service
@app.route("/inventory/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def inventory_service(path):
    try:
        # Make the request to the inventory service
        response = requests.request(
            method=request.method,
            url=f"{INVENTORY_SERVICE}/{path}",
            headers=request.headers,
            json=request.get_json()  # Pass the JSON body if any
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to Order-Service
@app.route("/orders/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def order_service(path):
    try:
        # Make the request to the order service
        response = requests.request(
            method=request.method,
            url=f"{ORDER_SERVICE}/{path}",
            headers=request.headers,
            json=request.get_json()  # Pass the JSON body if any
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # API Gateway listening on port 5000
