from werkzeug.middleware.dispatcher import DispatcherMiddleware
from lab1.app.app import app as lab1_app 
from lab2.app.app import app as lab2_app
from lab3.app.app import app as lab3_app
from lab4.app import create_app as lab4_app
from lab5.app import create_app as lab5_app
from lab6.app import create_app as lab6_app
from course_work.app import create_app as course_work_app
from exam_work.app import create_app as exam_work_app
from root_app.app.app import app as root_app

app = DispatcherMiddleware(root_app, {
    '/lab1': lab1_app,
    '/lab2': lab2_app,
    '/lab3': lab3_app,
    '/lab4': lab4_app(),
    '/lab5': lab5_app(),
    '/lab6': lab6_app(),
    '/course_work': course_work_app(),
    '/exam_work': exam_work_app()
})
application = app