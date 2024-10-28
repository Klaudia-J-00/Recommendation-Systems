# User-Based Collaborative Filtering with MovieLens 100K Dataset

This project implements a user-based Collaborative Filtering recommendation system using the MovieLens 100K Dataset. The goal is to generate personalized movie recommendations for users based on the ratings from similar users.

## Dataset Information

We use the MovieLens 100K Dataset, which contains:
- `u.data` – 100,000 ratings by 943 users on 1,682 movies, with each user rating at least 20 movies.
- `u.item` – Movie metadata, including titles and genres.

Dataset can be downloaded from [Kaggle](https://www.kaggle.com/datasets/prajitdatta/movielens-100k-dataset).

**Files Used:**
- **`u.data`**: Contains user ratings for movies, in the format `user_id | item_id | rating | timestamp`.
- **`u.item`**: Contains movie information, including `movie_id | title`.

## Implementation Overview

### Steps

1. **Convert Data into User-Item Matrix**: We pivot the data to create a matrix with users as rows and movies as columns, where each cell contains a user’s rating for a movie. NaN values indicate movies the user hasn’t rated.

2. **Calculate User Similarities (Cosine Similarity)**:
   The similarity between two users is calculated using cosine similarity:

   - cosine_similarity(A, B) = (A • B) / (||A|| * ||B||)

   where A and B are vectors representing the ratings of two users.

3. **Generate Recommendations**: Based on similarity scores, we find the top similar users, aggregate their ratings for movies the target user hasn’t rated, and generate a recommendation list.

### Requirements

Install the required packages:
```bash
pip install numpy pandas
```