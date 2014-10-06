__author__ = 'admin'


from flask.ext.admin import Admin, BaseView, expose


class MyView(BaseView):
    @expose('/')
    def test(self):
        return self.render('admin/test.html')