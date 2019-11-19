# python [path]get-pip.py (https://www.liquidweb.com/kb/install-pip-windows/)
# pip install sparqlwrapper
# pip install geojson
# pip install geomet  https://github.com/geomet/geomet
# pip install convertbng https://pypi.org/project/convertbng/

from SPARQLWrapper import SPARQLWrapper, JSON
import geojson
from geomet import wkt
import json

endpoint_url = "http://romanopendata.eu/sparql-endpoint"

query = """PREFIX : <http://www.semanticweb.org/ontologies/2015/1/EPNet-ONTOP_Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?amphtype ?inscriptionType ?ceipacNumber ?transcription ?findingPlace ?country ?lat ?lon
WHERE {
    ?amph a :Amphora .
    ?amph dcterms:identifier ?ceipacNumber .
  FILTER (?ceipacNumber>40000 && ?ceipacNumber < 50001)
  	?amph dcterms:description ?amphdesc .
  	?amph :hasAmphoraType ?amphtypeo .
  	?amphtypeo dcterms:title ?amphtype .
    ?amph :carries ?inscription .
  	?inscription a ?inscriptionType .
  	FILTER (?inscriptionType = :Stamp)
    ?inscription :isTranscribedBy ?linguisticObject .
    ?linguisticObject :hasFullTranscription ?transcription .
    ?amph :hasFindingPlace ?findplace .
    ?findplace :fallsWithin ?cou .
    ?cou a :Country .
    ?cou dcterms:title ?country .
    ?findplace :fallsWithin ?mun .
    ?mun a :Municipality .
    ?mun dcterms:title ?findingPlace .
  	?mun :hasLatitude ?lat.
   	?mun :hasLongitude ?lon.
    optional {
        ?findplace :fallsWithin ?msp .
        ?msp a :ModernSpot .
        ?msp dcterms:title ?findingSpot .
    }
}
ORDER BY ?ceipacNumber ?country ?findingPlace ?findingSpot
"""
# max 10000 elements...

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
    point = "POINT("+str(float(result["lon"]["value"]))+" "+str(float(result["lat"]["value"]))+")"
    #print(point)
    feature = { 'type': 'Feature', 'properties': properties, 'geometry': wkt.loads(point) }
    features.append(feature)
geojson = {'type': 'FeatureCollection', 'features': features }

print(json.dumps(geojson, sort_keys=True, indent=4))

with open('D:/tmp/romanopendata_40000_50001.geojson', 'w') as f:
    json.dump(geojson, f)
