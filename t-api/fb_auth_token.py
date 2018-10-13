# Used from  https://github.com/philipperemy/Deep-Learning-Tinder/blob/master/tinder_token.py

import re

import requests
import robobrowser

MOBILE_USER_AGENT = "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)"
FB_AUTH = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd"


def get_fb_access_token(email, password):
    s = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser="lxml")
    s.open(FB_AUTH)
    f = s.get_form()
    f["pass"] = password
    f["email"] = email
    s.submit_form(f)
    f = s.get_form()
    try:
        s.submit_form(f, submit=f.submit_fields['__CONFIRM__'])
        access_token = re.search(
            r"access_token=([\w\d]+)", s.response.content.decode()).groups()[0]
        return access_token
    except Exception as ex:
        print("access token could not be retrieved. Check your username and password.")
        print("Official error: %s" % ex)
        return {"error": "access token could not be retrieved. Check your username and password."}


def get_fb_id(access_token):
    if "error" in access_token:
        return {"error": "access token could not be retrieved"}
    """Gets facebook ID from access token"""
    req = requests.get(
        'https://graph.facebook.com/me?access_token=' + access_token)
    return req.json()["id"]

'''
fb_access token?
{"meta":{"status":200},"data":{"is_new_user":false,"api_token":"98cb6a6b-f2ab-47d3-9654-ee27ffda863b","sms_login":"auth_v2"}}
Request URL: https://www.facebook.com/impression.php/fd84461b2e271/?api_key=464891386855067&lid=114&payload=%7B%22payload%22%3A%7B%22init%22%3A1538842356746%2C%22close%22%3A1538842357510%2C%22method%22%3A%22permissions.oauth%22%2C%22display%22%3A%22popup%22%7D%2C%22source%22%3A%22jssdk%22%7D
tinder_token {"token":"fcc53c1b-8b45-4b92-9c00-259b8e8bbce3"}

fb access_token?
AT1LROUQGaaztzHrSlttySolmNLYdZAgGCOirUlDkfOX3uNDu4diHW5TKSS6kUKi9Ajfd1EX1xULGqVyVni_awQ0MZYbebdSCFHI3AtUqZOvAp_1kNdSLOXlutOjdxwA2KzFxtomH80
00252230F06532-A1B9-4B10-BB28-B29956C71AB1
eh5boFPYn6uh3Kva_1zjC42pQeKv6Z-bHkfMBrATqoI.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUURxbnM5bk8zTVhqNXpIb3JNVTNBOU9yZDRVdXo0RTBSTlVWbmN1RHFGQVdjbTNlaGFHemtudVpDdlR3UVlpYlJvdmp1bFdLMnNVNE9GNU5VcnY5dk1zdFJzWkoyMXZyQW1MVG1oZ21WTGthcVFwUE9sODQ2RVp1eldyVzU0Sm5UTnBzUVRRWDFVRVVTQThia3Q0a3llYTFiZTFTWHZfajhHMEN5NWpjV2xTbGNxM0V3b25GbkVpU3l4Y0l5N3NGNkJTTThpQWNaaVVUbWkzZ0dYUWJzWHNPY2dncTlSdF9MenZCNUZsZ2Z6aExnYXNmNTVDUF9LX0NWNFkzczRqY2tqcHNBSDFsWTZjM0NhaWhFbGpMZUVMX3U2ZndvUXVaajhiMEpQVTc2cUpibkdOYl9xY1N2Y1pwOFhzaThDQTJKSTRsaEZaWGdtQldEdlFhQ0Y1ZnFybUU1WHJDZVRKc05lcHVHMkg4UzJOSWFDRjdUbE5mUGtBZlJCZDBybEZBYk1kdHRmNnFLSUtsV2gwX0hpSmVLOTkiLCJpc3N1ZWRfYXQiOjE1Mzg4NDM0NDEsInVzZXJfaWQiOiI3OTA3MjAzODA5NDU5NjUifQ&
access_token=EAAGm0PX4ZCpsBAL5Kh5CGgmUoDDZCGPlBeXvOOpY1vHOaZBcaYZA18Nya1ZBLzJ6LzRG6rDMlhWFwUAUE14Aj7CUWtj7EtWo5ZCg8DIoqaEMm335ZAGjLlAPC9xqlZAgZBDpKiHrzbR4mWEi8YgIHLgP8c2Fs7ucf2BP0kuffDsNnWlm4D9xfFwmJxnfBF8QNZCud3zaVxUzZBdJee3zzJrnrs3FJSsbjZCt4AkZBWQdFW4cal8QqAyZCJSjxXbLsfrZAxuGemkFW5JXuHYvQZDZD
fb_user_id =790720380945965

https://github.com/defaultnamehere/tinder-detective/issues/3

curl -X POST https://api.gotinder.com/auth --data '{"facebook_token": 'EAAGm0PX4ZCpsBAL5Kh5CGgmUoDDZCGPlBeXvOOpY1vHOaZBcaYZA18Nya1ZBLzJ6LzRG6rDMlhWFwUAUE14Aj7CUWtj7EtWo5ZCg8DIoqaEMm335ZAGjLlAPC9xqlZAgZBDpKiHrzbR4mWEi8YgIHLgP8c2Fs7ucf2BP0kuffDsNnWlm4D9xfFwmJxnfBF8QNZCud3zaVxUzZBdJee3zzJrnrs3FJSsbjZCt4AkZBWQdFW4cal8QqAyZCJSjxXbLsfrZAxuGemkFW5JXuHYvQZDZD', "facebook_id": '790720380945965'}'
'''
