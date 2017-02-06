# -*- coding: utf-8 -*-
# @Author: Dima Sumaroka
# @Date:   2017-01-23 13:08:19
# @Last Modified by:   Dima Sumaroka
# @Last Modified time: 2017-02-03 14:22:26

from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager

app = Flask(__name__)

lm = LoginManager()
lm.init_app(app)
app.secret_key = "YOUR-SECRET-KEY"

app.config["MONGO_DBNAME"] = "YOUR_DB_NAME"
app.mongo = PyMongo(app, config_prefix='MONGO')
app.APP_URL = "http://127.0.0.1:5000"

# Example of how to create index on startup
#
# with app.app_context():
#     print("Setting up indexes:")
#     eventIndex = app.mongo.db.collection.create_index([
#         ('title', "text"),
#     ],
#     name="collection_search_index",
#     weights={
#         'title':100,
#     })

if __name__ == "__main__":
    app.run(debug=True)

from app import user_registration
