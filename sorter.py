"""
file: sorter.py
description:
    Log in to Instagram with the instagrapi library, collect the list of
    accounts I follow, and save each account's latest post date and caption
    to a CSV file.
"""

import json
import os
import csv
import time
from instagrapi import Client
from instagrapi.exceptions import PrivateError, UserNotFound, ClientError

# constants
SESSION_FILE = "instagram_session.json"
CSV_FILE = "instagram_following.csv"
SESSION_ID = "62819976716%3AwgbW4U3W1j7ZWo%3A27%3AAYlJ6u4IDKh8WC4fYngRTWiZJcOdBqXIQJFyVaFoLw"  # replace with your own session ID from the browser cookie
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

    if user.is_private:
       last_post_caption = "[Private Account - Restricted]"
    else:
          try:
              # fetch only the single most recent post (amount=1)
              medias = client.user_medias(user.pk, amount=1)
            
              if medias:
                  latest_post = medias[0]
                  last_post_date = latest_post.taken_at
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
    csvWriter.writerow([user.pk, user.username, user.is_private, date, caption])


# function: go through every account and save the results to a CSV
def exportFollowing(client, userList, csvFile):
    with open(csvFile, "w", newline="", encoding="utf-8") as f:
        csvWriter = csv.writer(f)
        csvWriter.writerow(["User ID", "Username", "Is Private", "Last Post Date", "Last Post Caption"])
        counter = 0
        private_accounts = []

        for user in userList:
            counter += 1
            if user.is_private:
                private_accounts.append(user.username)

            date, caption = getLastPost(client, user)

            # check if Instagram blocked me
            if caption.startswith("[Rate Limit or Blocked]"):
                print(f"\nStopped at user {user.username}. Progress saved.")
                break

            writeRow(csvWriter, user, date, caption)
            print(f"Processed {counter}/{len(userList)}: {user.username} - Last Post: {date}")
            time.sleep(4)  # wait 4 seconds to avoid rate limiting

    return private_accounts


# function: run the whole program
def main():
    client = Client()
    loginToInstagram(client, SESSION_FILE, SESSION_ID)
    print(f"Logged in as {client.username}")
    userList = getFollowing(client)
    print(f"Following: {len(userList)}")
    privates = exportFollowing(client, userList, CSV_FILE)
    print(f"\nTask complete! Processed data saved to {CSV_FILE}")
    print(f"Found {len(privates)} private accounts.")

main()