# import flask dependencies

from flask import Flask, request, jsonify, make_response, render_template
import os
import dialogflow_v2 as dialogflow
from response import RespondDB
from df_response_lib import *

# import requests
# import json
# import pusher


# initialize the flask app
app = Flask(__name__)


# default route
@app.route('/')
def index():
    card = {
        'card_title': 'informacje znajdziesz tu:',
        'text': 'wybierz jedną z pozycji',
        'sugestion1': 'SZOOP',
        'sugestion2': 'KWALIFIKOWALNOŚĆ',
        'link1': 'https://www.w3schools.com',
        'link2': 'https://www.w3schools.com',
    }
    return render_template('index.html', card=card)


@app.route('/simple_card')
def simple_card():



    return render_template('simple_card.html', card=card)

# functions for responses


# function to get response about project types



def nacoDofinansowanie(req):

    parameters = req.get('queryResult').get('parameters')
    parameters_string = str(parameters.values())
    db_value = parameters_string[-7:-3]
    response = RespondDB('typProjektu', 'TypyProjektow', 'dzialanie_id')
    result = response.get_db_info(value=db_value)
    text1 = 'Dla Działania {0} przewidziane są projekty typu:'.format(db_value)
    text2 = str(result)
# return text between brackets
    text2 = text2[text2.find("(")+1:text2.rfind(")")]
    return "{0}  {1}".format(text1, text2)


@app.route('/send_message', methods=['GET', 'POST'])
def send_message():

    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'pl')
    #print('message_Stachu_fulfillment_text =', fulfillment_text)
    response_text = {"message":  fulfillment_text.query_result.fulfillment_text, "tests": "haloo"}
    #response_text = {"suggestions":  fulfillment_text.query_result.fulfillment_messages[1].suggestions.suggestions.title}
    print('message_Stachu =', response_text)
    return jsonify(response_text)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        print('response =', response)

        return response
        # return response.query_result.fulfillment_text

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():

    # build a request object
    req = request.get_json(force=True)
    # fetch action from json
    action = req.get('queryResult').get('action')

    if action == 'input.nacoDofinansowanie':
        results = nacoDofinansowanie(req)

    if action == 'Demo':
        #fulfillment_text = 'Response form webhook sugestia'

        #aog = actions_on_google_response()
        #aog_sr = aog.simple_response([[fulfillment_text, fulfillment_text, False]])
        #aog_sc = aog.suggestion_chips(['sugestia 1', 'sugestia 2'])

        #ff_response = fulfillment_response()
        #ff_text = ff_response.fulfillment_text(fulfillment_text)
        #ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])

        #results = ff_response.main_response(ff_text, ff_messages)


        results = {'fulfillmentText': "Moja odpowiedz z webhooka",
                   'messages': [
                      {
                        "platform": "google",
                        "suggestions": [
                          {
                            "title": "Chip One"
                          },
                          {
                            "title": "Chip Two"
                          }
                        ],
                        "type": "suggestion_chips"
                      }
                    ]
                    }
        print('halohalo:', results)
        return make_response(jsonify(results))

    # return response
    return make_response(jsonify({'fulfillmentText': results}))





# run the app
if __name__ == '__main__':
    app.run()
