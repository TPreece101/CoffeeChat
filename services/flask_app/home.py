from groups import get_groups_block
from admin import get_admin_blocks

def get_home_view(db, user):
    return {
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Welcome to Coffee Chat :coffee: \n\n Coffee Chat allows you to subscribe to be put into random coffee chat groups to get to know your collegues better and talk to people that you might not usualy encounter"
                }
            },
            get_groups_block(db, user),
            *get_admin_blocks(user)
        ]
    }