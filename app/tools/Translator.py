from googletrans import Translator
from bs4 import BeautifulSoup
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

def detect(text):
    translator = Translator()
    return translator.detect(text).lang

if __name__ == '__main__':
    translate_by_url("Hi how are you ?")