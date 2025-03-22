from flask import Flask, request, jsonify

app = Flask(__name__)

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     return jsonify({"message": "Login successful", "user": data['username']})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)