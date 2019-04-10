#this is the module that will run on the admin or the expert's machine for remving the flagged news


from News import News
from User import User
from firebase import firebase

fb = firebase.FirebaseApplication('https://crowdsourcing101-357ca.firebaseio.com/', None)

news_list = fb.get('/News', None)

print(news_list.keys())

print(len(news_list.keys()))

subset_list = {}
for i in news_list.keys():
    print(i)
    if 'users_flagged' in news_list[i].keys(): #checking if the news has ever been flagged

        probability = 0
        total_flags = len(news_list[i].keys())
        #finding the cumulative probability of the news
        for user_id in news_list[i]['users_flagged'].keys():

            flag = news_list[i]['users_flagged'][user_id]
            if flag == 1:
                alpha = fb.get('Users/'+user_id,'alpha')
                probability = probability + alpha
            elif flag == -1:
                beta = fb.get('Users/'+user_id,'beta')
                probability = probability - beta
        #calculating utility factor of each news
        subset_list.update({i:(probability/total_flags)*(news_list[i]['users_seen_infinity']-len(news_list[i]['user_seen']))})


print(subset_list)