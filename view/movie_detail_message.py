def get_movie_detail_message(title, image_url, release_date, overview):
    message_block = [
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
                "text": title,
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Release date:* {release_date} \n{overview}"
            },
            "accessory": {
                "type": "image",
                "image_url": image_url,
                "alt_text": title
            }
        }
    ]
    return message_block
