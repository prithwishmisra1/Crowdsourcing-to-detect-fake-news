from User import User
import random

for i in range(0, 100):

    alpha = random.uniform(0, 1)
    beta = random.uniform(0, 1)
    gamma = random.uniform(0, 1)

    user = User(alpha=alpha, beta=beta, gamma=gamma)
    user.push_user()

#rs = fb.FirebaseApplication('https://crowdsourcing101-357ca.firebaseio.com/', None)
#result = rs.post('/Users',{'name':'prithwish','roll':1605615})
#print(result)
