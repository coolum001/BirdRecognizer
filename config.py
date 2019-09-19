import os


class Config(object):
    SECRET_KEY = '263e5536a9e864f5218604d5a5dda15c3e59fee22c0ec768'
    # UPLOAD_FOLDER = 'uploads/'
    # used in os.join() to create path for photo uploads
    UPLOAD_FOLDER = '/app'
    MODEL_FOLDER = 'models'


# end Config

