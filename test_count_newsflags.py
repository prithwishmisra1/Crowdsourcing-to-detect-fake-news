from firebase import firebase
from News import News
from User import User


fb = firebase.FirebaseApplication('https://crowdsourcing101-357ca.firebaseio.com/', None)

user_list = fb.get('Users',None)

news_list = fb.get('News', None)

#print(user_list)

user_rating = {}

for news_id in news_list.keys():

    if 'users_flagged' in news_list[news_id].keys():

        for user_id in news_list[news_id]['users_flagged'].keys():

            if news_list[news_id]['users_flagged'][user_id] == -1:

                if user_id in user_rating.keys():

                    if 'fake_flag' in user_rating[user_id].keys():

                        count = user_rating[user_id]['fake_flag']
                        count = count + 1

                    else:

                        count = 1

                    user_rating[user_id].update({'fake_flag':count})

                else:

                    count = 1

                    user_rating.update({user_id:{'fake_flag':count}})


            if news_list[news_id]['users_flagged'][user_id] == 1:

                if user_id in user_rating.keys():

                    if 'real_flag' in user_rating[user_id].keys():

                        count = user_rating[user_id]['real_flag']
                        count = count + 1

                    else:

                        count = 1

                    user_rating[user_id].update({'real_flag':count})

                else:

                    count = 1

                    user_rating.update({user_id:{'real_flag':count}})

for user_id in user_rating:

    fb.put('Users/'+user_id, 'user_rating_count', user_rating[user_id])