# python [path]get-pip.py (https://www.liquidweb.com/kb/install-pip-windows/)
# pip install pandas
# conda install geopandas with Microconda https://geopandas.readthedocs.io/en/latest/install.html#installing-with-anaconda-conda #conda install -c conda-forge geopandas
# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/
# pip install geojson
# pip install nlgeojson https://github.com/murphy214/nlgeojson
# pip install shapely
# pip install geomet  https://github.com/geomet/geomet

import pandas as pd
#import geopandas as gpd
from SPARQLWrapper import SPARQLWrapper, JSON
import geojson
import tempfile
from geomet import wkt
#import nlgeojson as nl
#from shapely import wkt

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

labels = []
geoms = []
items = []
geomsgj = []

features = []

for result in results["results"]["bindings"]:
    #print(result)
    #print(result["label"]["value"])
    #print(result["geo"]["value"])
    #print(result["item"]["value"])
    labels.append(result["label"]["value"])
    geoms.append(result["geo"]["value"].replace("Point", "POINT"))
    geomsgj.append(wkt.loads(result["geo"]["value"].replace("Point", "POINT")))
    items.append(result["item"]["value"])
    feature = { 'type': 'Feature', 'properties': { 'label': result["label"]["value"] }, 'geometry': wkt.loads(result["geo"]["value"].replace("Point", "POINT")) }
    print(feature)
    features.append(feature)

#print(labels)

# dataframe and pandas
# https://www.geeksforgeeks.org/python-pandas-dataframe/

# Define a dictionary containing employee data
data = {'labels':labels,
        'geoms':geoms,
        'items':items,
        'geomsgj':geomsgj}

# Convert the dictionary into DataFrame
df = pd.DataFrame(data)

# select two columns
print(df[['labels', 'items', 'geoms']])

# geojson stuff

geojson = {'type': 'FeatureCollection', 'features': features }

print(geojson)
