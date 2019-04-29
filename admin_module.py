#this is the module that will run on the admin or the expert's machine for remving the flagged news


from News import News
from User import User
from firebase import firebase

fb = firebase.FirebaseApplication('https://crowdsourcing101-357ca.firebaseio.com/', None)

news_list = fb.get('/News', None)
user_list = fb.get('/Users', None)

subset_list = {}
for i in news_list.keys():
    if 'users_flagged' in news_list[i].keys() and news_list[i]['activity_status'] == 1: #checking if the news has ever been flagged and if it is an active news

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
#this part onwards we will have the admin manually check all the shortlisted news and flag them
print("The following 10 news have been shortlisted for the administrators: ")

admin_news_flagging = {}
for news_id in final_subset_list.keys():

    print('header: '+news_list[news_id]['head'])
    print('content: '+news_list[news_id]['content'])
    flag = int(input('Your flag(1 for real and -1 for fake:\n'))
    admin_news_flagging.update({news_id:flag})

updated_user_rating = {}
print(admin_news_flagging)

#here we will update the flags of the users who had flagged the respective news
#and remove the news that were flagged fake by the administrator or the expert

for i in admin_news_flagging.keys():
    #print(i)

    if admin_news_flagging[i] == -1:

        for user_id in news_list[i]['users_flagged'].keys():

            if news_list[i]['users_flagged'][user_id] == -1:

                if user_id in updated_user_rating.keys() and 'beta' in updated_user_rating[user_id].keys():
                    beta = updated_user_rating[user_id]['beta']
                else:
                    beta = user_list[user_id]['beta']


                if user_id in updated_user_rating.keys() and 'user_rating_count' in updated_user_rating[user_id].keys() and 'fake_flag' in updated_user_rating[user_id]['user_rating_count'].keys():
                    total_fake = updated_user_rating[user_id]['user_rating_count']['fake_flag']
                else:
                    total_fake = user_list[user_id]['user_rating_count']['fake_flag']

                beta = (beta*total_fake+1)/(total_fake+1)
                updated_user_rating.update({user_id:{'beta':beta,'user_rating_count':{'fake_flag':total_fake+1}}})

            elif news_list[i]['users_flagged'][user_id] == 1:

                if user_id in updated_user_rating.keys() and 'beta' in updated_user_rating[user_id].keys():
                    beta = updated_user_rating[user_id]['beta']
                else:
                    beta = user_list[user_id]['beta']


                if user_id in updated_user_rating.keys() and 'user_rating_count' in updated_user_rating[user_id].keys() and 'fake_flag' in updated_user_rating[user_id]['user_rating_count'].keys():
                    total_fake = updated_user_rating[user_id]['user_rating_count']['fake_flag']
                else:
                    total_fake = user_list[user_id]['user_rating_count']['fake_flag']

                beta = (beta*total_fake)/(total_fake+1)
                updated_user_rating.update({user_id:{'beta':beta,'user_rating_count':{'fake_flag':total_fake+1}}})
        #uncomment the line below for the original code
        #fb.delete('News/'+i, None)

    elif admin_news_flagging[i] == 1:

        for user_id in news_list[i]['users_flagged'].keys():

            if news_list[i]['users_flagged'][user_id] == 1:

                if user_id in updated_user_rating.keys() and 'alpha' in updated_user_rating[user_id].keys():
                    alpha = updated_user_rating[user_id]['alpha']
                else:
                    alpha = user_list[user_id]['alpha']


                if user_id in updated_user_rating.keys() and 'user_rating_count' in updated_user_rating[user_id].keys() and 'real_flag' in updated_user_rating[user_id]['user_rating_count'].keys():
                    total_real = updated_user_rating[user_id]['user_rating_count']['real_flag']
                else:
                    total_real = user_list[user_id]['user_rating_count']['real_flag']

                alpha = (alpha*total_real+1)/(total_real+1)
                updated_user_rating.update({user_id:{'alpha':alpha,'user_rating_count':{'real_flag':total_real+1}}})

            elif news_list[i]['users_flagged'][user_id] == -1:

                if user_id in updated_user_rating.keys() and 'alpha' in updated_user_rating[user_id].keys():
                    alpha = updated_user_rating[user_id]['alpha']
                else:
                    alpha = user_list[user_id]['alpha']


                if user_id in updated_user_rating.keys() and 'user_rating_count' in updated_user_rating[user_id].keys() and 'real_flag' in updated_user_rating[user_id]['user_rating_count'].keys():
                    total_real = updated_user_rating[user_id]['user_rating_count']['real_flag']
                else:
                    total_real = user_list[user_id]['user_rating_count']['real_flag']

                alpha = (alpha*total_real)/(total_real+1)
                updated_user_rating.update({user_id:{'alpha':alpha,'user_rating_count':{'real_flag':total_real+1}}})
        #uncomment the line below for the original code
        # fb.put('News'+i, 'activity_status', 0)
print(updated_user_rating)

#updating the user ratings to the database

#uncomment from here to the end for the original code

# for user_id in updated_user_rating.keys():
#
#     if 'alpha' in updated_user_rating[user_id].keys():
#
#         fb.put('Users/'+user_id, 'alpha', updated_user_rating[user_id]['alpha'])
#
#     if 'beta' in updated_user_rating[user_id].keys():
#
#         fb.put('Users/'+user_id, 'beta', updated_user_rating[user_id]['beta'])
#
#     if 'user_rating_count' in updated_user_rating[user_id].keys():
#
#         if 'real_flag' in updated_user_rating[user_id]['user_rating_count'].keys():
#
#             fb.put('Users/'+user_id+'/user_rating_count/', 'real_flag', updated_user_rating[user_id]['user_rating_count']['real_flag'])
#
#         if 'fake_flag' in updated_user_rating[user_id]['user_rating_count'].keys():
#
#             fb.put('Users/'+user_id+'/user_rating_count/', 'fake_flag', updated_user_rating[user_id]['user_rating_count']['fake_flag'])
