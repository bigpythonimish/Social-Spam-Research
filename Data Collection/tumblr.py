from datetime import timedelta
import datetime
from bs4 import BeautifulSoup as bs 
import pytumblr
import pymongo


REQUEST_TOKEN_URL = 'http://www.tumblr.com/oauth/request_token'
AUTHORIZATION_URL = 'http://www.tumblr.com/oauth/authorize'
ACCESS_TOKEN_URL = 'http://www.tumblr.com/oauth/access_token'
CONSUMER_KEY = 'V3d6XXDyA2Mhet8YGcnBEP6FwJ7EZEhb8xYD5t1IjDnW3ivDaO'
CONSUMER_SECRET = 'DkfPLb5pYNdRcdEjSpLz6iLzZR46VRArFB06rCEyLwGNBKnlYh'

client = pymongo.MongoClient()
db = client.social_data
coll = db.posts

client = pytumblr.TumblrRestClient('V3d6XXDyA2Mhet8YGcnBEP6FwJ7EZEhb8xYD5t1IjDnW3ivDaO')

dups = 0
inserted = 0

def search(keyword):
    global dups, inserted
    for i in range(5):
        date = datetime.datetime.today()-timedelta(weeks=2*i)
        date = date.strftime("%s")
        print("searching for keyword " +keyword + " date before " + date)
        try:
            a = client.tagged(keyword,before=date)
        except:
            print("oops ran into an error")
            return

        for ax in a:

            try:
                raw = ax['trail'][0]['content']
                soup = bs(raw)
                text = soup.text

                print("##############################")
            except:
                try:
                    text = ax['summary']
                    # print(text
                    print("???????????????????????????????? ")
                except:


                    print("Couldnt parse the dict")

                    continue
            user = ax['blog_name']
            location = -1
            hashtags =ax['tags']
            post_id = ax['id']
            RT = -1
            fav = -1
            source = 'tumblr'
            date_added = ax['date'][:10]
            in_reply_to = -1
            timestamp = datetime.datetime.fromtimestamp(ax['timestamp']).strftime('%d %b %Y')
            obj = {}
            jsonx = {"_id": post_id, 'keyword': keyword, "username": user, "user_id": -1, "content": text, "timestamp": timestamp,
                         "location": location, "hashtags": hashtags, "Retweet": RT, "Fav": fav, 'source': source,
                         'date_added': date_added, 'in_reply_to': in_reply_to}

            # print(jsonx)
            try:
                coll.insert(jsonx)  # and insert
                inserted += 1
                # count_ins += 1
            except pymongo.errors.DuplicateKeyError:  # Except if it's already there
                # count_dup += 1
                dups += 1
                print("Duplicate Key")
            print(keyword + ":  \ntimestamp: " +'\n' + text )
            print("###########################" )

file = open('../keywords.txt', 'r')
print("opened")
num_lines = 0
for line in file:
    if line.strip():
        num_lines += 1
print(num_lines)

file = open('../keywords.txt', 'r')

for keyword in file:

    keyword = keyword.rstrip()
    print(keyword)
    if not keyword: continue
    query = keyword
    search(query)
print(f"######Inserted: {inserted}, Duplicates Discarded: {dups} #######")
