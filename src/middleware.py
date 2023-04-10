import flask
from flask import Flask
from flask_cors import CORS
from CacheManager import CacheManager
import re
import torch
from transformers import T5Tokenizer 

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = torch.load(r"/Users/utkarsh/Desktop/Utkarsh/College/Year_4/FYP/FYPBackend/src/model/my_model.pt")
model.eval()
device = torch.device("cpu")

app = Flask(__name__)
CORS(app)

cached_responses = CacheManager("fyp_cache")
sentence_splitter = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')


@app.route("/sendText/<text>", methods=["GET"])
def hello(text):
    try:
        query = text.strip()
        neutral_responses = []

        for sentence in sentence_splitter.split(query):
            sentence = sentence.strip()
            try:
                neutral_response = cached_responses(sentence)
                print(f"found {query=} in cache with {neutral_response=}")
                
            except KeyError:
                
                input_text = f"Rewrite this in a neutral tone: {sentence}"
                input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)
                outputs = model.generate(input_ids, max_new_tokens=4096, early_stopping=False, temperature=3)
                neutral_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                cached_responses[sentence] = neutral_response
                print(f"New Response added to cache {neutral_response=}")
            except TypeError:
                print(type(cached_responses(sentence)), cached_responses(sentence))

            except Exception as e:
                print(e)

            neutral_responses.append(neutral_response)

        response = flask.make_response('. '.join(neutral_responses))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    
    except Exception as e:
        return flask.make_response(f"{e.__class__.__name__}: {e}")
    

@app.route("/sendText", methods=["OPTIONS", "POST"])
def recieve_text_post():
    try:
        query = flask.request.form['inputText'].strip()
        neutral_responses = []

        for sentence in sentence_splitter.split(query):
            sentence = sentence.strip()
            try:
                neutral_response = cached_responses(sentence)
                print(f"found {query=} in cache with {neutral_response=}")
                
            except KeyError:
                
                input_text = f"Rewrite this in a neutral tone: {sentence}"
                input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)
                outputs = model.generate(input_ids, max_new_tokens=4096, early_stopping=False, temperature=3)
                neutral_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                cached_responses[sentence] = neutral_response
                print(f"New Response added to cache {neutral_response=}")
            except TypeError:
                print(type(cached_responses(sentence)), cached_responses(sentence))

            except Exception as e:
                print(e)

            neutral_responses.append(neutral_response)

        response = flask.make_response('. '.join(neutral_responses))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    
    except Exception as e:

        return flask.make_response(f"{e.__class__.__name__}: {e}")

app.run(debug=True)
