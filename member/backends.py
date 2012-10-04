from django.contrib.auth.models import User
from member.models import FacebookProfile

class FacebookBackend:
    """
    FacebookBackend for authentication
    """

    supports_anonymous_user = False
    supports_object_permissions = False
    supports_inactive_user = False

    def authenticate(self, facebook_uid, user=None):
        '''
        authenticates the token by requesting user information from facebook
        '''

        try:
            fbprofile = FacebookProfile.objects.get(uid=facebook_uid)
            return fbprofile.user
        except FacebookProfile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


