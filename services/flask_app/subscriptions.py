from operator import sub
from models import UserSubscription

def get_subscribed_groups(user_id):
    subscribed_groups = UserSubscription.query.filter_by(user_id=user_id).all()
    return {group.group_id for group in subscribed_groups}

def get_subscribed_users(group_id):
    subscribed_users = UserSubscription.query.filter_by(group_id=group_id).all()
    return [user.user_id for user in subscribed_users]

def update_subscriptions(db, selected_groups, user_id):
    # Get subscribed groups
    subscribed_groups = get_subscribed_groups(user_id)

    # Find missing from subscribed
    miss_from_table = selected_groups - subscribed_groups
    # Add to table
    for sub in miss_from_table:
        subscription = UserSubscription(
            user_id=user_id,
            group_id=sub,
        )
        db.session.add(subscription)

    # Find missing from selected
    miss_from_selected = subscribed_groups - selected_groups
    # Remove from table
    for sub in miss_from_selected:
        subscription = UserSubscription.query.filter_by(user_id=user_id, group_id=sub).first()
        db.session.delete(subscription)
    
    db.session.commit()


def parse_subscribe_actions(actions:list):
    return {option.get('value') for option in actions[0].get('selected_options')}