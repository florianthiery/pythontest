# python [path]get-pip.py (https://www.liquidweb.com/kb/install-pip-windows/)
# pip install sparqlwrapper
# pip install geojson
# pip install geomet  https://github.com/geomet/geomet

from SPARQLWrapper import SPARQLWrapper, JSON
import geojson
from geomet import wkt
import json

endpoint_url = "http://linkedgeodata.org/sparql"

query = """Prefix lgdo: <http://linkedgeodata.org/ontology/>
Prefix geom: <http://geovocab.org/geometry#>
Prefix ogc: <http://www.opengis.net/ont/geosparql#>
Prefix owl: <http://www.w3.org/2002/07/owl#>

Prefix ogc: <http://www.opengis.net/ont/geosparql#>
Prefix geom: <http://geovocab.org/geometry#>
Prefix lgdo: <http://linkedgeodata.org/ontology/>

Select ?item ?label ?geo
From <http://linkedgeodata.org> {
  ?item
    a lgdo:Restaurant ;
    rdfs:label ?label ;
    geom:geometry [
      ogc:asWKT ?geo
    ] .

  Filter (
    bif:st_intersects (?geo, bif:st_point (8.274167,49.998889),0.5)
  ) .
}"""

def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url, agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

results = get_results(endpoint_url, query)

# geojson stuff

features = []

for result in results["results"]["bindings"]:
    properties = {}
    for var in results["head"]["vars"]:
        properties[var] = result[var]["value"]
    print(properties)
    if "POINT" in result["geo"]["value"]:
        feature = { 'type': 'Feature', 'properties': properties, 'geometry': wkt.loads(result["geo"]["value"].replace("Point", "POINT")) }
        features.append(feature)
geojson = {'type': 'FeatureCollection', 'features': features }

print(json.dumps(geojson, sort_keys=True, indent=4))

with open('C:/tmp/data.geojson', 'w') as f:
    json.dump(geojson, f)
