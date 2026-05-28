import base64
import json
from flask import Flask, render_template, request
from flask_cors import CORS
import os
from worker import speech_to_text, text_to_speech, watsonx_process_message

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    print("processing STT request")
    audio_binary = request.data
    text = speech_to_text(audio_binary)
    #creating json response for front end
    response = app.response_class(
        response=json.dumps({'text':text}),
        status=200,
        mimetype='application/json'
    )
    print(response)
    print(response.data)
    return(response)

@app.route('/process-message', methods=['POST'])
def process_message_route():
    user_message = request.json['userMessage']
    print('user_message',user_message)
    
    voice = request.json['voice']
    print('voice',voice)

    #Call watsonx model to process user message and voice preference
    watsonx_response_text = watsonx_process_message(user_message,voice)

    #transform watsonx text response into speech for user
    watsonx_response_speech = text_to_speech(watsonx_response_text)

    #convert raw audio into base64 so front end can process it easily
    watsonx_response_speech = base64.b64encode(watsonx_response_speech).decode('utf-8')

    response = app.response_class(
        response =json.dumps({
            "watsonxResponseText":watsonx_response_text,
            "watsonxResponseSpeech":watsonx_response_speech
        }),
        status=200,
        mimetpye='application/json'
    )
    print(response)
    return response

if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')
