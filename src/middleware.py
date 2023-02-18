import flask
from flask import Flask
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route("/sendText/<text>", methods=["GET"])
def hello(text):
    print(f"We got {text}")
    return {'body':json.dumps(f"We got {text}")}

@app.route("/sendText", methods=["OPTIONS", "POST"])
def recieve_text_post():
    try:
        response = flask.make_response(flask.request.form['inputText'])
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        return flask.make_response(f"{e.__class__.__name__}: {e}")

app.run(debug=True)
