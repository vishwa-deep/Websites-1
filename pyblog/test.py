__author__ = 'admin'

import os
import unittest

from views import app, db
from config import basedir
from models import Post, User
from datetime import date
from flask_login import current_user

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
        self.login('Michael', 'password')
        response = self.app.get('/admin/postview/')
        self.assertEquals(response.status_code, 200)
        self.assertIn('Post', response.data)

    def test_user_can_logout(self):
        self.create_user()
        self.login('Michael', 'password')
        response = self.logout()
        self.assertEquals(response.status_code, 200)
        self.assertIn('Logged out successfully.', response.data)

    def test_logged_out_users_cannot_access_admin(self):
        response = self.app.get('/admin')
        self.assertNotIn('Post', response.data)

    def test_post_is_on_homepage(self):
        self.create_post()
        response = self.app.get('')
        self.assertIn('Test Post', response.data)


    # This test verifies that if a user is authenticated they get
    # to skip the login page
    def test_logged_in_users_skip_login_to_get_to_admin(self):
        self.create_user()
        self.login('Michael', 'password')
        self.app.get('/')
        response = self.app.get('/admin/postview', follow_redirects=True)
        self.assertIn('Create', response.data)

    def test_login_page_gives_blank_input_error(self):
        response = self.login('', '')
        self.assertIn('Error in the Password field - This field is required', response.data)

    def test_invalid_user_cannot_login(self):
        response = self.login('test', 'user')
        self.assertIn('Username or password does not exist!', response.data)

    def test_login_page_exists(self):
        response = self.app.get('/login')
        self.assertIn('Login to add a post!', response.data)

    def test_page_for_post_works(self):
        self.create_post()
        response = self.app.get('/post/Test_Post')
        self.assertIn('This is a test post.', response.data)


    ######################################
    ###             Admin              ###
    ######################################

    def test_admin_homepage_is_available(self):
        self.create_user()
        self.login('Michael', 'password')
        response = self.app.get('/admin/')
        self.assertIn('Welcome to the admin page.', response.data)


    ################################
    ###         Models           ###
    ################################

    def test_string_representation_of_post_object(self):
        self.create_post()
        post = db.session.query(Post).all()
        print post
        for p in post:
            self.assertEquals(p.title, 'Test Post')

    def test_string_representation_of_user_object(self):
        self.create_user()
        user = db.session.query(User).all()
        print user
        for u in user:
            self.assertEquals(u.user_id, "Michael")



if __name__ == '__main__':
    unittest.main()










