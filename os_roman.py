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

endpoint_url = "http://data.ordnancesurvey.co.uk/datasets/os-linked-data/apis/sparql"

query = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX spatial: <http://data.ordnancesurvey.co.uk/ontology/spatialrelations/>
PREFIX gaz: <http://data.ordnancesurvey.co.uk/ontology/50kGazetteer/>

SELECT ?uri ?label ?easting ?northing
WHERE {
  ?uri
    #filter on type
    gaz:featureType gaz:RomanAntiquity;

    #bind everything we want to return
    rdfs:label ?label;
    spatial:easting ?easting;
    spatial:northing ?northing;
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
    eastings = [float(result["easting"]["value"])]
    northings = [float(result["northing"]["value"])]
    res_list_en = convert_lonlat(eastings, northings)
    point = "POINT("+str(res_list_en[0][0])+" "+str(res_list_en[1][0])+")"
    print(point)
    feature = { 'type': 'Feature', 'properties': properties, 'geometry': wkt.loads(point) }
    features.append(feature)
geojson = {'type': 'FeatureCollection', 'features': features }

print(json.dumps(geojson, sort_keys=True, indent=4))

with open('D:/tmp/data.geojson', 'w') as f:
    json.dump(geojson, f)
