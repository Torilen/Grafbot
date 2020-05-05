from googletrans import Translator

def translate(text, src='en', dest='en'):
    translator = Translator()
    return translator.translate(text, src=src, dest=dest).text

def detect(text):
    translator = Translator()
    return translator.detect(text).lang