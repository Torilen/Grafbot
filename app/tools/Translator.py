from googletrans import Translator
from bs4 import BeautifulSoup
from google.cloud import translate
import urllib

def translate_by_url(text, src='en', dest='en'):
    link = "https://translate.google.fr/?hl=fr#view=home&client=gtx&op=translate&sl="+src+"&tl="+dest+"&text="+text
    print(link)
    myfile = urllib.request.urlopen(link).read()
    soup = BeautifulSoup(myfile, "html")
    div = soup.find("span", {"class": "tlid-translation translation"})

    content = str(div)

    print("Le contenu de la traduction est : {}".format(content))

def translate(text, src='en', dest='en'):
    translator = Translator()
    return translator.translate(text, src=src, dest=dest).text

def translate_by_api(text, src='en', dest='en'):
    translate_client = translate.Client("AIzaSyCf3b4hDbDAWSvM8hvVU_elfIzzJz3rmwU")

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=dest)

    print(u'Text: {}'.format(result['input']))
    print(u'Translation: {}'.format(result['translatedText']))
    print(u'Detected source language: {}'.format(
        result['detectedSourceLanguage']))
    return result['translatedText']

def detect(text):
    translator = Translator()
    return translator.detect(text).lang

if __name__ == '__main__':
    translate_by_url("Hi how are you ?")