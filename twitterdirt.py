from __future__ import unicode_literals
import tweepy
import os

os.system("sh creds.sh") ## this sets up my credentials locally
consumerKey = os.environ.get('CONSUMER_KEY')
consumerSecret = os.environ.get('CONSUMER_SECRET')
accessToken = os.environ.get('ACCESS_TOKEN')
accessSecret = os.environ.get('ACCESS_SECRET')

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)

auth.set_access_token(accessToken, accessSecret)

api = tweepy.API(auth, wait_on_rate_limit=True)

past_followers = []
present_followers = []
following = []

if os.path.isfile("followers.txt") == False:
    print("Initializing your followers.txt file...")
    outfile = open("followers.txt", "w")

    print("Getting your current followers...")
    for user in tweepy.Cursor(api.followers).items():
        present_followers.append(user.screen_name)

    for follower in present_followers:
        outfile.write(follower + "\n")
    outfile.close()

infile = open("followers.txt", 'r')
print("Reading followers from the last time you checked...")

for line in infile:
    past_followers.append(line.strip())
infile.close()

if len(present_followers) == 0:
    print("Getting your current followers...")
    for user in tweepy.Cursor(api.followers).items():
        present_followers.append(user.screen_name)

print("Getting people you follow...")
for friend in tweepy.Cursor(api.friends).items():
    following.append(friend.screen_name)

print("Calculating differences...")
print()
print()
if len(past_followers) > len(present_followers):
    for elem in past_followers:
        if elem not in present_followers:
            print(elem, "unfollowed you!")
elif len(present_followers) > len(past_followers):
    for elem in present_followers:
        if elem not in past_followers:
            print(elem, "followed you!")
else:
    print("No change in followers/following since last time you checked")

print()
print()

for person in following:
    if person not in present_followers:
        print(person, "doesn't follow you back!")

outfile = open("followers.txt", "w")

for follower in present_followers:
    outfile.write(follower + "\n")

outfile.close()
