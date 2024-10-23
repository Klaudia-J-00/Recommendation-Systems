"""
The task is to use Web Scrapping to get information from a website of choice, that has ratings, and users.

We need to fetch information about:
- Movie/Game/Book etc. ID - movie_id
- It's link - movie_link
- It's title - movie_title
- General User Rating of that Movie/Game/Book etc. - general_rating (since we chose Steam we will also include recent rating)
- Recent User Rating of that Movie/Game/Book etc. - recent_rating
- Specific User Rating of that Movie/Game/Book etc. - user_rating
- User ID - user_id

Fetched information should be saved in .txt or .csv file.

Website: https://store.steampowered.com/
Steam has a detailed review system for games, with each review tied to a specific user.
User reviews: Reviews are detailed with specific user ratings (thumbs up/down).
"""
import csv
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
# because the page is dynamically loaded we will use selenium to get the page content
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

import time
load_dotenv()
driver_path = os.getenv('EDGE_DRIVER_PATH')


# ----------------- STEAM 3 -----------------
multiplayer_url = 'https://store.steampowered.com/search/?category2=27'

# Request the page
response = requests.get(multiplayer_url)
game_links = []

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all game links on the page
    for link in soup.find_all('a', class_='search_result_row'):
        game_link = link['href']
        # Parse the URL and rebuild it without query parameters (we want clear URL's)
        trimmed_link = game_link.split('?')[0]
        game_links.append(trimmed_link)
else:
    print("Failed to retrieve the multiplayer category page.")

user_ratings = []
processed_users = {}

for i, link in enumerate(game_links):
    # if i >= 2:
    #     break we can use that to limit the number of games we want to scrape

    game_url = link # we replaced the link to the specific game with the link from game_links list

    # steam reviews are divided into recent and all reviews, we are interested in all reviews
    # 80% review means 80% of users liked the game
    response = requests.get(game_url)

    if response.status_code == 200:  # if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')  # parse the html content of the page

        # get the title of the game
        game_title = soup.find('div', class_='apphub_AppName').text.strip()
        # get the game id
        game_id = game_url.split('/')[-3]
        print(f'Title: {game_title}, game_id: {game_id}')  # the id is the number in the url

        # get the total percentage of positive reviews
        all_reviews = soup.find_all('span', class_='game_review_summary')

        if soup.find('div', class_='game_area_dlc_bubble') or len(all_reviews) == 0: # we skip DLC's because there are no reviews for them and Selenium will throw an error
            print(f'Skip Game: {game_url}')
            continue

        if len(all_reviews) > 1:
            recent_rating = all_reviews[0].text.strip()  # The first 'game_review_summary' is usually for recent reviews
            general_rating = all_reviews[1].text.strip()  # The second 'game_review_summary' is usually for all reviews
            print(f'General User Rating (All Reviews): {general_rating}, Recent User Rating: {recent_rating}')
        else:
            general_rating, recent_rating = "No rating", "No rating"

        reviews_link = f'https://steamcommunity.com/app/{game_id}/reviews/'
        print(f'Link to reviews: {reviews_link}')

        options = Options()
        options.headless = True  # Run in headless mode
        driver = webdriver.Edge(service=Service(driver_path), options=options)  # path to msedgedriver.exe

        driver.get(reviews_link)
        time.sleep(2)  # Wait for the page to load
        current_url = driver.current_url
        if current_url != reviews_link:
            print(f'Skip Game: {game_url} (Redirected to: {current_url})')
            driver.quit()  # Quit the driver for this game
            continue  # Skip this game

        # Initialize the set of processed users for the current game
        if game_id not in processed_users:
            processed_users[game_id] = set()

        # Simulate scrolling to load more reviews
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_count = 10  # Number of times to scroll

        while scroll_count > 0:  # we won't fetch all reviews cause of runtime, to fetch all we need to change to while True
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for more reviews to load

            # Check if the page height has changed
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # Exit the loop if no more reviews are loaded

            last_height = new_height

            soup = BeautifulSoup(response.text, 'html.parser')

            review_cards = driver.find_elements(By.CLASS_NAME, 'apphub_Card')

            if not review_cards:
                break  # If there are no more reviews, stop

            for card in review_cards:
                author_block = card.find_element(By.CLASS_NAME, 'apphub_friend_block_container')
                if author_block:
                    profile_link = author_block.find_element(By.TAG_NAME, 'a').get_attribute(
                        'href')  # User profile link
                    user_id = profile_link.split('/')[-2]  # Extract user ID from the URL
                    # there are two types of links to user profiles, one is /profile/id and the other is /id/nickname,
                    # it's because steam allows to set custom url, steam doesn't allow two users to have the same custom url,
                    # so we will treat that as a user id as well

                    # to avoid duplicates
                    # Check if the user has already rated this game
                    if user_id in processed_users[game_id]:
                        continue  # Skip this user if already processed

                    # Add user_id to the set of processed users for this game
                    processed_users[game_id].add(user_id)
                else:
                    user_name = "Unknown"
                    user_id = "Unknown"
                    profile_link = "Unknown"

                # user rating
                rating_block = card.find_element(By.CLASS_NAME, 'apphub_UserReviewCardContent')
                if rating_block:
                    user_rating = rating_block.find_element(By.CLASS_NAME,
                                                            'title').text.strip()  # user rating on steam can be Recommended or Not Recommended
                else:
                    user_rating = "No rating"

                user_ratings.append(
                    [game_id, game_title, game_url, general_rating, recent_rating, user_rating, user_id, profile_link]
                )

            scroll_count -= 1

        print(len(user_ratings))

# Save data to CSV files
# 1. reviews.csv
with open('reviews.csv', mode='w', newline='', encoding='utf-8') as reviews_file:
    reviews_writer = csv.writer(reviews_file)
    reviews_writer.writerow(['user_id', 'game_id', 'user_rating'])  # Header
    for rating in user_ratings:
        reviews_writer.writerow([rating[6], rating[0], rating[5]])  # user_id, game_id, user_rating

# 2. user.csv
with open('user.csv', mode='w', newline='', encoding='utf-8') as user_file:
    user_writer = csv.writer(user_file)
    user_writer.writerow(['user_id', 'profile_link'])  # Header
    unique_users = {rating[6]: rating[7] for rating in user_ratings}  # Create a unique user dictionary
    for user_id, profile_link in unique_users.items():
        user_writer.writerow([user_id, profile_link])  # user_id, profile_link

# 3. game.csv
with open('game.csv', mode='w', newline='', encoding='utf-8') as game_file:
    game_writer = csv.writer(game_file)
    game_writer.writerow(['game_id', 'game_title', 'game_url', 'general_rating', 'recent_rating'])  # Header
    unique_games = {rating[0]: [rating[1], rating[2], rating[3], rating[4]] for rating in user_ratings}
    for game_id, data in unique_games.items():
        game_writer.writerow([game_id] + data)  # game_id, game_title, game_url, general_rating, recent_rating
