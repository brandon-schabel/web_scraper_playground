from mongoengine import *

class Profile(Document):
  name = StringField()
  #description = StringField()
  image_url = StringField()
  #occupation = StringField()
  #school = StringField()
  reason = StringField()
  liked = BooleanField()
  datetime = DateTimeField()
  #distance = IntField() 
  age = IntField()
  attributes = DictField()
  user_id = StringField()