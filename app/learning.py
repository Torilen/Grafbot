import nltk
from tools.EntityExtractor import get_entities
from tools.Converter import Entities2Tuples

from structure.SemKG import SemKG
from structure.EpiKG import EpiKG

nltk.download('punkt')

semkg = SemKG()
epikg = EpiKG()

inp = "Le chat a mangé la souris mais a une queue noire"

entities = get_entities(inp)

tuples = Entities2Tuples([x[0] for x in entities], "quadratic")

semkg.add_relations(tuples, epikg)
#epikg.add_relations([(t[0], t[1], "a mangé") for t in tuples])

semkgContent = semkg.get_graph()
print([x[0] for x in entities])
semkg.get_stories(epikg, [x[0] for x in entities])
#print(list(epikg.get_graph()["s_root"].keys()))
print(semkgContent["nodesId"])
