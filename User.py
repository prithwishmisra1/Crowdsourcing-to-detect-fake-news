#python module to define user class

from firebase import  firebase
from News import News

class User:

    def __init__(self, id='', alpha=0, beta=0, gamma=0):
        user_dict = firebase.FirebaseApplication('https://crowdsourcing101-357ca.firebaseio.com/', None)
        user = user_dict.get('/Users/'+id, None)

        if id == '':

            self.id = id
            self.alpha = alpha
            self.beta = beta
            self.gamma = gamma
            self.user_rating_real = 0
            self.user_rating_fake = 0
            self.neighbours = []

        elif user == None:

            print("Invalid User")

        else:

            self.id = user['id'] #getting the user id
            self.alpha = user['alpha'] #getting the alpha value
            self.beta = user['beta'] #getting the beta value
            self.gamma = user['gamma']  #getting the gamma value
            self.user_rating_real = user['user_rating_count']['real_flag'] #no of real flags
            self.user_rating_fake = user['user_rating_count']['fake_flag'] #no of fake flags
            self.neighbours = []

    def push_user(self):

        fb = firebase.FirebaseApplication('https://crowdsourcing101-357ca.firebaseio.com/', None)

        push_val = {'alpha':self.alpha,
             'beta':self.beta,
             'gamma':self.gamma,
             'user_rating_count':{'fake_flag':self.user_rating_fake,
                                  'real_flag':self.user_rating_real}}

        key = fb.post('/Users',push_val)
        id_val = key['name']
        fb.put('Users/'+id_val,'id',id_val)

        return id_val

    def generate_news(self):

        head = input("Enter header:")
        content = input("Enter content:")
        news = News(user_id=self.id, content=content, head=head)
        news.push_news()

    def view_news(self):

        fb = firebase.FirebaseApplication('https://crowdsourcing101-357ca.firebaseio.com/', None)

        news_list = fb.get('/News', None)

        for i in news_list.keys():
            print('news id: '+i)
            print('head: '+news_list[i]['head'])
            print('')

        news_id =  input("Enter news id to view: ")
        print(news_list[news_id])
        print('news id: '+news_id)
        print('head: '+news_list[news_id]['head'])
        print('content: '+news_list[news_id]['content'])

        if self.id not in news_list[news_id]['user_seen']:
            user_seen = list(news_list[news_id]['user_seen'])
            user_seen.append(self.id)
            fb.put('/News/'+news_id, 'user_seen',user_seen)

        if self.id not in news_list[news_id]['users_flagged'].keys():
            ch =  input("Flag given news? (y/n)")
            if ch  == 'y':

                flag = int(input('Enter 1 for real and -1 for fake'))
                users_flagged = dict(news_list[news_id]['users_flagged'])
                users_flagged.update({self.id:flag})
                fb.put('/News/'+news_id, 'users_flagged',users_flagged)
