# python [path]get-pip.py (https://www.liquidweb.com/kb/install-pip-windows/)
# pip install sparqlwrapper
# pip install geojson
# pip install geomet  https://github.com/geomet/geomet
# pip install convertbng https://pypi.org/project/convertbng/

from SPARQLWrapper import SPARQLWrapper, JSON
import geojson
from geomet import wkt
import json
import utm
from convertbng.util import convert_bng, convert_lonlat
import shapely

endpoint_url = "http://sandbox.mainzed.org/osi/sparql"

query = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX osi: <http://ontologies.geohive.ie/osi#>
PREFIX geosparql: <http://www.opengis.net/ont/geosparql#>

SELECT ?uri ?label ?wkt WHERE {
  ?uri a osi:Townland .
  ?uri rdfs:label ?label .
  FILTER (langMatches( lang(?label), "en" ) )
  ?uri geosparql:hasGeometry ?geom .
  ?geom geosparql:asWKT ?wkt.
} LIMIT 5"""

def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url, agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

results = get_results(endpoint_url, query)

print(results)
with open('D:/tmp/test.json', 'w') as f:
    json.dump(results, f)

# geojson stuff
features = []
for result in results["results"]["bindings"]:
    properties = {}
    for var in results["head"]["vars"]:
        properties[var] = result[var]["value"]
    wktStr = result["wkt"]["value"].replace("<http://www.opengis.net/def/crs/EPSG/0/2157> ","")
    print(wktStr)
    feature = { 'type': 'Feature', 'properties': properties, 'geometry': wkt.loads(wktStr) }
    features.append(feature)
geojson = {'type': 'FeatureCollection', 'features': features }

print(json.dumps(geojson, sort_keys=True, indent=4))

with open('D:/tmp/data.geojson', 'w') as f:
    json.dump(geojson, f)
