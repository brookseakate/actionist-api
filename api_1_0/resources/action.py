# package imports
from flask_restful import Resource

# relative imports
from ..app import auth
from ..models import CallAction, EmailAction, EventAction
from call_action import CallActionListAPI, CallActionAPI
from email_action import EmailActionListAPI, EmailActionAPI
from event_action import EventActionListAPI, EventActionAPI

class ActionListAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        # get CallActions
        call_actions = CallActionListAPI()
        call_list = call_actions.get()['call_actions']

        for call_action in call_list:
            call_action['type'] = 'call_action'

        # get EmailActions
        email_actions = EmailActionListAPI()
        email_list = email_actions.get()['email_actions']

        for email_action in email_list:
            email_action['type'] = 'email_action'

        # get EventActions
        event_actions = EventActionListAPI()
        event_list = event_actions.get()['event_actions']

        for event_action in event_list:
            event_action['type'] = 'event_action'

        action_list = call_list + email_list + event_list

        return { 'actions': action_list }
