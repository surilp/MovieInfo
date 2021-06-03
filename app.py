import os
# Use the package we installed
from slack_bolt import App
from movie import MovieService
import logging

logging.basicConfig(level=logging.INFO)


movie_service = MovieService()

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        # views.publish is the method that your app uses to push a view to the Home tab
        client.views_publish(
            # the user that opened your app's app home
            user_id=event["user"],
            # the view object that appears in the app home
            view={
                "type": "home",
                "callback_id": "home-view",

                # body of the view
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "*Welcome to Movie Info!:tada:*",
                            "emoji": True
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "block_id": "multi-selection-block",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Select a movie:"
                        },
                        "accessory": {
                            "type": "external_select",
                            "action_id": "movie-selection-action",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select an item",
                                "emoji": True
                            }
                        }
                    }
                ]
            }
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.options("movie-selection-action")
def show_options(ack, body):
    search = body['value']
    options = movie_service.search_movie(search)
    ack(options=options)


@app.action("movie-selection-action")
def show_options(ack, body):
    ack()
    # print(body)


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
