import requests

from elsevier_apikey import apikey

URL_SOURCE = "http://api.elsevier.com/content/search/sciencedirect?query=%s&date=%d"


def retrieves_nb_search(search_token, year):
    """
    Retrieves the number of search results for a specific query and a year

    :param search_token: the query to send to Sciencedirect search engine
    :type search_token: str
    :param year: the year to look for (can be a range, eg. 2001-2005)
    :type year: str or int
    :raises BaseException: when the query doesn't succeed
    :return: the number of total results
    :rtype: str
    """
    header = {"Accept": "application/json", "X-ELS-APIKey": apikey}

    r = requests.get(URL_SOURCE % (search_token, year), headers=header)
    if r.status_code != 200:
        raise BaseException("Error %s" % r.status_code)

    return r.json()["search-results"]["opensearch:totalResults"]


if __name__ == "__main__":
    import logging

    import matplotlib.pyplot as plt
    import pandas as pd

    years_range = range(2000, 2020)
    tokens = ["smart city", "sustainable city"]

    results = {}
    for token in tokens:
        logging.info("Looks for token %s", token)
        results[token] = {}
        for year in years_range:
            value = retrieves_nb_search(token, year)
            results[token][year] = int(value.strip())
            logging.info("\t Year %s: %s", year, value)

    df = pd.DataFrame(results)
    df.columns = [f'expression "{c}"' for c in df.columns]

    df.plot(figsize=(7, 7), marker=".")
    plt.title("Number of publications per year on sciencedirect.com")
    plt.tight_layout()
    plt.show()
