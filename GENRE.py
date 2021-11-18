import types
import pandas as pd
from botocore.client import Config
import ibm_boto3
import io
from decouple import config

def __iter__(self): return 0

ratings = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies1.csv')
moviesWithGenres = pd.read_csv('moviesWithGenres.csv')

<<<<<<< HEAD
=======
client_dc9ddb978841432ba58f9e610c697598 = ibm_boto3.client(service_name='s3',
    ibm_api_key_id=config('ibm-api-key-id-s3'),
    ibm_auth_endpoint='https://iam.cloud.ibm.com/oidc/token',
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
>>>>>>> 5b26b82830ceaef6db3807d63d738efb179a5215

# # CONTENT BASED SOLUTION

def define_existing_user_profile(user_id):
    user_num = user_id
    ratings_users = ratings.loc[ratings['user_id'] == user_num]
    moviesid = movies[movies['movie_id'].isin(ratings_users['movie_id'].tolist())]

    # Then merging it so we can get the movieId. It's implicitly merging it by title.
    global inputMovies
    inputMovies = pd.merge(moviesid, ratings_users, how='right', on=['movie_id'])

    # Create the user profile
    inputMovies = inputMovies[['movie_id', 'title', 'genres', 'rating']]
    # Filtering out the movies from the input
    userMovies = moviesWithGenres[moviesWithGenres['movie_id'].isin(inputMovies['movie_id'].tolist())]


    # Resetting the index to avoid future issues
    userMovies = userMovies.reset_index(drop=True)
    # Dropping unnecessary issues due to save memory and to avoid issues
    global userGenreTable
    userGenreTable = userMovies.drop('movie_id', 1).drop('title', 1).drop('genres', 1).drop('year', 1)

    # Dot produt to get weights
    global userProfile
    userProfile = userGenreTable.transpose().dot(inputMovies['rating'])

    return userProfile


def recommend_top_5_existing_user(user_id):
    # Get user profile
    userProfile = define_existing_user_profile(user_id)
    # Now let's get the genres of every movie in our original dataframe
    genreTable = moviesWithGenres.set_index(moviesWithGenres['movie_id'])
    # And drop the unnecessary information
    genreTable = genreTable.drop('movie_id', 1).drop('title', 1).drop('genres', 1).drop('year', 1)

    # Multiply the genres by the weights and then take the weighted average
    recommendationTable_df = ((genreTable * userProfile).sum(axis=1)) / (userProfile.sum())

    # Sort our recommendations in descending order
    recommendationTable_df = recommendationTable_df.sort_values(ascending=False)

    # The final recommendation table
    return movies.loc[movies['movie_id'].isin(recommendationTable_df.head(5).keys())]

if __name__ == '__main__':
    recommendation_result = recommend_top_5_existing_user(10)
    recommendation_result.drop(columns=['movie_id'], inplace=True)
    recommendation_result.index = range(1, 6)
    print(recommendation_result)
