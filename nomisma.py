# python [path]get-pip.py (https://www.liquidweb.com/kb/install-pip-windows/)
# pip install sparqlwrapper
# pip install geojson
# pip install geomet  https://github.com/geomet/geomet
# pip install convertbng https://pypi.org/project/convertbng/

from SPARQLWrapper import SPARQLWrapper, JSON
import geojson
from geomet import wkt
import json

endpoint_url = "http://nomisma.org/query"

query = """PREFIX rdf:	<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dcterms:	<http://purl.org/dc/terms/>
PREFIX geo:	<http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX nm:	<http://nomisma.org/id/>
PREFIX nmo:	<http://nomisma.org/ontology#>
PREFIX skos:	<http://www.w3.org/2004/02/skos/core#>
PREFIX spatial: <http://jena.apache.org/spatial#>
PREFIX xsd:	<http://www.w3.org/2001/XMLSchema#>

SELECT ?mint ?label ?lat ?long WHERE {
   ?loc geo:lat ?lat ;
        geo:long ?long .
   ?mint geo:location ?loc ;
         skos:prefLabel ?label ;
         a nmo:Mint
  FILTER langMatches (lang(?label), 'en')
}"""

def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url, agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

results = get_results(endpoint_url, query)

#print(results)

# geojson stuff
features = []
for result in results["results"]["bindings"]:
    properties = {}
    for var in results["head"]["vars"]:
        properties[var] = result[var]["value"]
    point = "POINT("+str(float(result["long"]["value"]))+" "+str(float(result["lat"]["value"]))+")"
    #print(point)
    feature = { 'type': 'Feature', 'properties': properties, 'geometry': wkt.loads(point) }
    features.append(feature)
geojson = {'type': 'FeatureCollection', 'features': features }

print(json.dumps(geojson, sort_keys=True, indent=4))

with open('D:/tmp/data.geojson', 'w') as f:
    json.dump(geojson, f)
