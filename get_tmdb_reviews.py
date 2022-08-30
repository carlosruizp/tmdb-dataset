import tmdbsimple as tmdb
from cleantext import clean
import pandas as pd
from icecream import ic

MAX_PAGES = 1000 # Max number of movie pages to download
tmdb.REQUESTS_TIMEOUT = (2, 5)  # seconds, for connect and read specifically 

with open('API.secret', 'r') as f:
    API_KEY = f.read()
tmdb.API_KEY = API_KEY

def get_reviews_from_id(id):
    movie = tmdb.Movies(id)
    response = movie.reviews()
    n_pages = response['total_pages']
    reviews = {}
    for p in range(1, n_pages+1):
        page_resp = movie.reviews(page=p)
        for r in page_resp['results']:
            review_id = r['id']
            review_text = r['content']
            reviews[review_id] = [clean(review_text, no_emoji=True)]
    return reviews


discover = tmdb.Discover()
response = discover.movie(vote_count_gte=500)
ic(response['total_pages'])
n_pages = min(response['total_pages'], MAX_PAGES)


for p in range(1, n_pages+1):
    reviews = {}
    ic(p)
    response = discover.movie(vote_count_gte=500, page=p)
    for result in response['results']:
        print(result['title'], result['id'])
        id = result['id']
        resp = get_reviews_from_id(id)
        reviews = {**reviews, **resp}
    
    columns = ['text']
    reviews_df = pd.DataFrame.from_dict(reviews, orient='index', columns=columns)
    print(reviews_df)
    
    reviews_df.to_csv('reviews.csv', mode='a', header=False, index=False)