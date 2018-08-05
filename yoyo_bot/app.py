# Ref: https://github.com/bhavaniravi/rasa-site-bot
from flask import Flask
from flask import render_template, jsonify, request
import requests
import random
from engine import (
    intent_response_dict, gstinfo_response_dict,
    gst_query_value_dict, gst_info, gst_query,
    handle_greet, handle_affirm, handle_restaurant_search,
    handle_goodbye,
)


HANDLES = {
    "greet": handle_greet,
    "affirm": handle_affirm,
    "restaurant_search": handle_restaurant_search,
    "goodbye": handle_goodbye,
}


app = Flask(__name__)
app.secret_key = '12345'


@app.route('/')
def hello_world():
    return render_template('home.html')

get_random_response = lambda intent:random.choice(intent_response_dict[intent])


@app.route('/chat',methods=["POST"])
def chat():
    try:
        user_message = request.form["text"]
        response = requests.get("http://localhost:5000/parse", params={"q":user_message})
        response = response.json()
        print("Got Response from NLP server...")
        entities = response.get("entities")
        topresponse = response["intent"]
        intent = topresponse.get("name")
        print("Intent {}, Entities {}".format(intent, entities))
        if intent == "gst-info":
            response_text = gst_info(entities)# "Sorry will get answer soon" #get_event(entities["day"],entities["time"],entities["place"])
        elif intent == "gst-query":
            response_text = gst_query(entities)
        else:
            response_text = get_random_response(intent)
        return jsonify({"status":"success","response": response_text})
    except Exception as e:
        print(e)
        return jsonify({"status":"success","response":"Sorry I am not trained to do that yet..."})


app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8080)
