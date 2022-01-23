import os
import json
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete

load_dotenv()

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:
    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      user_id=event['user'],
      # the view object that appears in the app home
      view=get_home_view(event['user'])
    )
  
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

@app.action("group-subscribe-checkbox")
def group_subscribe_action(ack, body, logger):
    ack()
    logger.info(body)

@app.action("add-group")
def add_group_action(ack, body, client):
    ack()
    view_id = body.get('view').get('id')
    view_hash = body.get('view').get('hash')
    client.views_open(
        trigger_id = body['trigger_id'],
        view = get_group_modal_view(private_metadata=json.dumps({'view_id':view_id, 'hash':view_hash})),
    )

@app.view("edit_group_modal")
def handle_edit_group_modal_view_events(ack, body, client, logger):
    ack()
    add_group(db=db, **parse_group_modal_view(body.get('view')))
    logger.info(body)
    private_metadata = json.loads(body.get('view').get('private_metadata'))

    client.views_update(
        view_id=private_metadata.get('view_id'),
        hash=private_metadata.get('hash'),
        view = get_home_view(body.get('user').get('id'))
    )

@app.action("delete-group")
def handle_delete_group_action(ack, body, client, logger):
    ack()
    id_to_delete = body.get('actions')[0].get('value')
    delete_group(db, id_to_delete)
    logger.info(body)

    client.views_update(
        view_id=body.get('view').get('id'),
        hash=body.get('view').get('hash'),
        view=get_home_view(body.get('user').get('id'))
    )

@app.action("edit-group")
def handle_edit_group_action(ack, body, client, logger):
    ack()
    logger.info(body)
    view_id = body.get('view').get('id')
    view_hash = body.get('view').get('hash')
    
    # Get details from db
    group_id = body.get('actions')[0].get('value')
    group = get_group(group_id)
    
    client.views_open(
        trigger_id = body['trigger_id'],
        view = get_group_modal_view(
            name=group.name,
            description=group.description,
            group_size=str(group.group_size),
            week_gap=str(group.week_gap),
            week_day=group.week_day,
            time_of_day=group.time_of_day.strftime(format='%H:%M'),
            private_metadata=json.dumps({'view_id':view_id, 'hash':view_hash})
        ),
    )

@app.action("modal_group_size")
def handle_modal_group_size(ack, body, logger):
    ack()
    logger.info(body)

@app.action("modal_week_gap")
def handle_modal_week_gap(ack, body, logger):
    ack()
    logger.info(body)

@app.action("modal_week_day")
def handle_modal_week_day(ack, body, logger):
    ack()
    logger.info(body)

# Flask stuff
flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@docker.local'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(flask_app)
handler = SlackRequestHandler(app)

from groups import add_group, delete_group, get_group
from home import get_home_view
from group_modal import get_group_modal_view, parse_group_modal_view

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@flask_app.route("/slack/interaction", methods=["POST"])
def slack_interaction():
    return handler.handle(request)
