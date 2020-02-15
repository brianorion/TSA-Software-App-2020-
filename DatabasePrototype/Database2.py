import pyrebase

config = {
    "apiKey": "AIzaSyAyBMylU0GlXtQKdOhd3G6a7Nnp_uHmto4",
    "authDomain": "tsa-software-development-f63ad.firebaseapp.com",
    "databaseURL": "https://tsa-software-development-f63ad.firebaseio.com",
    "projectId": "tsa-software-development-f63ad",
    "storageBucket": "tsa-software-development-f63ad.appspot.com",
    "messagingSenderId": "459362496062",
    "appId": "1:459362496062:web:95cb00fcffff7cb4926b6f",
    "measurementId": "G-DJ0534LNZR"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

email = input("Please enter a email\n")
password = input("Please enter a password\n")

user = auth.sign_in_with_email_and_password(email, password)

print(user)