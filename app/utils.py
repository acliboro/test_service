from datetime import datetime
from dateutil.relativedelta import relativedelta
from unittest import result
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_datetime_now():
    time_now = datetime.utcnow()
    print(f"This is the datetime now: {time_now}")
    return time_now

def get_expiration_seconds(time_now):
    date_only = time_now
    next_day = date_only + relativedelta(days=1)
    next_day = next_day.replace(hour=0, minute=0, second=0)
    print(f"This is the next_day {next_day}")
    expiration_date = next_day - time_now
    # return expiration_date.total_seconds()
    # Temporary set to 5 seconds expiry time
    return 10
