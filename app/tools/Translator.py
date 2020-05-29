from googletrans import Translator
from bs4 import BeautifulSoup
import urllib

def translate_by_url(text, src='en', dest='en'):
    link = "https://translate.google.fr/?hl=fr#view=home&op=translate&sl="+src+"&tl="+dest+"&text="+text
    f = urllib.urlopen(link)
    myfile = f.read()
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