'''
Created on 2013. 7. 12.

@author: jun-yongbag
'''
from django.contrib.auth.models import User, Group
from teammate.models import *
from rest_framework import serializers
from rest_framework.relations import *



class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=254)
    password = serializers.CharField(max_length=254)
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ('username', 'password', 'email',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name')

class TeamSerializer(serializers.ModelSerializer):
    league = serializers.Field(source='league')
    owner = serializers.Field(source='owner')
    class Meta:
        model = Team
        fields = ('name','location','league','owner')
        depth = 2


class GameSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=254)
    hometeam = serializers.CharField(max_length=254)
    awayteam = serializers.CharField(max_length=254)
    location = serializers.CharField(max_length=254)
    gamedate = serializers.DateTimeField(input_formats=None)
    owner = serializers.Field(source='owner')
    class Meta:
        model = Game
        fields = ('id','name','hometeam','awayteam','location','gamedate','owner')
        depth = 2


class GameEntrySerializer(serializers.ModelSerializer):
    game = serializers.Field(source='game')
    player = serializers.Field(source='player')
    class Meta:
        model = GameEntry
        fields = ('game','team','player','playerstatus')
        depth = 2
#            
class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ('name','sporttype','creator')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user','number','nick','hand','foot','created','is_staff')
        #depth = 1



