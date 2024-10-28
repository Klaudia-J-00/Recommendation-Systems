"""
The task is to implement user-based Collaborative Filtering.

We are going to use data stored in MovieLens 100K Dataset.
Url: https://www.kaggle.com/datasets/prajitdatta/movielens-100k-dataset
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

# print("First few rows of the dataset:")
# print(data.head())
#
# print("First few rows of the dataset:")
# print(movies.head())
#
# # Check for any missing values
# print("\nMissing values per column:")
# print(data.isnull().sum())

user_item_matrix = data.pivot(index='user_id', columns='item_id', values='rating')
print(user_item_matrix.head())
print(f"Shape of user-item matrix: {user_item_matrix.shape}")


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


def recommendation(u_id, useritem_matrix, top_n=5, n_recommendations=5):
    """
    This function generates recommendations for a specific user.

    :param u_id: user ID
    :param useritem_matrix: user-item matrix
    :param top_n: number of top similar users to consider
    :param n_recommendations: number of recommendations to generate
    :return: list of recommended movie titles
    """
    user_ratings = useritem_matrix.iloc[u_id - 1].fillna(0).values  # Fill NaN with 0 for calculations

    # Calculate similarities with other users
    user_similarities = similarity(user_ratings, useritem_matrix)

    # Sort by similarity score and get top N similar users
    user_similarities.sort(reverse=True, key=lambda x: x[0])  # Sort by cosine similarity in descending order
    top_similar_users = user_similarities[:top_n]  # Get top N similar users

    # Create a dictionary to store aggregated ratings
    recommendations = {}

    for similarity_score, similar_user_index in top_similar_users:
        similar_user_ratings = useritem_matrix.iloc[similar_user_index]

        # Loop through items rated by similar user
        for item_id, rate in similar_user_ratings.items():
            if pd.isna(useritem_matrix.iloc[u_id - 1][item_id]):  # Only consider items not rated by the target user
                if item_id not in recommendations:
                    recommendations[item_id] = 0  # Initialize if not already in dictionary
                recommendations[item_id] += rate * similarity_score  # Weighted rating

    # Sort recommendations by score
    recommended_movies = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)

    # Get the top N recommendations
    recommended_movie_id = [movie_ids for movie_ids, score in recommended_movies[:n_recommendations]]
    recommended_movie_titles = movies[movies['item_id'].isin(recommended_movie_id)]['title'].tolist()

    return recommended_movie_titles

# Example usage
user_id = 2
recommended_movie_ids = recommendation(user_id, user_item_matrix)
print(f"Recommended movies for User {user_id}: {recommended_movie_ids}")