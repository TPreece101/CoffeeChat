from models import Group

def group_option(group):
    return {
        "text": {
            "type": "mrkdwn",
            "text": group.name
        },
        "description": {
            "type": "mrkdwn",
            "text": group.description
        },
        "value": str(group.id)
    }

def get_group_options(user):
    groups = Group.query.all()
    return [group_option(group) for group in groups]


def get_groups_block(user):
    groups = Group.query.all()
    if len(groups) > 0:
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Here are your available groups:"
            },
            "accessory": {
                "type": "checkboxes",
                "options": get_group_options(user),
                "action_id": "group-subscribe-checkbox"
            }
        }
    else:
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Here are your available groups:"
            },
            "text": {
                "type": "mrkdwn",
                "text": "You have no available groups 😢"
            },
        }

def add_group(db, name, description, group_size, week_gap, week_day, time_of_day):
    group = Group(
        name=name,
        description=description,
        group_size=group_size,
        week_gap=week_gap,
        week_day=week_day,
        time_of_day=time_of_day
    )
    db.session.add(group)
    db.session.commit()
    print(f"Group added group id={group.id}")

def delete_group(db, id):
    Group.query.filter_by(id=id).delete()
    db.session.commit()

def get_group(id):
    group = Group.query.filter_by(id=id).first()
    return group

