# @TODO - update user addresses to real addresses (for Google Civic API calls)

# package & module imports
import string
import phonenumbers
from random import randrange, randint, choice, shuffle, getrandbits
from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Faker

# relative imports
from app import db
from api_1_0.models import User, CallAction, EmailAction, EventAction

fake = Faker()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # Helper Methods # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def select_random_official():
    official_types = ["President of the United States", "Vice-President of the United States", "Attorney General", "United States House of Representatives", "United States Senate", "Governor", "State House District", "State Senate District"]
    return choice(official_types)

def select_random_user():
    user_count = User.query.count()
    random_user = User.query.offset(randint(0, user_count - 1)).first()
    return random_user

def select_kudos_text():
    return choice(["Keep it up! You're fighting for what's right.", "Keep being the change you wish to see in the world.", "You're making a difference.", "You did it. Good job!", "Thank you for taking action.", "The people united will never be divided. We're getting there together", "Step by step. We make the road by walking."])

def generate_datetimes(type_event=False): # call with True for event_actions, otherwise False
    # set up arbitrary last date for end_datetime range
    last_date = datetime(2017, 4, 30, 0, 0, 0)

    # set up random start & end datetimes for listing & event
    start = fake.date_time_between(start_date="-90d", end_date="+90d")
    end = fake.date_time_between_dates(datetime_start=start, datetime_end=last_date)

    # for event_actions, return start & end listing datetimes, + event start datetime
    if type_event:
        ev_start = end - timedelta(hours = randint(1,10))
        return start, end, ev_start
        # NOTE: ev_start gets returned as datetime.datetime value, whereas start & end are returned as just datetime
    # for other action types, return just start & end listing datetimes
    return start, end

def generate_title_and_headline(action_type, pro=True):
    if action_type == "call":
        verb = choice(["Call", "Speak Out", "Advocate", "Fight", "Act"])
    elif action_type == "event":
        verb = choice(["March", "Stand", "Rise Up", "Fight", "Act", "Community Meeting", "Workshop"])
    elif action_type == "email":
        verb = choice(["Write", "Advocate", "Speak Out", "Fight", "Act"])
    else:
        verb = choice("Call Fight Act Stand Speak March".split())

    if pro == True:
        issue = choice(["Immigrant Rights", "Trans Rights", "Refugees", "Black Lives", "Economic Justice", "Peace", "Environmental Justice", "Clean Water", "Education", "Affordable Housing", "Reproductive Rights", "Universal Health Care"])
        title = verb + " for " + issue
    else:
        issue = choice(["the new Youth Jail", "White Supremacy", "Homophobia", "Racism", "Mass Incarceration", "Deportation", "Police Brutality", "the Dakota Access Pipeline"])
        title = verb + " against " + issue

    head_words = fake.words(randint(1, 4))
    head_words.append(issue)
    shuffle(head_words)
    headline = " ".join(head_words).title() + "."

    return title, headline, issue

def generate_script(point, length):
    return "Hello. My name is ____, and I am a constituent. I am calling today to ask you to " + point.lower() + ". " + fake.text(length)

def generate_phonenumber():
    # generate & validate random 10-digit phone number
    while True:
        ph_num = str(randint(2000000000,9999999999))
        parsed_ph_num = phonenumbers.parse(ph_num, "US")
        if phonenumbers.is_valid_number(parsed_ph_num) == True:
            return ph_num

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # Seeder Class # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Seeder:
    @staticmethod
    def seed_users(count=100):
        for i in range(count):
            # generate a random device id
            random_device_id = ''.join(choice(string.ascii_uppercase + string.digits + '-') for a in range(40))

            # create User
            u = User(user_name = fake.user_name(),
                    device_id = random_device_id,
                    email = fake.email(),
                    first_name = fake.first_name(),
                    last_name = fake.last_name(),
                    about = fake.text(randrange(5, 2000)), # text of random character length, max 2000 characters
                    street_address_1 = fake.street_address(),
                    street_address_2 = (fake.street_address() if i % 7 == 0 else None),
                    city = fake.city(),
                    state = fake.state_abbr(),
                    zip = fake.zipcode())

            # add to db session & commit
            db.session.add(u)
            db.session.commit()

    @staticmethod
    def seed_call_actions(count=100):
        for j in range(count):
            # collect values
            pro_issue = bool(getrandbits(1))
            call_title, call_headline, call_issue = generate_title_and_headline("call", pro_issue)
            talk_point = ("Support " if pro_issue else "Oppose ") + call_issue
            start_date, end_date = generate_datetimes(False)

            # create Action
            ca = CallAction(title = call_title,
                            headline = call_headline,
                            description = (fake.text(randrange(5, 2000)) if j % 11 != 0 else None),
                            list_start_datetime = start_date,
                            list_end_datetime = end_date,
                            target_phone_number = (generate_phonenumber() if j % 2 == 0 else None),
                            target_name = (fake.name() if (j % 2 == 0 or j % 5 == 0) else None),
                            target_official_type = (select_random_official() if j % 2 == 1 else None),
                            script = generate_script(talk_point, randint(40, 1000)),
                            talking_point_1 = talk_point,
                            talking_point_2 = (fake.text(randrange(5, 70)) if j % 4 != 0 else None),
                            talking_point_3 = (fake.text(randrange(5, 70)) if j % 8 == 1 else None),
                            kudos_text = select_kudos_text(),
                            user = select_random_user()
                            )

            # add to db session & commit
            db.session.add(ca)
            db.session.commit()

    @staticmethod
    def seed_email_actions(count=100):
        for k in range(count):
            # collect values
            pro_issue = bool(getrandbits(1))
            email_title, email_headline, email_issue = generate_title_and_headline("email", pro_issue)
            subject = ("Support " if pro_issue else "Oppose ") + email_issue
            start_date, end_date = generate_datetimes(False)

            # create Action
            ema = EmailAction(title = email_title,
                            headline = email_headline,
                            description = (fake.text(randrange(5, 2000)) if k % 11 != 0 else None),
                            list_start_datetime = start_date,
                            list_end_datetime = end_date,
                            target_email = (fake.email() if k % 2 == 0 else None),
                            target_name = (fake.name() if (k % 2 == 0 or k % 5 == 0) else None),
                            target_official_type = (select_random_official() if k % 2 != 0 else None),
                            email_subject = subject,
                            body = fake.text(randrange(5, 2500)),
                            kudos_text = select_kudos_text(),
                            user = select_random_user()
                            )

            # add to db session & commit
            db.session.add(ema)
            db.session.commit()

    @staticmethod
    def seed_event_actions(count=100):
        for l in range(count):
            # collect values
            pro_issue = bool(getrandbits(1))
            event_title, event_headline, event_issue = generate_title_and_headline("event", pro_issue)
            start_date, end_date, event_start = generate_datetimes(True)

            # create CallAction
            eva = EventAction(title = event_title,
                            headline = event_headline,
                            description = (fake.text(randrange(5, 2000)) if l % 11 != 0 else None),
                            list_start_datetime = start_date,
                            list_end_datetime = end_date,
                            location = fake.address(),
                            event_start_datetime = event_start,
                            event_end_datetime = end_date,
                            kudos_text = select_kudos_text(),
                            user = select_random_user()
                            )

            # add to db session & commit
            db.session.add(eva)
            db.session.commit()
