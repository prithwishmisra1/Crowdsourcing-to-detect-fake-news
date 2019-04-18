#program to push news in bulk

from News import News
import random
from firebase import firebase

fb =  firebase.FirebaseApplication('https://crowdsourcing101-357ca.firebaseio.com/', None)

rs = fb.get('/Users',None)

user_list = []

for i in rs.keys():
    user_list.append(i)

flag_list = [-1,1]
print(user_list)
l = len(user_list)


for i in range(0, 38):
    user_id = user_list[random.randint(0, l-1)]
    head = "This is a sample head"
    content = "This is a sample content"

    #selecting a random no of users who have seen the news
    m = random.randint(0, l-1)

    users_seen = []
    #selecting the users who have seen the news
    while m > 0:
        j = random.randint(0, l-1)
        if user_list[j] not in users_seen and user_list[j] != user_id:
            users_seen.append(user_list[j])
            m = m-1
    #print(users_seen)

    #randomly selecting the users who have flagged the news
    j = random.randint(0, len(users_seen)-1)
    users_flagged = {}

    while j > 0:

        k = random.randint(0, len(users_seen)-1)
        if users_seen[k] not in users_flagged.keys():
            users_flagged.update({users_seen[k]: flag_list[random.randint(0, 1)]})
            j = j - 1

    ob = News(user_id, content, head, users_seen=users_seen, users_flagged=users_flagged)

    ob.push_news()