home_screen_view = {
    "type": "home",
    "callback_id": "home-view",

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
                        "action_id": "movie-button-action"
                    }
                ]
            }
    ]
}
