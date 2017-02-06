Dead simple and stupid, built for Python3 to use flask, flask-login, pymongo to authenticate/register user and check if user is logged in


Created becasue I wanted to use flask to authenticate my user without forms while using mongodb. I wanted to be a standalone API service for my mobile app. This was very poorly documented online so had to create my own version. This will be updated the more I work on stuff.

Right now it authenticates based on username. This is an easy switch. In user_registration, replace in the login function `user = app.mongo.db.user.find_one({"username": username})` with `user = app.mongo.db.user.find_one({"email": email})` and make sure to pass in email and get the email from request.

#Register User
`data = {"username": "myUser", "password":"myPass", "email": "d@d.com" }`
`post("http://127.0.0.1:5000/register", json=data).json()`

If succsessful then the json responce will be `{ 'success' : true, 'userId': '734891274389012', 'responce': "User saved"}`

#Login

`login = {"username":"myUser", "password": "myPass"}`
`post("http://127.0.0.1:5000/login", json=login).json()`

If succsessful then the json responce will be `{ 'success' : true, 'sessionId': '73333333334891274389012', 'responce': "User Logged In" } `
Save the sessionId for later use in your headers.


#Check to see if you can authenticate

Use base64 encoding for the sessionId when passing it in your headers. Add that header to access anything that is `@login_required`.

`headers={'Authorization': 'Basic ' + base64.b64encode(bytes('73333333334891274389012', 'utf-8')}
get("http://127.0.0.1:5000/write", headers=headers )`


`__init__.py` Contains the a stubbed out way of creating a index for searching mongoDB

Replace `YOUR-SECRET-KEY` in the `__init__.py` to whatever you want the secret to be.
Replace `YOUR_DB_NAME` in the `__init__.py` to whatever you want the secret to be.

To run:

makesure `mognod` is running

`python3 run.py`



