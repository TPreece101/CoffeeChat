import os
from models import Group

def get_admin_group_blocks(group):
    return [
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"{group.name} \n {group.description}"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"style": "primary",
					"text": {
						"type": "plain_text",
						"text": "Edit",
						"emoji": True
					},
					"value": group.id,
					"action_id": "edit-group"
				},
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Force Group Creation",
                        "emoji": True
                    },
                    "value": group.id,
                    "action_id": "force-group"
                },
				{
					"type": "button",
					"style": "danger",
					"text": {
						"type": "plain_text",
						"text": "Delete",
						"emoji": True
					},
					"value": group.id,
					"action_id": "delete-group"
				}
			]
		}
    ]

def get_admin_blocks(user):
    admin_users = os.environ['ADMIN_USERS'].split(',')
    if user in admin_users:
        groups = Group.query.all()
        nested_blocks = [get_admin_group_blocks(group) for group in groups]
        blocks = [item for sublist in nested_blocks for item in sublist]

        blocks.insert(
            0,
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Admin Section"
                }
            }
        )

        blocks.append(
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "style": "primary",
                        "text": {
                            "type": "plain_text",
                            "text": "Add Group",
                            "emoji": True
                        },
                        "value": "groupid",
                        "action_id": "add-group"
                    }
                ]
            }
        )
        return blocks
    else:
        return []