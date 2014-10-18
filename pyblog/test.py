__author__ = 'admin'

import os
import unittest

from views import app, db
from config import basedir
from models import Post, User
from datetime import date

TEST_DB = 'post.db'


class PostTests(unittest.TestCase):

    #####################################
    ##      Setup and Teardown         ##
    #####################################

    #executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    #executed after each test
    def tearDown(self):
        db.drop_all()

    ######################################
    ##          Helper Methods          ##
    ######################################

    def login(self, name, password):
        return self.app.post(
            '/login',
            data=dict(
                uid=name,
                password=password
            ),
            follow_redirects=True
        )

    def create_user(self):
        new_user = User(
            user_id='Michael',
            authenticated=False,
        )
        new_user.hash_password('password')
        db.session.add(new_user)
        db.session.commit()

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def create_post(self):
        new_post = Post(
            title='Test Post',
            post_body='This is a test post.',
            tags='testing',
            posted_date=date(2014, 10, 03),
            updated_at=None,
            status=1,
            user_id='Michael'
        )
        db.session.add(new_post)
        db.session.commit()

    ##########################################
    ## not used due to adding post in admin ##
    ##########################################
    # def create_post(self):
    #     return

    #######################
    ### views           ###
    #######################

    def test_logged_in_users_can_access_admin_post(self):
        self.create_user()
        #self.app.get('/login', follow_redirects=True)
        response = self.login('Michael', 'password')
        #response = self.app.get('/admin/', follow_redirects=True)
        self.assertIn('Post', response.data)

    def test_user_can_logout(self):
        self.create_user()
        self.login('Michael', 'password')
        response = self.logout()
        self.assertIn('Logged out successfully.', response.data)

    def test_logged_out_users_cannot_access_admin(self):
        response = self.app.get('/admin')
        self.assertNotIn('Post', response.data)

    def test_post_is_on_homepage(self):
        self.create_post()
        response = self.app.get('')
        self.assertIn('Test Post', response.data)

if __name__ == '__main__':
    unittest.main()










