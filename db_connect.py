from mongoengine import *
from secrets import db_host, db_port, db_user, db_password
from schemas import Profile

connect('t_database', port=db_port, host=db_host, username=db_user, password=db_password )

def get_profiles():
  return Profile.objects