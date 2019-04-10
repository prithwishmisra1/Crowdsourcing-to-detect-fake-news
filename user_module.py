__author__ = '1605615'

#module that will run on the client machines
from firebase import firebase
from News import News
from User import User


ch = input('2. Existing User\n1. New User')

if ch == '1':
    new_user = User()
    user_id = new_user.push_user()
    print('User created. Your id is '+user_id)

elif ch == '2':
    user_id = input('Enter user id: ')
    user = User(user_id)

    while True:
        print('Enter your choice(-1 to exit): ')
        print('1.View News')
        print('2. Generate News\n')

        ch2 = input()
        if ch2 == '1':
            user.view_news()

        elif ch2 == '2':
            user.generate_news()

        elif ch2 == '-1':
            break

        else:
            print('Wrong choice. Try again')
