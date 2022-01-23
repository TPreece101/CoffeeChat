from datetime import time

def get_options_from_list(options_list):
    return [
        {
            "text": {
                "type": "plain_text",
                "text": option,
                "emoji": True
            },
            "value": option
        }
        for option in options_list
    ]

def get_static_select_accessory(action_id, option_list, selected_option=None):
    if selected_option is None:
        return {
                    "type": "static_select",
                    "action_id": action_id,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Choose list",
                        "emoji": True
                    },
                    "options": get_options_from_list(option_list)
        }
    else:
        if selected_option in option_list:
            return {
                    "type": "static_select",
                    "action_id": action_id,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Choose list",
                        "emoji": True
                    },
                    "options": get_options_from_list(option_list),
                    "initial_option": {
                        "text": {
                            "type": "plain_text",
                            "text": selected_option,
                        },
                        "value": selected_option
                    }
            }
        else:
            raise Exception(f'Option:{selected_option} not in list: {option_list}')

def get_input_element(action_id, placeholder_text, initial_value=None, multiline=False):
    if initial_value is None:
        return {
                    "type": "plain_text_input",
                    "action_id": action_id,
                    "multiline": multiline,
                    "placeholder": {
                        "type": "plain_text",
                        "text": placeholder_text
                    }
        }
    else:
        return {
                    "type": "plain_text_input",
                    "action_id": action_id,
                    "multiline": multiline,
                    "placeholder": {
                        "type": "plain_text",
                        "text": placeholder_text
                    },
                    "initial_value": initial_value
        }

def get_time_element(action_id, placeholder_text, time_of_day=None):
    if time_of_day is None:
        return {
                    "type": "timepicker",
                    "placeholder": {
                        "type": "plain_text",
                        "text": placeholder_text,
                        "emoji": True
                    },
                    "action_id": action_id
        }
    else:
        return {
                    "type": "timepicker",
                    "placeholder": {
                        "type": "plain_text",
                        "text": placeholder_text,
                        "emoji": True
                    },
                    "action_id": action_id,
                    "initial_time": time_of_day
        }

def get_group_modal_view(name=None, description=None, group_size=None, week_gap=None, week_day=None, time_of_day=None, private_metadata=None):
    return {
        "type": "modal",
        "callback_id": "edit_group_modal",
        "private_metadata":private_metadata,
        "title": {"type": "plain_text", "text": "Add/Edit Group"},
        "submit": {"type": "plain_text", "text": "Submit"},
        "blocks":[
            {
                "type": "input",
                "block_id": "modal_group_name_block",
                "element": get_input_element("modal_group_name", "What would you like your group to be called?", name),
                "label": {
                    "type": "plain_text",
                    "text": "Group Name",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "block_id": "modal_group_description_block",
                "element": get_input_element("modal_group_description", "Tell us about your group", description, True),
                "label": {
                    "type": "plain_text",
                    "text": "Group Description",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "block_id": "modal_group_size_block",
                "text": {
                    "type": "mrkdwn",
                    "text": ":people_holding_hands: *Number of people*\nHow many people should be in each random group?"
                },
                "accessory": get_static_select_accessory("modal_group_size", ["2", "3", "4", "5", "6", "7", "8", "9", "10"], group_size)
            },
            {
                "type": "section",
                "block_id": "modal_week_gap_block",
                "text": {
                    "type": "mrkdwn",
                    "text": ":straight_ruler: *Weeks between*\nHow many weeks between each random group assignment?"
                },
                "accessory": get_static_select_accessory("modal_week_gap", ["1","2", "3", "4", "5", "6"], week_gap)
            },
            {
                "type": "section",
                "block_id": "modal_week_day_block",
                "text": {
                    "type": "mrkdwn",
                    "text": ":date: *Day of the week*\nWhat day of the week should random groups be assigned?"
                },
                "accessory": get_static_select_accessory("modal_week_day", ["Monday","Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], week_day)
            },
            {
                "type": "input",
                "block_id": "modal_time_of_day_block",
                "element": get_time_element("modal_time_of_day", "Select time", time_of_day),
                "label": {
                    "type": "plain_text",
                    "text": "Time of day for group assignment",
                    "emoji": True
                }
            }
        ]
    }

def get_element_state(element_name, state_values):
    return state_values.get(f'modal_{element_name}_block').get(f'modal_{element_name}')

def parse_group_modal_view(view:dict):
    state_values = view.get('state').get('values')

    return {
        'name' :get_element_state('group_name', state_values).get('value'),
        'description' : get_element_state('group_description', state_values).get('value'),
        'group_size' : int(get_element_state('group_size', state_values).get('selected_option').get('value')),
        'week_gap' : int(get_element_state('week_gap', state_values).get('selected_option').get('value')),
        'week_day' : get_element_state('week_day', state_values).get('selected_option').get('value'),
        'time_of_day' : time.fromisoformat(get_element_state('time_of_day', state_values).get('selected_time')),
    }