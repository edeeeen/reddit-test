import requests
import random
import time
from faker import Faker

############################################ NEED TO PUT IN YOUR AUTH TOKEN FOR THIS TO WORK ###############################################
# Expires after around a half a day i think. can be found on POST request to https://gql.reddit.com/ as "Authorization".  I think its found on any request being made.
authToken = ""

# creates a session. might not be necessary
s = requests.session()
# create useragent via faker. Reddit doesnt accept all of them though. Didnt like it when i kept using the same useragent but not much
# testing was ever done
f = Faker()
userAgent = f.windows_platform_token()

def reply(message, thing):
    # run 10 times
    for z in range(10):
        #all of this might not be necessary. havent done enough testing. some were already removed
        x = s.post("https://oauth.reddit.com/api/comment.json", 
            params={
                "rtj": "only", 
                "emotes_as_images": "true", 
                "redditWebClient": "desktop2x", 
                "app": "desktop2x-client-production", 
                "raw_json": "1", 
                "gilding_detail": "1"
            }, 
            data={
                "api_type": "json", 
                "return_rtjson": "true", 
                # "t3_" + the id of the post
                "thing_id": thing, 
                "text": message, 
                "richtext_json": None
            },
            headers={
                "Authorization": authToken
            })
        #check if the api likes the user agent. if not gen new userAgent, wait 1 sec, and try again 10 times
        print(x)
        if x.status_code == 200:
            #return the response
            return x
        userAgent = f.windows_platform_token()
        time.sleep(1)



def newThread(subreddit, title, message):
    for z in range(10):
        x = s.post("https://oauth.reddit.com/api/submit.json", 
            params={
                "rtj": "only", 
                "emotes_as_images": "true", 
                "redditWebClient": "desktop2x", 
                "app": "desktop2x-client-production", 
                "raw_json": "1", 
                "gilding_detail": "1"
            }, 
            data={
                # subreddit name
                "sr": subreddit,
                "submit_type": "subreddit",
                "api_type": "json",
                "show_error_list": "true",
                # post title
                "title": title,
                "spoiler": "false",
                "nsfw": "false",
                "recaptcha_token": "",
                "kind": "self",
                "original_content": "false",
                "post_to_twitter": "false",
                "sendreplies": "true",
                # text
                "text": message, 
                "validate_on_submit": "true"
            }, 
            headers={
                "Authorization": authToken
            })
        #check if the api likes the user agent. if not gen new userAgent, wait 1 sec, and try again 10 times
        print(x)
        if x.status_code == 200:
            #return the response
            return x
        userAgent = f.windows_platform_token()
        time.sleep(1)

if __name__ == "__main__" :
    # make a post on r/test that is two random 9 digit ints and a tilte of "test"
    newThread("test", "test " + str(random.randint(99999999,999999999)), str(random.randint(99999999,999999999)) + "\n\n" + str(random.randint(99999999,999999999)))
    # replys to reddit.com/14gfxp1/ with two random 9 digit ints
    reply(str(random.randint(99999999,999999999)) + "\n\n" + str(random.randint(99999999,999999999)), "t3_14gfxp1")
