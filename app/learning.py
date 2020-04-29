import nltk
from tools.EntityExtractor import get_entities
from tools.Converter import Entities2Tuples

from structure.SemKG import SemKG

nltk.download('punkt')

semkg = SemKG()

inp = "Le chat a mangé la souris mais a une queue noire"

entities = get_entities(inp)

tuples = Entities2Tuples([x[0] for x in get_entities("Le chat a mangé la souris mais a une queue noire")], "quadratic")

semkg.add_relations(tuples)

semkgContent = semkg.get_graph()

print(semkgContent["graph"])
print(semkgContent["nodesId"])
