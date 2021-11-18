import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from decouple import config
import types
from botocore.client import Config
import ibm_boto3
import io

endpoint_dc9ddb978841432ba58f9e610c697598 = 'https://s3.eu.cloud-object-storage.appdomain.cloud'

client_dc9ddb978841432ba58f9e610c697598 = ibm_boto3.client(service_name='s3',
    ibm_api_key_id=config('ibm-api-key-id-s3'),
    ibm_auth_endpoint="https://iam.cloud.ibm.com/oidc/token",
    config=Config(signature_version='oauth'),
    endpoint_url=endpoint_dc9ddb978841432ba58f9e610c697598)

body = client_dc9ddb978841432ba58f9e610c697598.get_object(Bucket='mvpteamorange-donotdelete-pr-2zh4qs0w6rau5m', Key='final_dataset.csv')['Body']
# add missing __iter__ method, so pandas accepts body as file-like object
if not hasattr(body, "__iter__"):
    body.__iter__ = types.MethodType(__iter__, body)

final_dataset = pd.read_csv(body, index_col=0)

body = client_dc9ddb978841432ba58f9e610c697598.get_object(Bucket='mvpteamorange-donotdelete-pr-2zh4qs0w6rau5m', Key='movies2.csv')['Body']
# add missing __iter__ method, so pandas accepts body as file-like object
if not hasattr(body, "__iter__"):
    body.__iter__ = types.MethodType(__iter__, body)

movies = pd.read_csv(body, index_col=0)

csr_data = csr_matrix(final_dataset.values)
final_dataset.reset_index(inplace=True)

knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
knn.fit(csr_data)


#pipeline = Pipeline(steps=[(('knn', knn))])
#model = pipeline.fit(csr_data)

def get_movie_recommendation(movie_name):
    n_movies_to_reccomend = 10
    movie_list = movies[movies['title'].str.contains(movie_name)]
    if len(movie_list):
        movie_idx = movie_list.iloc[0]['movie_id']
        movie_idx = final_dataset[final_dataset['movie_id'] == movie_idx].index[0]
        distances, indices = knn.kneighbors(csr_data[movie_idx], n_neighbors=n_movies_to_reccomend + 1)
        rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
        recommend_frame = []
        for val in rec_movie_indices:
            movie_idx = final_dataset.iloc[val[0]]['movie_id']
            idx = movies[movies['movie_id'] == movie_idx].index
            recommend_frame.append({'Title': movies.iloc[idx]['title'].values[0], 'Distance': val[1]})
        df = pd.DataFrame(recommend_frame, index=range(1, n_movies_to_reccomend + 1))
        return df
    else:
        return "No movies found. Please check your input"

if __name__ == "__main__":
  print(get_movie_recommendation('Hercules'))
