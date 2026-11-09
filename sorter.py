"""
file: sorter.py
description:
    Log in to Instagram with the instagrapi library, collect the list of
    accounts I follow, and save each account's latest post date and caption
    to a CSV file.
"""

# constants
SESSION_FILE = "instagram_session.json"
CSV_FILE = "instagram_following.csv"
SESSION_ID = "PASTE_YOUR_ACTUAL_SESSION_ID_HERE"
# NOTE: SESSION_ID comes from the browser cookie called 'sessionid'.
#       It is a temporary workaround because the normal username/password
#       login is being blocked.


# function: log in to Instagram, reusing a saved session if possible
# NOTE: logging in with a session ID is a temporary workaround for now
def loginToInstagram(client, sessionFile, sessionID):
    '''
    if sessionFile exists
        try loadSavedSession(client, sessionFile)
        if it worked, return True
    if sessionID is still the placeholder text
        tell the user to paste in their real session ID
        stop the program
    try to log in with sessionID
        (temporary: replace with a normal login once the block is fixed)
        save the new session to sessionFile
    if the login fails
        show the error and stop the program
    '''
    pass


# function: load a saved session and check that it still works
def loadSavedSession(client, sessionFile):
    '''
    read the session data from sessionFile
    give the session data to the client
    ask Instagram for the timeline to test the session
    if anything goes wrong
        clear the client's settings
        return False
    return True
    '''
    pass


# function: get everyone the logged in user follows
def getFollowing(client):
    '''
    ask Instagram for the accounts the user follows
    print how many there are
    turn the results into a list
    if this fails, show the error and stop the program
    return the list
    '''
    pass


# function: get the date and caption of one account's newest post
def getLastPost(client, user):
    '''
    set date and caption to "N/A"
    if the account is private
        caption is "[Private Account - Restricted]"
    otherwise, try to get the single newest post
        if there is a post
            date is when it was posted
            caption is the post's caption, or "[No Caption]" if it has none
        if there are no posts
            caption is "[No Posts Found]"
    if Instagram says the account is private
        caption is "[Private Account - Restricted]"
    if the user can't be found
        caption is "[User Not Found/Suspended]"
    if Instagram blocks or rate limits me
        pass the problem up so the main loop can stop
    if any other error happens
        caption is the error message
    return the date and caption
    '''
    pass


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
    '''
    create the Instagram client
    loginToInstagram(client, SESSION_FILE, SESSION_ID)
    userList = getFollowing(client)
    privates = exportFollowing(client, userList, CSV_FILE)
    tell the user the task is done and where the file was saved
    tell the user how many private accounts were found
    '''
    pass


main()