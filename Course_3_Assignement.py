import json
import requests_with_caching


# TasteDive stuff
def get_movies_from_tastedive(title: str):
    """Get data from TasteDive for a movie TITLE or music artist."""
    base_url = 'https://tastedive.com/api/similar'
    parameters = {}
    parameters['q'] = title
    parameters['type'] = 'movies'
    parameters['limit'] = 5

    Response = requests_with_caching.get(base_url, parameters)
    TasteDiveDictionary = json.loads(Response.text)

    return TasteDiveDictionary


def extract_movie_titles(TasteDiveDictionary):
    """Extracts just the list of movie titles from a dictionary returned by get_movies_from_tastedive"""
    # print(type(TasteDiveDictionary))
    # print(list(TasteDiveDictionary.keys()))
    # print(type(TasteDiveDictionary['Similar']))
    # print(list(TasteDiveDictionary['Similar'].keys()))
    # print(type(TasteDiveDictionary['Similar']['Results']))
    # print(len(TasteDiveDictionary['Similar']['Results']))
    # print(TasteDiveDictionary['Similar']['Results'])
    return [movie['Name'] for movie in TasteDiveDictionary['Similar']['Results']]


def get_related_titles(lst_movies: list):
    """ Takes a list of movie titles as input.
    It gets five related movies for each from TasteDive,
    extracts the titles for all of them, and combines them all
    into a single list. """
    related_titles = []
    for movie in lst_movies:
        for suggested in extract_movie_titles(get_movies_from_tastedive(movie)):
            if suggested not in related_titles:
                related_titles.append(suggested)
    return related_titles


# OMDB stuff
def get_movie_data(title: str):
    """Return a dictionary with information about that movie"""
    baseURL = 'http://www.omdbapi.com/'
    parameters = {}
    parameters['t'] = title
    parameters['r'] = 'json'

    response = requests_with_caching.get(baseURL, parameters)
    py_object = json.loads(response.text)

    return py_object


def get_movie_rating(ombd_dictionary):
    """ Takes an OMDB dictionary result for one movie
    and extracts the Rotten Tomatoes rating as an integer. """
    # print(list(OMDBdictionary.keys()))
    # print(OMDBdictionary['Ratings'])
    rotten_tomatoes_rating = 0
    for rating in ombd_dictionary['Ratings']:
        if rating['Source'] == 'Rotten Tomatoes':
            rotten_tomatoes_rating = int(rating['Value'][:-1])
    return rotten_tomatoes_rating


def get_sorted_recommendations(titles: list):
    """  It takes a list of movie titles as an input.
    It returns a sorted list of related movie titles as output,
    up to five related movies for each input movie title.
    The movies should be sorted in descending order by their
    Rotten Tomatoes rating, as returned by the
    get_movie_rating function. """
    related_titles = get_related_titles(titles)
    sorted_recommendations = sorted(related_titles, key=lambda title: (get_movie_rating(get_movie_data(title)), title),
                                    reverse=True)
    return sorted_recommendations
