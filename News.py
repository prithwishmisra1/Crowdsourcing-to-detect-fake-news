#News class

from firebase import firebase

class News:

    def __init__(self, user_id, content, head, id='', users_seen=[], users_seen_infinity=0, users_flagged = {}):


        self.users_seen_infinity = users_seen_infinity
        self.id = id
        self.head = head
        self.content = content
        self.user_id = user_id
        self.users_seen = list(users_seen)
        self.users_flagged = dict(users_flagged)
        self.active = 1

    def push_news(self):

        fb = firebase.FirebaseApplication('https://crowdsourcing101-357ca.firebaseio.com/', None)
        user_list_length = len(fb.get('/Users',None).keys())

        push_val = {'head':self.head,
             'content':self.content,
             'user_id':self.user_id,
             'user_seen':self.users_seen,
             'users_seen_infinity':user_list_length,
             'users_flagged':self.users_flagged,
             'activity_status':self.active}



        key = fb.post('/News',push_val)
        id_val = key['name']
        fb.put('News/'+id_val,'id',id_val)

