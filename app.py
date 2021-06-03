import os
from slack_bolt import App
from service.movie import MovieService
from view.home_screen import home_screen_view
from view.movie_selection_modal import movie_selection_view
from view.movie_detail_message import get_movie_detail_message
from conf import SERVER_PORT
import logging

logging.basicConfig(level=logging.INFO)

movie_service = MovieService()

# Initializes app with bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    """This function creates a home tab view from which user can click a button to search movie
    """
    try:
        # pushes a view to the Home tab
        client.views_publish(
            user_id=event["user"],
            view=home_screen_view
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.action("movie-button-action")
def open_modal(ack, body, client):
    """When select movie button is clicked this function will handle it by opening a modal to search movie
    """
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view=movie_selection_view
    )


@app.view("movie-modal-view")
def handle_view_events(ack, body, logger, client):
    """This function handles selected movie from dropdown and retrieves detail for it and sends it to user through DM.
    """
    ack()
    user_id = body["user"]["id"]
    movie_id = body["view"]["state"]["values"]["movie-selection-block"]["movie-selection-action"]["selected_option"]["value"]
    try:
        movie_detail = movie_service.get_movie_detail(movie_id)
        result = client.chat_postMessage(
            channel=user_id,
            blocks=get_movie_detail_message(movie_detail.get("title"), movie_detail.get(
                "poster_path"), movie_detail.get('release_date'), movie_detail.get('overview'))
        )
    except Exception as e:
        logger.error(f"Error posting message: {e}")


@app.options("movie-selection-action")
def show_options(ack, body):
    """This function retrieves movies based on search string and populates dropdown. Support typeahead
    """
    search = body['value']
    options = movie_service.search_movie(search)
    ack(options=options)


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", SERVER_PORT)))
