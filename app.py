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
                        "type": "section",
                        "text": {
                            "type": "plain_text",
                            "text": "Click the button below to pick a movie!",
                                "emoji": True
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                        "type": "plain_text",
                                        "text": "Select a Movie!",
                                                "emoji": True
                                },
                                "value": "click_me_123",
                                "action_id": "actionId-0"
                            }
                        ]
                    }
                ]
            }
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.action("actionId-0")
def open_modal(ack, body, client):
    # Acknowledge the command request
    ack()
    # Call views_open with the built-in client
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": "movie-modal-view",
            "title": {"type": "plain_text", "text": "Movie Info"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "movie-selection-block",
                    "element": {
                        "type": "external_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select an item",
                            "emoji": True
                        },
                        "action_id": "movie-selection-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Select a Movie:",
                        "emoji": True
                    }
                }
            ]
        }
    )


@app.view("movie-modal-view")
def handle_view_events(ack, body, logger, client):
    ack()
    logger.info(body)

    user_id = body["user"]["id"]
    # ID of the channel you want to send the message to
    movie_id = body["view"]["state"]["values"]["movie-selection-block"]["movie-selection-action"]["selected_option"]["value"]
    try:
        movie_detail = movie_service.get_movie_detail(movie_id)
        # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel=user_id,
            blocks=[
                {
                    "type": "divider"
                },                
                {
                    "type": "section",
                    "text": {
                            "type": "plain_text",
                        "text": "Here's the movie info you requested!",
                                "emoji": True
                    }
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": movie_detail.get("title"),
                                "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Release date:* {movie_detail.get('release_date')} \n{movie_detail.get('overview')}"
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": movie_detail.get("poster_path"),
                        "alt_text": movie_detail.get("title")
                    }
                }
            ]
        )
        logger.info(result)

    except Exception as e:
        logger.error(f"Error posting message: {e}")


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
