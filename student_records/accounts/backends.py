from django.contrib.auth.backends import BaseBackend

class PhoneEmailBackend(BaseBackend):
    '''
    Extend authentication to Phone and email.
    Now user can use:
    -> email and password
    -> phone_number and password
    -> username and password(default)
    '''
    def authenticate(self, request, username=None, password=None):
         

    def get_user(self, user_id):
        # Implement logic to retrieve user based on user ID
        # ...
