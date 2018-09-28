from mongoengine import *
from schemas import Profile
from db_secrets import *

connect('t_database', port=port, host=host, username=user, password=password )
user = Profile(name="Brenda", age=25, image_url="https://blog.conservation.org/wp-content/uploads/2014/06/ci_19290600_cropped.jpg", occupation="software engineer", distance=25 )
user.save()

print(Profile.objects)
for profile in Profile.objects:
  print(profile.name)