"""
Script to count the number of items in the reviews.csv, user.csv, and game.csv files
"""

import csv

# Count the number of items in the reviews.csv file
with open('reviews.csv', mode='r', encoding='utf-8') as reviews_file:
    reviews_reader = csv.reader(reviews_file)
    reviews = list(reviews_reader)
    num_reviews = len(reviews) - 1  # Subtract 1 for the header

    print(f'Number of items in reviews.csv: {num_reviews}')

# Count the number of items in the user.csv file
with open('user.csv', mode='r', encoding='utf-8') as user_file:
    user_reader = csv.reader(user_file)
    users = list(user_reader)
    num_users = len(users) - 1  # Subtract 1 for the header

    print(f'Number of items in user.csv: {num_users}')

# Count the number of items in the game.csv file
with open('game.csv', mode='r', encoding='utf-8') as game_file:
    game_reader = csv.reader(game_file)
    games = list(game_reader)
    num_games = len(games) - 1  # Subtract 1 for the header

    print(f'Number of items in game.csv: {num_games}')