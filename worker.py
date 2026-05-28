# To call watsonx's LLM, we need to import the library of IBM Watson Machine Learning
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes,DecodingMethods
from ibm_watson_machine_learning.foundation_models import Model
# Define the model parameters
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
import requests
# placeholder for Watsonx_API and Project_id incase you need to use the code outside this environment
# API_KEY = "Your WatsonX API"
PROJECT_ID= "skills-network"

# Define the credentials 
credentials = {
    "url": "https://us-south.ml.cloud.ibm.com"
	#"apikey": API_KEY
}
	
# Specify model_id that will be used for inferencing
model_id = "mistralai/mistral-medium-2505"

parameters = {
    GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
    GenParams.MIN_NEW_TOKENS: 1,
    GenParams.MAX_NEW_TOKENS: 1024
}

# Define the LLM
model = Model(
    model_id=model_id,
    params=parameters,
    credentials=credentials,
    project_id=PROJECT_ID
)


def speech_to_text(audio_binary):
    base_url="https://sn-watson-stt.labs.skills.network"
    api_url = base_url+'/speech-to-text/api/v1/recognize'
    headers = {
        'Content-Type': 'audio/mp3',
        'Accept': 'application/json'
    }
    params = {
        'model':'en-US_Multimedia',
    }
    body = audio_binary

    response = requests.post(api_url, headers=headers,params=params, data=body).json()
    text = 'null'
    while bool(response.get('results')):
        print('STT response:',response)
        text = response.get('results').pop().get('alternatives').pop().get('transcript')
        print('recognized text',text)
        return text

def watsonx_process_message(user_message):
    prompt = f"""
    Translate the following English sentence into Spanish. 
    Reply ONLY with the translation, no explanations, no formatting, no extra text.

    English: {user_message}
    Spanish:
    """
    response_text = model.generate_text(prompt=prompt)
    print("watson-response:",response_text)
    return response_text.strip()

def text_to_speech(text, voice=""):
    base_url = "https://sn-watson-tts.labs.skills.network"
    api_url = base_url+'/text-to-speech/api/v1/synthesize?output=output_text.wav'
    
    #Adding voice selection of user chose one for AI response
    if voice != "" and voice != "default":
        api_url+="&voice="+voice
    
    headers={
        'Accept': 'audio/wav',
        'Content-Type': 'application/json',
    }
    json_data={
        'text':text
    }
    response = requests.post(api_url,headers=headers, data=json_data)
    print('TTS response:',response)
    return response.content

