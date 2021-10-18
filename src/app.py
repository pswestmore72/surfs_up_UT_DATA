from flask import Flask, json, jsonify, render_template
import os

app = Flask(__name__)

def not_found():
    return {'error': "Not Found!"}, 404

@app.route('/', methods=['GET'])
def index():
    print("Server received request for 'Home' page")
    return render_template('home.html', data={})


if __name__ == "__main__":
    app.run(debug=True, port=3000)