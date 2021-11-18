import types
import pandas as pd
from botocore.client import Config
import ibm_boto3
import io

def __iter__(self): return 0

endpoint_dc9ddb978841432ba58f9e610c697598 = 'https://s3.eu.cloud-object-storage.appdomain.cloud'

client_dc9ddb978841432ba58f9e610c697598 = ibm_boto3.client(service_name='s3',
    ibm_api_key_id='5CeeegWJZTd5oyM4R65-r-fPAqAII_JctAIQ9gsRFTr2',
    ibm_auth_endpoint="https://iam.cloud.ibm.com/oidc/token",
    config=Config(signature_version='oauth'),
    endpoint_url=endpoint_dc9ddb978841432ba58f9e610c697598)

body = client_dc9ddb978841432ba58f9e610c697598.get_object(Bucket='mvpteamorange-donotdelete-pr-2zh4qs0w6rau5m', Key='users.csv')['Body']
# add missing __iter__ method, so pandas accepts body as file-like object
if not hasattr(body, "__iter__"):
    body.__iter__ = types.MethodType(__iter__, body)

users = pd.read_csv(body, index_col=0)

body = client_dc9ddb978841432ba58f9e610c697598.get_object(Bucket='mvpteamorange-donotdelete-pr-2zh4qs0w6rau5m', Key='ratings.csv')['Body']
# add missing __iter__ method, so pandas accepts body as file-like object
if not hasattr(body, "__iter__"):
    body.__iter__ = types.MethodType(__iter__, body)

ratings = pd.read_csv(body, index_col=0)


ratings = ratings.drop(['timestamp', 'user_emb_id', 'movie_emb_id'], axis=1)


body = client_dc9ddb978841432ba58f9e610c697598.get_object(Bucket='mvpteamorange-donotdelete-pr-2zh4qs0w6rau5m', Key='movies.csv')['Body']
# add missing __iter__ method, so pandas accepts body as file-like object
if not hasattr(body, "__iter__"):
    body.__iter__ = types.MethodType(__iter__, body)

movies = pd.read_csv(io.BytesIO(body.read()), encoding='latin1')


movies['year'] = movies.title.str.extract('(\(\d\d\d\d\))', expand=False)
# Removing the parentheses
movies['year'] = movies.year.str.extract('(\d\d\d\d)', expand=False)
# Removing the years from the 'title' column
movies['title'] = movies.title.str.replace('(\(\d\d\d\d\))', '')
# Applying the strip function to get rid of any ending whitespace characters that may have appeared
movies['title'] = movies['title'].apply(lambda x: x.strip())

# Every genre is separated by a | so we simply have to call the split function on |
movies['genres'] = movies.genres.str.split('|')
# Copying the movie dataframe into a new one since we won't need to use the genre information in our first case.
moviesWithGenres = movies.copy()

# For every row in the dataframe, iterate through the list of genres and place a 1 into the corresponding column
for index, row in movies.iterrows():
    for genre in row['genres']:
        moviesWithGenres.at[index, genre] = 1
# Filling in the NaN values with 0 to show that a movie doesn't have that column's genre
moviesWithGenres = moviesWithGenres.fillna(0)

movies.to_csv('movies1.csv')
ratings.to_csv('ratings.csv')
moviesWithGenres.to_csv('moviesWithGenres.csv')