# @TODO - update user addresses to real addresses (for Google Civic API calls)

# package & module imports
import string
import phonenumbers
from random import randrange, randint, choice
from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
# from phonenumbers import parse, is_valid_number

# relative imports
from app import db
from api_1_0.models import User, CallAction, EmailAction, EventAction

fake = Faker()

# elected official type selector
def select_random_official():
    official_types = ["President of the United States", "Vice-President of the United States", "Attorney General", "United States House of Representatives", "United States Senate", "Governor", "State House District", "State Senate District"]
    return choice(official_types)

def select_random_user():
    user_count = User.query.count()
    random_user = User.query.offset(randint(0, user_count - 1)).first()
    return random_user

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

    # for other actions, return just start & end listing datetimes
    return start, end

class Seeder:
    @staticmethod
    def seed_users(count=100):
        for i in range(count):
            # generate a random device id
            rand_dev_id = ''.join(choice(string.ascii_uppercase + string.digits + '-') for a in range(40))

            # create User
            u = User(user_name = fake.user_name(),
                    device_id = rand_dev_id,
                    email = fake.email(),
                    first_name = fake.first_name(),
                    last_name = fake.last_name(),
                    about = fake.text(randrange(5, 2000)), # text of random character length, max 2000 characters
                    street_address_1 = fake.street_address(),
                    city = fake.city(),
                    state = fake.state_abbr(),
                    zip = fake.zipcode())

            # add user to db session
            db.session.add(u)

            # give some users a secondary address line
            if i % 7 == 0:
                u.street_address_2 = fake.secondary_address()

            # commit to db
            db.session.commit()

    @staticmethod
    def seed_call_actions(count=100):
        # set up arbitrary last date for end_datetime range
        # last_date = datetime(2017, 4, 30, 0, 0, 0) # @TODO - remove

        for j in range(count):
            start_date, end_date = generate_datetimes(False)

            # set up random start & end datetimes
             # @TODO - remove
            # start_date = fake.date_time_between(start_date="-90d", end_date="+90d")
            # end_date = fake.date_time_between_dates(datetime_start=start_date, datetime_end=last_date)

            # # generate & validate random 10-digit phone number
            ph_num = str(randint(2000000000,9999999999))
            parsed_ph_num = phonenumbers.parse(ph_num, "US")
            while phonenumbers.is_valid_number(parsed_ph_num) != True:
                ph_num = str(randint(2000000000,9999999999))
                parsed_ph_num = phonenumbers.parse(ph_num, "US")

            # create CallAction
            ca = CallAction(title = fake.text(randrange(5, 80)),
                            headline = fake.text(randrange(5, 100)),
                            description = fake.text(randrange(5, 2000)),
                            list_start_datetime = start_date,
                            list_end_datetime = end_date,
                            target_phone_number = ph_num,
                            target_name = fake.name(),
                            target_official_type = select_random_official(),
                            script = fake.text(randrange(5, 1000)),
                            talking_point_1 = fake.text(randrange(5, 70)),
                            talking_point_2 = fake.text(randrange(5, 70)),
                            kudos_text = fake.text(randrange(5, 100)),
                            user = select_random_user()
                            )

            # add to db session
            db.session.add(ca)

            # give some actions a third talking point
            if j % 7 == 0:
                ca.talking_point_3 = fake.text(randrange(5, 70))

            # commit to db
            db.session.commit()

    @staticmethod
    def seed_email_actions(count=100):
         # @TODO - remove
        # # set up arbitrary last date for end_datetime range
        # last_date = datetime(2017, 4, 30, 0, 0, 0)

        for k in range(count):
            start_date, end_date = generate_datetimes(False)

             # @TODO - remove
            # # set up random start & end datetimes
            # start_date = fake.date_time_between(start_date="-90d", end_date="+90d")
            # end_date = fake.date_time_between_dates(datetime_start=start_date, datetime_end=last_date)

            # create CallAction
            ema = EmailAction(title = fake.text(randrange(5, 80)),
                            headline = fake.text(randrange(5, 100)),
                            description = fake.text(randrange(5, 2000)),
                            list_start_datetime = start_date,
                            list_end_datetime = end_date,
                            target_email = fake.email(),
                            target_name = fake.name(),
                            target_official_type = select_random_official(),
                            email_subject = fake.text(randrange(5, 255)),
                            body = fake.text(randrange(5, 2500)),
                            kudos_text = fake.text(randrange(5, 100)),
                            user = select_random_user()
                            )

            # add to db session
            db.session.add(ema)
            # commit to db
            db.session.commit()

    @staticmethod
    def seed_event_actions(count=100):
        #  # @TODO - remove
        # # set up arbitrary last date for end_datetime range
        # last_date = datetime(2017, 4, 30, 0, 0, 0)

        for l in range(count):
            start_date, end_date, event_start = generate_datetimes(True)

            #  # @TODO - remove
            # # set up random start & end datetimes for listing & event
            # start_date = fake.date_time_between(start_date="-90d", end_date="+90d")
            # end_date = fake.date_time_between_dates(datetime_start=start_date, datetime_end=last_date)
            # event_start = end_date - timedelta(hours = randint(1,10))

            # create CallAction
            eva = EventAction(title = fake.text(randrange(5, 80)),
                            headline = fake.text(randrange(5, 100)),
                            description = fake.text(randrange(5, 2000)),
                            list_start_datetime = start_date,
                            list_end_datetime = end_date,
                            location = fake.address(),
                            event_start_datetime = event_start,
                            event_end_datetime = end_date,
                            kudos_text = fake.text(randrange(5, 100)),
                            user = select_random_user()
                            )

            # add to db session
            db.session.add(eva)
            # commit to db
            db.session.commit()
