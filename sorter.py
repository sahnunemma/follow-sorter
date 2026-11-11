"""
file: sorter.py
description:
    Log in to Instagram with the instagrapi library, collect the list of
    accounts I follow, and save each account's latest post date and caption
    to a CSV file.
"""

import json
import os
from instagrapi import Client
from instagrapi.exceptions import PrivateError, UserNotFound, ClientError

# constants
SESSION_FILE = "instagram_session.json"
CSV_FILE = "instagram_following.csv"
SESSION_ID = "62819976716%3AH0RvPrhus5Ctaf%3A11%3AAYlpyT9ogHXBXHrM4ntcSfCWIckynECTnwhi7nG_xQ"  # replace with your own session ID from the browser cookie
# NOTE: SESSION_ID comes from the browser cookie called 'sessionid'.
#       It is a temporary workaround because the normal username/password
#       login is being blocked.


# function: log in to Instagram, reusing a saved session if possible
# NOTE: logging in with a session ID is a temporary workaround for now
def loginToInstagram(client, sessionFile, sessionID):
    # try the saved session
    if os.path.exists(sessionFile):
        if loadSavedSession(client, sessionFile):
            return True

    print("Attempting login using Session ID...")
    try:
        # temporary: replace with a normal login once the block is fixed
        client.login_by_sessionid(sessionID)
        print("Login successful via Session ID!")

        # save the new session so the cookie isn't needed next time
        with open(sessionFile, "w") as f:
            json.dump(client.get_settings(), f)
        print("Fresh session saved to file.")
        return True
    except Exception as e:
        print(f"Session ID login failed: {e}")
        exit()


# function: load a saved session and check that it still works
def loadSavedSession(client, sessionFile):
    try:
        print("Loading saved session from file...")
        with open(sessionFile, "r") as f:
            sessionData = json.load(f)

        client.set_settings(sessionData)

        # test the session by asking Instagram for the timeline
        client.get_timeline_feed()
        print("Session successfully restored from cache!")
        return True
    except Exception as e:
        print(f"Saved session file was invalid or expired: {e}")
        client.set_settings({})  # clear the client's settings
        return False


# function: get everyone the logged in user follows
def getFollowing(client):
    try:
        following = client.user_following(client.user_id)
        return list(following.values())
    except Exception as e:
        print(f"Failed to get following list: {e}")
    exit()



# function: get the date and caption of one account's newest post
def getLastPost(client, user):
    last_post_date = "N/A"
    last_post_caption = "N/A"
    last_post_image_url = "N/A"


    if user.is_private:
       last_post_caption = "[Private Account - Restricted]"
    else:
          try:
              # fetch only the single most recent post (amount=1)
              medias = client.user_medias(user.pk, amount=1)
            
              if medias:
                  latest_post = medias[0]
                  last_post_date = latest_post.taken_at
                  last_post_image_url = latest_post.image_urls[0] if latest_post.image_urls else "N/A"
              else:
                  last_post_caption = "[No Posts Found]"


          #raise exceptions for specific error cases
          except PrivateError:
              last_post_caption = "[Private Account - Restricted]"
          except UserNotFound:
              last_post_caption = "[User Not Found/Suspended]"
          except ClientError as e:
              print(f"\n[Rate Limit or Blocked] Stopped at user {user.username}. Error: {e}")
              print("Saving progress and exiting safely to protect your account.")
          except Exception as e:
              last_post_caption = f"[Error fetching post: {e}]"
    return last_post_date, last_post_caption



# function: write one account's details as a row in the CSV
def writeRow(csvWriter, user, date, caption):
    '''
    write the user ID, username, is private, date, and caption
        as one row in the CSV file
    '''
    pass


# function: go through every account and save the results to a CSV
def exportFollowing(client, userList, csvFile):
    '''
    open csvFile for writing
    write the column headings
        User ID, Username, Is Private, Last Post Date, Last Post Caption
    start a counter at zero
    make an empty list for private accounts
    loop through userList
        add one to the counter
        if the account is private, add its username to the private list
        getLastPost(client, user)
        if Instagram blocked me
            warn the user where it stopped
            leave the loop early to keep the account safe
        writeRow(csvWriter, user, date, caption)
        print a progress message
        wait 4 seconds so Instagram doesn't rate limit me
    close the file
    return the list of private accounts
    '''
    pass


# function: run the whole program
def main():
    client = Client()
    loginToInstagram(client, SESSION_FILE, SESSION_ID)
    print(f"Logged in as {client.username}")
    userList = getFollowing(client)
    print(f"Following: {len(userList)}")
    #test printing the last post for each user
    for user in userList:
       print(f"User: {user.username}, Last Post: {getLastPost(client, user)}")


    '''
    privates = exportFollowing(client, userList, CSV_FILE)
    tell the user the task is done and where the file was saved
    tell the user how many private accounts were found
    '''


main()