# python [path]get-pip.py (https://www.liquidweb.com/kb/install-pip-windows/)
# pip install pandas
# conda install geopandas with Microconda https://geopandas.readthedocs.io/en/latest/install.html#installing-with-anaconda-conda #conda install -c conda-forge geopandas
# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/
# pip install geojson
# pip install nlgeojson https://github.com/murphy214/nlgeojson
# pip install shapely

import pandas as pd
#import geopandas as gpd
from SPARQLWrapper import SPARQLWrapper, JSON
import geojson
import tempfile
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

for result in results["results"]["bindings"]:
    #print(result)
    #print(result["label"]["value"])
    #print(result["geo"]["value"])
    #print(result["item"]["value"])
    labels.append(result["label"]["value"])
    geoms.append(result["geo"]["value"])
    items.append(result["item"]["value"])

#print(labels)

# dataframe and pandas
# https://www.geeksforgeeks.org/python-pandas-dataframe/

# Define a dictionary containing employee data
data = {'labels':labels,
        'geoms':geoms,
        'items':items}

# Convert the dictionary into DataFrame
df = pd.DataFrame(data)

# select two columns
print(df[['labels', 'items', 'geoms']])

# geojson stuff

# https://geopandas.readthedocs.io/en/latest/gallery/create_geopandas_from_pandas.html
