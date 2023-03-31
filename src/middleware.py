import flask
from flask import Flask
from flask_cors import CORS
import openai
from CacheManager import CacheManager
import re

app = Flask(__name__)
CORS(app)

openai.api_key = "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"
cached_responses = CacheManager("fyp_cache")
sentence_splitter = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')


@app.route("/sendText/<text>", methods=["GET"])
def hello(text):
    try:
        response = flask.make_response(f"{text}")
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        return flask.make_response(f"{e.__class__.__name__}: {e}")
    

@app.route("/sendText", methods=["OPTIONS", "POST"])
def recieve_text_post():
    try:
        query = flask.request.form['inputText']
        neutral_responses = []

        for sentence in sentence_splitter.split(query):
            try:
                neutral_response = cached_responses(sentence)
                print(f"found {query=} in cache with {neutral_response=}")
            except KeyError:
                gpt_response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Can you rewrite this to sound more neutral - {query}",
                    temperature=0.3,
                    max_tokens=128,
                )
                neutral_response = gpt_response["choices"][0]["text"]
                cached_responses[query] = neutral_response

            neutral_responses.append(neutral_response)

        response = flask.make_response('. '.join(neutral_responses))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    
    except Exception as e:
        return flask.make_response(f"{e.__class__.__name__}: {e}")

app.run(debug=True)
