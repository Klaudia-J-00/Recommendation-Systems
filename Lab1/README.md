# Steam Multiplayer Game Reviews - Data Scraping

## Overview 
This project involves data scraping from the Steam platform, specifically focusing on multiplayer games. The data collected includes game ratings, reviews, and user information.
* **Data Source**: Steam platform https://store.steampowered.com/
* **Data Scraping Tool**: Python
* **Category Scraped**: Multiplayer Games https://store.steampowered.com/search/?category2=27
Since Steam is a massive platform with thousands of games, this project only captures data from a subset of games within the multiplayer category.

## Steam Reviews System 
On Steam, games are reviewed through a thumbs-up/thumbs-down system. A game's rating consists of two key factors:
1. Percentage of positive reviews
2. Total number of reviews

The following table breaks down the rating system:

| score in % | reviews      | rating   | confidence     |
|------------|--------------|----------|----------------|
| 95 - 100   | 500+ reviews | positive | overwhelmingly |
| 85 - 100   | 50+ reviews  | positive | very           |
| 80 - 100   | 10+ reviews  | positive | -              |
| 70 - 79    | 10+ reviews  | positive | mostly         |
| 40 - 69    | 10+ reviews  | mixed    | -              |
| 20 - 39    | 10+ reviews  | negative | mostly         |
| 0 - 19     | 10+ reviews  | negative | -              |
| 0 - 19     | 50+ reviews  | negative | very           |
| 0 - 19     | 500+ reviews | negative | overwhelmingly |

## Review Categories 
Steam provides two types of game ratings:

* **General Rating:** The rating based on all reviews ever submitted.
* **Recent Rating:** The rating based on reviews from the last 30 days.
This distinction is important because games can evolve over time. A game that was considered excellent a decade ago might no longer meet today's standards due to changes in the market.

## Data Scraping Process
The data scraping process involves the following steps:
1. **Collect Game Links** - We first scrape the Steam multiplayer games page to collect links to individual game pages.
`multiplayer_url = 'https://store.steampowered.com/search/?category2=27'
2. **Extract Game Information** - For each game, we extract the following information:
   * Game Title
   * Game ID 
   * General Rating
   * Recent Rating
   
   We then navigate to the Steam reviews section using Selenium, and simulate scrolling to load additional reviews.
3. **Extrac User Ratings** - For each review, we extract the user ID and their rating (Recommended/Not Recommended). To avoid duplicates, we track users already processed for each game.
4. **Extract User Information** - For each user, we extract the user ID and their Steam profile link.
5. **Save Data** - Once the data is collected, we save it into separate CSV files:
   * game.csv: Contains information about games.
   * reviews.csv: Contains the individual user reviews.
   * user.csv: Contains user profile information.

## Files Generated 
The data is saved in three different CSV files, each containing specific information related to the games, reviews, and users:

1. game.csv
   * **Headers:** game_id, game_title, game_url, general_rating, recent_rating
   * **Description:** Contains the game ID, title, link to the game page, overall user rating, and the rating from recent reviews.
2. **reviews.csv**  
   &nbsp;&nbsp;&nbsp;&nbsp;**Headers:** user_id, game_id, user_rating  
   &nbsp;&nbsp;&nbsp;&nbsp;**Description:** Contains user reviews for each game with the rating provided by the user.
3. user.csv
   * **Headers**: user_id, profile_link
   * **Description**: Contains the user ID and the link to the user's Steam profile. Steam allows users to create custom URLs for their profiles, so some user IDs may be strings instead of numerical IDs. However, these custom URLs are unique and can still be used to identify individual users.

## Data Collection Summary 
The data was collected for the first 50 multiplayer games listed on Steam, although some games were skipped due to missing reviews (for example, games that were not yet released or DLCs that lacked individual reviews).

For each game, a maximum of 110 reviews was scraped to reduce the time required for data collection. As a result, the dataset is a partial representation of Steam's review system, including only a fraction of the available games and their reviews.
* **Total Games Scraped:** 34
* **Total Reviews Scraped:** 3430
* **Total Users Scraped:** 3407

## Conclusion
This project provides a snapshot of user reviews for multiplayer games on Steam, focusing on both general and recent ratings. The data collected offers insights into user satisfaction and game performance over time, while highlighting individual user ratings and their respective profiles.