from models import Group, UserSubscription
from collections import namedtuple

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

def get_groups_with_subscriptions(db, user):
    query = f"""
    WITH user_subscriptions AS (
        SELECT user_id, group_id, True AS subscribed
        FROM public.user_subscriptions
        WHERE user_id = '{user}'
    )
    SELECT g.id, g.name, g.description, COALESCE(us.subscribed, false) AS subscribed
    FROM public.groups g
    LEFT JOIN user_subscriptions us 
    ON g.id = us.group_id;
    """
    result = db.session.execute(query)
    Record = namedtuple('Record', result.keys())
    records = [Record(*r) for r in result.fetchall()]
    
    return records

def get_groups_block(db, user):
    groups = get_groups_with_subscriptions(db, user)
    if len(groups) > 0:
        subscribed_groups = list(filter(lambda x: x.subscribed == True, groups))
        if len(subscribed_groups) > 0:
            return {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Here are your available groups:"
                },
                "accessory": {
                    "type": "checkboxes",
                    "options": [group_option(group) for group in groups],
                    "action_id": "group-subscribe-checkbox",
                    "initial_options": [group_option(group) for group in subscribed_groups]
                }
            }
        else:
            return {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Here are your available groups:"
                },
                "accessory": {
                    "type": "checkboxes",
                    "options": [group_option(group) for group in groups],
                    "action_id": "group-subscribe-checkbox",
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
    db.session.merge(group)
    db.session.commit()
    print(f"Group added/updated id={group.id}")

def delete_group(db, id):
    # Delete group
    Group.query.filter_by(id=id).delete()
    # Delete subscriptions
    UserSubscription.query.filter_by(group_id=id).delete()
    db.session.commit()

def get_group(id):
    group = Group.query.filter_by(id=id).first()
    return group

