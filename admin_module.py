#this is the module that will run on the admin or the expert's machine for remving the flagged news


from News import News
from User import User
from firebase import firebase

fb = firebase.FirebaseApplication('https://crowdsourcing101-357ca.firebaseio.com/', None)

news_list = fb.get('/News', None)
user_list = fb.get('/Users', None)

subset_list = {}
for i in news_list.keys():
    if 'users_flagged' in news_list[i].keys(): #checking if the news has ever been flagged

        probability = 0
        total_flags = len(news_list[i].keys())
        #finding the cumulative probability of the news
        for user_id in news_list[i]['users_flagged'].keys():

            flag = news_list[i]['users_flagged'][user_id]
            if flag == 1:
                alpha = user_list[user_id]['alpha']
                probability = probability + alpha
            elif flag == -1:
                beta = user_list[user_id]['beta']
                probability = probability - beta
        #calculating utility factor of each news
        if probability < 0:
            subset_list.update({i:(probability/total_flags)*(news_list[i]['users_seen_infinity']-len(news_list[i]['user_seen']))})


if subset_list != None:

    subset_list_keys =  list(subset_list.keys())
    subset_list_values = list(subset_list.values())
    #finding the k news for which we will perform manual analysis
    final_subset_list = {}
    k = 10
    while k > 0 or len(subset_list_keys) == len(final_subset_list.keys()):

        value = min(subset_list_values)
        index = subset_list_values.index(value)
        key = subset_list_keys[index]
        final_subset_list.update({key:value})
        subset_list_values[index] = 1.0
        k = k - 1

print(final_subset_list)