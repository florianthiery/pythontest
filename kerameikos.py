# python [path]get-pip.py (https://www.liquidweb.com/kb/install-pip-windows/)
# pip install sparqlwrapper
# pip install geojson
# pip install geomet  https://github.com/geomet/geomet
# pip install convertbng https://pypi.org/project/convertbng/

from SPARQLWrapper import SPARQLWrapper, JSON
import geojson
from geomet import wkt
import json

endpoint_url = "http://kerameikos.org/query"

query = """PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX crmgeo: <http://www.ics.forth.gr/isl/CRMgeo/>
PREFIX crmsci: <http://www.ics.forth.gr/isl/CRMsci/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX kid: <http://kerameikos.org/id/>
PREFIX kon: <http://kerameikos.org/ontology#>
PREFIX org: <http://www.w3.org/ns/org#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?pp ?label ?lat ?long WHERE {
   ?loc geo:lat ?lat ;
        geo:long ?long .
   ?pp geo:location ?loc ;
         skos:prefLabel ?label ;
         a kon:ProductionPlace
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
