import pyrebase
import json

from gconf import config

# the firebase configuration


firebase = pyrebase.initialize_app(config)


class Authentication:
    # the authenticator object
    auth = firebase.auth()

    # signup the user
    def signup(self, email, password) -> "Returns a error message if invalid email or incorrect password":
        # we first throw a signup request and the data
        signup_request = self.auth.create_user_with_email_and_password(email=email, password=password)
        data = json.loads(signup_request.content.decode())
        # if the response was not good, load the error
        if not signup_request.ok:
            error_message = data["error"]["message"]
            return error_message

        # get the id token and send a email verification
        id_token = data["idToken"]
        self.auth.send_email_verification(id_token)

        local_id = data["localId"]
        return local_id

    def sign_in(self, email, password) -> "Returns an ID Token if everything succeeds":
        # we first throw a sign in request
        sign_in_request = self.auth.sign_in_with_email_and_password(email=email, password=password)
        data = json.loads(sign_in_request.content.decode())
        # if the user put an incorrect password or email
        if not sign_in_request.ok:
            error_message = data["error"]["message"]
            return error_message, "Dummy"

        id_token = data["idToken"]

        # local id
        local_id = data["localId"]

        return local_id, id_token

    def get_user_data(self, id_token) -> "Returns user information":
        return self.auth.get_account_info(id_token)

    @staticmethod
    def check_email_verified(user_data: dict) -> "Check if the user has verified their email":
        return user_data["users"][0]["emailVerified"]

    def reset_password(self, email: str):
        request = self.auth.send_password_reset_email(email)
        return request


class Database:
    db = firebase.database()

    @staticmethod
    def get_occupation(database, local_id, key: str, folder: str):
        data = database.child(folder).child(local_id).get().val()
        return data[key]


if __name__ == "__main__":
    auth = Authentication()
    ids = auth.sign_in("brianplease1@gmail.com", "Okpleaseop31")
    print(ids)
    database = Database.db
    user_data = auth.get_user_data(ids[1])
    print(Authentication.check_email_verified(user_data))
    print(ids[1])
    if Authentication.check_email_verified(user_data):
        print("It has been verified")
    elif not Authentication.check_email_verified(user_data):
        print("It has not been verified")
