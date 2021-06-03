movie_selection_view = {
    "type": "modal",
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
