# python [path]get-pip.py (https://www.liquidweb.com/kb/install-pip-windows/)
# pip install sparqlwrapper
# pip install geojson
# pip install geomet  https://github.com/geomet/geomet

from SPARQLWrapper import SPARQLWrapper, JSON
import geojson
from geomet import wkt
import json

endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?label ?geo ?item WHERE {
  ?item wdt:P31 wd:Q2016147;
    wdt:P361 wd:Q67978809;
    wdt:P195 ?collection.
  OPTIONAL { ?item wdt:P625 ?geo. }
  OPTIONAL {
    ?item rdfs:label ?label.
    FILTER((LANG(?label)) = "en")
  }
  OPTIONAL {
    ?collection rdfs:label ?collectionLabel.
    FILTER((LANG(?collectionLabel)) = "en")
  }
}
ORDER BY (?label)"""

def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

results = get_results(endpoint_url, query)

features = []

for result in results["results"]["bindings"]:
    #print(result)
    #print(result["label"]["value"])
    #print(result["geo"]["value"])
    #print(result["item"]["value"])
    #labels.append(result["label"]["value"])
    #geoms.append(result["geo"]["value"].replace("Point", "POINT"))
    #geomsgj.append(wkt.loads(result["geo"]["value"].replace("Point", "POINT")))
    #items.append(result["item"]["value"])
    feature = { 'type': 'Feature', 'properties': { 'label': result["label"]["value"], 'item': result["item"]["value"] }, 'geometry': wkt.loads(result["geo"]["value"].replace("Point", "POINT")) }
    features.append(feature)

# geojson stuff

geojson = {'type': 'FeatureCollection', 'features': features }

print(json.dumps(geojson, sort_keys=True, indent=4))

with open('D:/tmp/data.geojson', 'w') as f:
    json.dump(geojson, f)
