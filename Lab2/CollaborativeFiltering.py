"""
The task is to implement user-based Collaborative Filtering.

We are going to use data stored in MovieLens 100K Dataset.
Url: https://www.kaggle.com/datasets/prajitdatta/movielens-100k-dataset

From the dataset webpage we learn that:
u.data -- The full u data set, 100000 ratings by 943 users on 1682 items.
Each user has rated at least 20 movies. Users and items are numbered consecutively from 1. The data is randomly
ordered. This is a tab separated list of user id | item id | rating | timestamp.

u.item -- Information about the items (movies); this is a tab separated list of
movie id | movie title | release date | video release date | IMDb URL | unknown | Action | Adventure |
Animation | Children's | Comedy | Crime | Documentary | Drama | Fantasy | Film-Noir | Horror | Musical |
Mystery | Romance | Sci-Fi | Thriller | War | Western |
The last 19 fields are the genres, a 1 indicates the movie is of that genre, a 0 indicates it is not; movies can be
in several genres at once. The movie ids are the ones used in the u.data dataset.

Implementation
----------------
First step: Convert the dataset into a user-item matrix (each row will represent a user, and each column will
represent a movie). Nan will mean that user hasn't rated a specific movie.
Second step: Calculate User Similarities - Cosine Similarity
cosine_similarity(A, B) = (A dot B)/(||A|| x ||B||)
Third step: Generate Recommendations
"""
import numpy as np
import pandas as pd

# Load the u.data file
column_names = ['user_id', 'item_id', 'rating', 'timestamp']
data = pd.read_csv('u.data', sep='\t', names=column_names)

# Load u.item file
movie_column_names = ['item_id', 'title', 'release_date', 'video_release_date', 'IMDb_URL', 'unknown', 'Action',
                      'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                      'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
movies = pd.read_csv('u.item', sep='|', names=movie_column_names, usecols=['item_id', 'title'], encoding='ISO-8859-1')

print("First few rows of the dataset:")
print(data.head())

print("First few rows of the dataset:")
print(movies.head())

# Check for any missing values
print("\nMissing values per column:")
print(data.isnull().sum())

# Getting an example movie - rating pair
movie_id = data.loc[123, 'item_id']
rating = data.loc[123, 'rating']
movie_title = movies.loc[movies['item_id'] == movie_id, 'title'].values[0]
print(f"The title of the movie rated in data[123] is: {movie_title}. The rating given to this movie is: {rating}")

# First step
user_item_matrix = data.pivot(index='user_id', columns='item_id', values='rating')
print(user_item_matrix.head())
print(f"Shape of user-item matrix: {user_item_matrix.shape}")

# Second step
def similarity(user, r):
    """
    This functions calculates cosine similarity using the following equation:
    (A, B) = (A dot B)/(||A|| x ||B||)

    :param user: user - a vector representing ratings of specific user
    :param r: r - user-item matrix
    :return: return the similarities list, which contains the cosine similarity values and
    the corresponding user indices for all users compared to the specified user
    """
    similarities = []  # list to store similarities with other users
    for i in range(len(r)):
        dot = np.dot(user, r.iloc[i].values)
        norm_user = np.sqrt(np.dot(user, user))
        norm_i = np.sqrt(np.dot(r.iloc[i].values, r.iloc[i].values))

        if norm_user == 0 or norm_i == 0:
            cosine_similarity = 0
        else:
            cosine_similarity = dot / (norm_user * norm_i)
        similarities.append([cosine_similarity, i])

    return similarities


# Third step
def recommendation(user_id, user_item_matrix, top_n=5, n_recommendations=10):
    """
    This function generates recommendations for a specific user.

    :param user_id:
    :param user_item_matrix:
    :param top_n:
    :param n_recommendations:
    :return:
    """
    user_ratings = user_item_matrix.iloc[user_id - 1].fillna(0).values  # Fill NaN with 0 for calculations

    # Calculate similarities with other users
    user_similarities = similarity(user_ratings, user_item_matrix)

    # Sort by similarity score and get top N similar users
    user_similarities.sort(reverse=True, key=lambda x: x[0])  # Sort by cosine similarity in descending order
    top_similar_users = user_similarities[:top_n]  # Get top N similar users

    # Create a dictionary to store aggregated ratings
    recommendations = {}

    for similarity_score, similar_user_index in top_similar_users:
        similar_user_ratings = user_item_matrix.iloc[similar_user_index]

        # Loop through items rated by similar user
        for item_id, rating in similar_user_ratings.items():
            if user_item_matrix.iloc[user_id - 1][item_id] == 0:  # Only consider items not rated by the target user
                if item_id not in recommendations:
                    recommendations[item_id] = 0  # Initialize if not already in dictionary
                recommendations[item_id] += rating * similarity_score  # Weighted rating

    # Sort recommendations by score
    recommended_movies = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)

    # Get the top N recommendations
    recommended_movie_ids = [movie_id for movie_id, score in recommended_movies[:n_recommendations]]

    return recommended_movie_ids


# Example usage
user_id = 2  # For example, user ID 1
recommended_movie_ids = recommendation(user_id, user_item_matrix)
print(f"Recommended movies for User {user_id}: {recommended_movie_ids}")
