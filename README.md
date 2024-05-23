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
    - You can get you app API keys here: https://www.reddit.com/prefs/apps
    - Modify the `settings.py` file in the project root directory with the following content:
        ```python
        CLIENT_ID = "YOUR_CLIENT_ID_KEY_HERE"
        CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"
        ```

## Usage

1. **Run the Script**:
    ```sh
    python main.py
    ```

2. **Check Results**:
    - The script creates a `results` directory in the project root.
    - Inside the `results` directory, you will find:
        - `posts.xlsx` containing today's top posts.
        - A `comments` subdirectory with individual Excel files for each post's comments.

3. **Recommendation**:
    - Before running the script again, store your results in the `results` folder to avoid overwriting it.

## Considerations

- **Rate Limit**:
    - The Reddit API rate limit is set to 5 minutes (`RATE_LIMIT = 840` seconds, 14 minutes). Therefore, depending on the number of posts and comments, the script may take several minutes to complete.
    - Be patient and allow the script to run to completion. The rate limit ensures the script adheres to Reddit's API usage policies and avoids getting temporarily banned for excessive requests.
