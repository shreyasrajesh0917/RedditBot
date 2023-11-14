from urllib import requests #Chuck Norris joke API
import praw
import config
import time
import os

def login():
    r = praw.Reddit(username = config.username, password = config.password, clientId = config.clientId, secretId = config.secretId, userAgent = "Shreyas's Joke Comment Tracker")
    print("Successfully logged in.")
    return r

def run(r, commentsReplied):
    print("Obtaining 20 comments...")
    for comment in r.subreddit('test').comments(limit = 20):
        if "joke" in comment.body and comment.id not in commentsReplied and comment.author != r.user.me():
            print("I saw the word \"joke\" in comment " + comment.id)

            reply = "You want a Chuck Norris joke? Ask and you shall receive:\n\n"
            joke = requests.get('https://api.chucknorris.io/jokes/random').json()['value']
            reply += ">" + joke #add joke as quote to comment reply
            reply += "\n\nThis joke is from [chucknorris.io](https://api.chucknorris.io)."

            print("Replied to comment " + comment.id)
            commentsReplied.append(comment.id)
            with open("commentsReplied.txt", "a") as file:
                file.write(comment.id + "\n")

time.sleep(10) #wait 10 seconds before replying to not cause overflow of replies 

def saveComments():
    if not os.path.isfile("commentsReplied.txt"):
        commentsReplied = []
    else:
        with open("commentsReplied.txt", "r") as file:
            commentsReplied = file.read()
            commentsReplied = commentsReplied.split("\n") #makes the commentsReplied list contain all the comments in the text file, separated by a newline
            commentsReplied = filter(None, commentsReplied)
    return commentsReplied

r = login()
commentsReplied = saveComments() #list to keep track

while True:
    run(r, commentsReplied)

