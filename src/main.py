import pandas
import numpy
import json
from configs.config_const import CATEGORIES, DIR_SAVED_DATA
from utils.util import get_total_pages

def load_articles() -> list:
    articles = []
    for category in CATEGORIES:
        for page in get_total_pages():
            filepath = f"{DIR_SAVED_DATA}/items-{category}-{page}.json"
            try:
                dataPage = open(filepath)
                articlesByPage = json.load(dataPage)
                articles = articles + articlesByPage
            except:
                print(f"No se pudo cargar el arcivo: {filepath}")
    
    return articles

def preprocess_text(text: str):
    return []

dataframe = pandas.DataFrame(load_articles())
print(dataframe)