"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
from google.oauth2 import service_account
import os

dict_lang = dict()
dict_lang['fr'] = "fr-FR"
dict_lang['en'] = "en-US"

def speak(text, lang, env):
    urls = dict()
    urls["windows"] = "C:/Users/scorp/Grafbot-c753fa94ac04.json"
    urls["ubuntu"] = "/root/Grafbot/Grafbot-c753fa94ac04.json"

    path = dict()
    path["windows"] = "web/"
    path["ubuntu"] = "/root/Grafbot/app/web/"
    credentials = service_account.Credentials.from_service_account_file(urls[env])
    # Instantiates a client
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code=dict_lang[lang],
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    with open(path[env]+'output.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)