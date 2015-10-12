# -*- coding: utf-8 -*-
'''
Created on 2013. 7. 12.

@author: jun-yongbag
'''
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
 
from teammate.models import *


 
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = u'프로필'
 
# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )
 
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile,)
admin.site.register(SportType,)
admin.site.register(Team,)
admin.site.register(League,)
# admin.site.register(GameSchedule,)
admin.site.register(TeamMembership,)
admin.site.register(Game,)
admin.site.register(LeagueMembership,)
admin.site.register(GameEntry,)
admin.site.register(UserRequest,)
admin.site.register(TeamRequest,)


