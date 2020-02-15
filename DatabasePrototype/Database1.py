import pyrebase
import requests

config = {
    "apiKey": "AIzaSyAyBMylU0GlXtQKdOhd3G6a7Nnp_uHmto4",
    "authDomain": "tsa-software-development-f63ad.firebaseapp.com",
    "databaseURL": "https://tsa-software-development-f63ad.firebaseio.com",
    "projectId": "tsa-software-development-f63ad",
    "storageBucket": "tsa-software-development-f63ad.appspot.com",
    "messagingSenderId": "459362496062",
    "appId": "1:459362496062:web:55a7b101dcd06b23926b6f",
    "measurementId": "G-HSX1PHN421"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

user = auth.sign_in_with_email_and_password("brianplease1@gmail.com", "Okpleaseop31")

db = firebase.database()

data = {"age": 12}
#
# post_requests = requests.patch("https://tsa-software-development-f63ad.firebaseio.com/" +
#                                str(user["localId"]) + ".json?auth=" + str(user["idToken"]), data=data)

temp = db.child("hello").child("Joe").child("No u").set(data)


