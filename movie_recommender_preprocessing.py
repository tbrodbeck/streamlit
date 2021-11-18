from decouple import config
import types
import pandas as pd
from botocore.client import Config
import ibm_boto3
import io
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline

def __iter__(self): return 0

# @hidden_cell
# The following code accesses a file in your IBM Cloud Object Storage. It includes your credentials.
# You might want to remove those credentials before you share the notebook.


endpoint_dc9ddb978841432ba58f9e610c697598 = 'https://s3.eu.cloud-object-storage.appdomain.cloud'

client_dc9ddb978841432ba58f9e610c697598 = ibm_boto3.client(service_name='s3',
    ibm_api_key_id=config('ibm-api-key-id-s3'),
    ibm_auth_endpoint="https://iam.cloud.ibm.com/oidc/token",
    config=Config(signature_version='oauth'),
    endpoint_url=endpoint_dc9ddb978841432ba58f9e610c697598)

body = client_dc9ddb978841432ba58f9e610c697598.get_object(Bucket='mvpteamorange-donotdelete-pr-2zh4qs0w6rau5m', Key='users.csv')['Body']
# add missing __iter__ method, so pandas accepts body as file-like object
if not hasattr(body, "__iter__"):
    body.__iter__ = types.MethodType(__iter__, body)

users = pd.read_csv(body, index_col=0)
users_list = users['user_id']

body = client_dc9ddb978841432ba58f9e610c697598.get_object(Bucket='mvpteamorange-donotdelete-pr-2zh4qs0w6rau5m', Key='ratings.csv')['Body']
# add missing __iter__ method, so pandas accepts body as file-like object
if not hasattr(body, "__iter__"):
    body.__iter__ = types.MethodType(__iter__, body)

ratings = pd.read_csv(body, index_col=0)


ratings.groupby(['movie_id'])['rating'].count().sort_values(ascending=True)

# Every row in the ratings dataframe has a user id associated with at least one movie, a rating and a timestamp showing when they reviewed it. We won't be needing the timestamp, user_emb_id and movie_emb_id column, so let's drop it to save on memory.
# Drop removes a specified row or column from a dataframe
ratings = ratings.drop(['timestamp', 'user_emb_id', 'movie_emb_id'], axis=1)

# ## MOVIES
body = client_dc9ddb978841432ba58f9e610c697598.get_object(Bucket='mvpteamorange-donotdelete-pr-2zh4qs0w6rau5m', Key='movies.csv')['Body']
# add missing __iter__ method, so pandas accepts body as file-like object
if not hasattr(body, "__iter__"):
    body.__iter__ = types.MethodType(__iter__, body)

movies = pd.read_csv(io.BytesIO(body.read()), encoding='latin1')

# Let's also remove the year from the **title** column by using pandas' replace function and store in a new **year** column.
# Using regular expressions to find a year stored between parentheses
# We specify the parantheses so we don't conflict with movies that have years in their titles
movies['year'] = movies.title.str.extract('(\(\d\d\d\d\))', expand=False)
# Removing the parentheses
movies['year'] = movies.year.str.extract('(\d\d\d\d)', expand=False)
# Removing the years from the 'title' column
movies['title'] = movies.title.str.replace('(\(\d\d\d\d\))', '')
# Applying the strip function to get rid of any ending whitespace characters that may have appeared
movies['title'] = movies['title'].apply(lambda x: x.strip())
titles = list(movies['title'])

# Every genre is separated by a | so we simply have to call the split function on |
movies['genres'] = movies.genres.str.split('|')

# Since keeping genres in a list format isn't optimal for the content-based recommendation system technique, we will use the One Hot Encoding technique to convert the list of genres to a vector where each column corresponds to one possible value of the feature. This encoding is needed for feeding categorical data. In this case, we store every different genre in columns that contain either 1 or 0. 1 shows that a movie has that genre and 0 shows that it doesn't. Let's also store this dataframe in another variable since genres won't be important for our first recommendation system.
# Copying the movie dataframe into a new one since we won't need to use the genre information in our first case.
# moviesWithGenres = movies.copy()

# # For every row in the dataframe, iterate through the list of genres and place a 1 into the corresponding column
# for index, row in movies.iterrows():
#     for genre in row['genres']:
#         moviesWithGenres.at[index, genre] = 1
# # Filling in the NaN values with 0 to show that a movie doesn't have that column's genre
# moviesWithGenres = moviesWithGenres.fillna(0)


# movies_merged = movies.merge(ratings, on='movie_id')

# # ## Average Ratings & Rating Count

# movies_average_rating = movies_merged.groupby('title')['rating'].mean().sort_values(ascending=False).reset_index().rename(columns={'rating': 'Average Rating'})


# movies_rating_count = movies_merged.groupby('title')['rating'].count().sort_values(ascending=True).reset_index().rename(columns={'rating': 'Rating Count'})  # ascending=False
# movies_rating_count_avg = movies_rating_count.merge(movies_average_rating, on='title')

final_dataset = ratings.pivot(index='movie_id', columns='user_id', values='rating')
final_dataset.fillna(0, inplace=True)


no_user_voted = ratings.groupby('movie_id')['rating'].agg('count')
no_movies_voted = ratings.groupby('user_id')['rating'].agg('count')

final_dataset = final_dataset.loc[no_user_voted[no_user_voted > 10].index, :]
final_dataset = final_dataset.loc[:, no_movies_voted[no_movies_voted > 50].index]

final_dataset.to_csv('final_dataset.csv')
movies.to_csv('movies2.csv')
