import nltk
from tools.EntityExtractor import get_entities
from tools.Converter import Entities2Tuples

from structure.SemKG import SemKG
from structure.EpiKG import EpiKG

nltk.download('punkt')

semkg = SemKG()
epikg = EpiKG()

inp = "Selon les résultats de travaux menés en 2006 et 2007, le chat domestique est une sous-espèce du chat sauvage Felis silvestris issue d'ancêtres appartenant à la sous-espèce du chat sauvage d’Afrique"

entities = get_entities(inp)

tuples = Entities2Tuples(entities, "linear")

semkg.add_relations(tuples, epikg, inp)

print(entities)

print(semkg.get_stories(epikg, ["2006", "chat"]))




