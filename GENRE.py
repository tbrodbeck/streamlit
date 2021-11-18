import types
import pandas as pd
from botocore.client import Config
import ibm_boto3
import io

def __iter__(self): return 0

ratings = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies1.csv')
moviesWithGenres = pd.read_csv('moviesWithGenres.csv')


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
