from django.contrib import admin
from member.models import UserTemp, FacebookProfile, UserProfile

admin.site.register(UserTemp)
admin.site.register(FacebookProfile)
admin.site.register(UserProfile)
