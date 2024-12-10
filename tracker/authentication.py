from django.contrib.auth.backends import BaseBackend
from tracker.models import User

class EmailBackend(BaseBackend):
    def authenticate(self,request,username=None,password=None):
        try:
            user_obj=User.objects.get(email=username)
            if user_obj.check_password(password):
                return user_obj
            else:
                return  None
        except:
            return None

    def get_user(self,user_id):
        return User.objects.get(id=user_id)

class PhoneBackend(BaseBackend):
    def authenticate(self,request,username=None,password=None):
        try:
            user_obj=User.objects.get(phone=username)
            if user_obj.check_password(password):
                return user_obj
            else:
                return  None
        except:
            return None

