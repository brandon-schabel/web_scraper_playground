## Basic setup

### secrets.py setup 
fb_email = "facebook_login_email@example.com"

fb_pass = 'my_fb_pass'


sms_login_password = "examplepass"

phone = '1234567890'


microsoft face api subscription key
subscription_key = ''

filter_words = ["these", "are", "my", "filter", "words"]


db_host = 'mongodb://ds123456.mlab.com/my_database'

db_port = 123456

db_user = 'my_db_user'

db_password = 'password_example'


### server .env file setup 
DB_URL="mongodb://my_db_user:password_example@ds123456.mlab.com:123456/my_database"

## Usage
To run selenium_playground, here are the basic functions to start it up.

load_site(driver)

get_api_token()

t_login_fb(driver)

close_initial_dialogs(driver)

eval_profile()

or

eval_num_profiles(num)

or

start_swiping()