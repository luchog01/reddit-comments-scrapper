# Reddit Comments Scrapper

This project is a Reddit scraper that collects the top posts of the day from the selected subreddit and their respective comments, saving them into Excel files.

## Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/luchog01/reddit-comments-scrapper.git
    cd pickleball-scraper
    ```

2. **Create and Activate a Virtual Environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set Up Configuration**:
    - You can get your app API keys here: [Reddit Apps](https://www.reddit.com/prefs/apps)
    - Modify the `settings.py` file in the project root directory with the following content:
        ```python
        CLIENT_ID = "YOUR_CLIENT_ID_KEY_HERE"
        CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"
        TARGET_SUBREDDIT = "pickleball"  # Target subreddit
        ```

## Usage

1. **Run the Script**:
    ```sh
    python main.py
    ```

2. **Check Results**:
    - The script creates a `results` directory in the project root.
    - Inside the `results` directory, you will find:
        - `posts.xlsx` containing all obtained posts.
        - `comments.xlsx` containing comments for the collected posts.

3. **Recommendation**:
    - The results will be appended to the existing Excel files. If duplicates are found, the newer version will be kept.

## Considerations

- **Rate Limit**:
    - The Reddit API rate limit is set to 5 minutes (`RATE_LIMIT = 840` seconds, 14 minutes). Depending on the number of posts and comments, the script may take several minutes to complete.
    - Be patient and allow the script to run to completion. The rate limit ensures the script adheres to Reddit's API usage policies and avoids getting temporarily banned for excessive requests.