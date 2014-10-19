__author__ = 'admin'


from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.base import MenuLink
from flask.ext.login import current_user
from flask.ext.admin.contrib.sqla import ModelView
from flask import Blueprint


class MyView(BaseView):

    def is_accessible(self):
        return current_user.is_authenticated()

    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class AuthenticatedMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated()


class MyModel(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated()