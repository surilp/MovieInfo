# MovieInfo

Steps to building movie info app

* Setting up Ngrok for local testing
    1. Download zip file and extract it from https://ngrok.com/ 
    2. Extract it to /usr/local/bin
    3. tunnel your server by running - ngrok http {PORT}

* Create TMDB account to access TMDB API and generate API key from https://www.themoviedb.org/

* Follow instruction to set up starter python bolt project - https://slack.dev/bolt-python/tutorial/getting-started

* Build Slack UI blocks using [BlockKit Builder](https://app.slack.com/block-kit-builder)


Run App

1. Make sure ngrok is running
2. Copy URL provided in ngrok execution terminal to Interactive & Shortcuts (Request URL and Select Menus) and Event Subscription (Request URL)
3. Make sure Key and Token are available in in environment. Update them in start.sh file
   - export SLACK_BOT_TOKEN={xoxb-TOKEN}
   - export SLACK_SIGNING_SECRET={SECRET}
   - export MOVIE_API_KEY={API_KEY}
4. Make sure python environment is available (If not available run python -m venv .venv in root of project[/MovieInfo])
5. Install dependent packages by running -> pip install -r requirements.txt
6. run ./start.sh