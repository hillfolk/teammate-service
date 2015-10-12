'''
Created on 2013. 7. 12.

@author: jun-yongbag
'''
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.views import View
from rest_framework.authentication import BasicAuthentication
from teammate import status
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from teammate.models import *
from teammate.serializers import *
from django.contrib.auth.models import User
from rest_framework import authentication
from django.core import serializers
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from datetime import datetime
from rest_framework import permissions
from push_notifications.models import GCMDevice


@api_view(['GET'])
def push_add(request,username,message):
    user = get_object_or_404(User,username = username)
    device1 = GCMDevice.objects.get(user=user)
    content = device1.send_message(message)
    print content
    return HttpResponse(content, status=status.HTTP_200_OK)





@authentication_classes((BasicAuthentication))
@permission_classes((permissions.IsAuthenticated,))
@api_view(['GET'])
def user_login(request,format=None):
    user = get_object_or_404(User,username=request.user.username)

    userserialized = UserSerializer(user)
    content = JSONRenderer().render([userserialized.data])
    return HttpResponse(content, status=status.HTTP_200_OK)

@authentication_classes((BasicAuthentication))
@permission_classes((permissions.IsAuthenticated,))
@api_view(['POST'])
def hello_world(request,format=None):
    print request.DATA
    print request.user
    content = JSONRenderer().render(request.DATA)
    print request
    print content
    return HttpResponse(content, status=status.HTTP_200_OK)


#--------------------------------UserView-------------------------------------#
@api_view(['GET'])
@authentication_classes((BasicAuthentication))
@permission_classes((permissions.IsAuthenticated,))
def user_auth(request, format=None):

    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
    } 
    content = JSONRenderer().render(content)
    print request
    print content
    return HttpResponse(content, status=status.HTTP_200_OK)

@api_view(['GET'])
def users(request):
    profile = Profile.objects.all()
    print request.user
    # print profile
    # print users
    members_json = ProfileSerializer(profile,many=True)
    content = JSONRenderer().render(members_json.data)
    if content:
        # profile_json = serializers.serialize("json", profile)
        return HttpResponse(content, mimetype="application/json", status=status.HTTP_200_OK)
    else:
        return HttpResponse('errors', status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def user_create(request):
    #permission_classes = (permissions.FullAnonAccess,)
    serialized = UserSerializer(data=request.DATA)
    print serialized.init_data['username']

    if serialized.is_valid():
        User.objects.create_user(
            serialized.init_data['username'],
            serialized.init_data['password'],
            serialized.init_data['email']

        )
        Profile.objects.create_profile(serialized.init_data['username'],)
        return HttpResponse(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return HttpResponse(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def profile_update(request,pk):
    #permission_classes = (permissions.FullAnonAccess,)
    u = get_object_or_404(User,pk = pk)
    p = get_object_or_404(Profile,user=u)
    print request.DATA
    
    if p:
        Profile.objects.update_profile(
            p.id,
            request.DATA['number'],
            request.DATA['nick'],
            request.DATA['hand'],
            request.DATA['foot'],
            request.DATA['is_staff']
            )
        return HttpResponse(request.DATA, status=status.HTTP_200_OK)
    else:
        return HttpResponse(request.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_send_member_requset_list(request,username):
    userrequset = get_list_or_404(UserRequest,username = username)
    if userrequset:
        # profile_json = serializers.serialize("json", profile)
        return HttpResponse(userrequset, mimetype="application/json", status=status.HTTP_200_OK)
    else:
        return HttpResponse('errors', status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def team_recive_member_requset_list(request,username):
    teamrequset = get_list_or_404(TeamRequest,username = username)
    if userrequset:
        # profile_json = serializers.serialize("json", profile)
        return HttpResponse(userrequset, mimetype="application/json", status=status.HTTP_200_OK)
    else:
        return HttpResponse('errors', status=status.HTTP_400_BAD_REQUEST)
 



@api_view(['POST'])
def user_member_request(request,username,teamname):
    u = get_object_or_404(User,username = username)
    t = get_object_or_404(Team,name = teamname)
    result =  UserRequest.objects.requset_UserRequest(u,t)
    if result:
        return HttpResponse(result, status=status.HTTP_201_CREATED)
    else:
        return HttpResponse(result, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def user_member_answer(request,username,request_id):
    #{"REQUEST_STATUS":0}
    r = get_object_or_404(TeamRequest,id = request_id)
    status = request.DATA['status'];
    # if r.user.username != username:
    #     return HttpResponse(result, status=status.HTTP_400_BAD_REQUEST)
    result =  TeamRequest.objects.answer_TeamRequest(r,status)
    if result:
        return HttpResponse(result, status=status.HTTP_200_OK)
    else:
        return HttpResponse(result, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_detile(request, username):
    # permission_classes =(permissions.FullAnonAccess)
    u = get_object_or_404(User, username=username)
    p = u.get_profile()
    myteams = [teamMemberships.team for teamMemberships in u.TeamMembership_User_set.all()]
    user =  [u]
    pro = [p]
    print type(myteams)
    allteam = user + pro + myteams
    json = serializers.serialize("json", allteam)
    return HttpResponse(json, mimetype="application/json")


@api_view(['GET'])
def user_teams(request, username):
    # permission_classes =(permissions.FullAnonAccess)
    u = get_object_or_404(User, username=username)

    myteams = [teamMemberships.team for teamMemberships in u.TeamMembership_User_set.all()]
    print myteams
    json = serializers.serialize("json", myteams)
    return HttpResponse(json, mimetype="application/json")


@api_view(['GET'])
def profiles(request):
    print request
    profile_list = Profile.objects.all()
    serializer = ProfileSerializer(profile_list,many = True)
    content = JSONRenderer().render(serializer.data)
    return HttpResponse(content, mimetype="application/json")


@api_view(['PUT'])
def profile_update(request,username):
    #permission_classes = (permissions.FullAnonAccess,)
    u = get_object_or_404(User,username = username)
    p = get_object_or_404(Profile,user=u)
    print request.DATA
    
    if p:
        Profile.objects.update_profile(
            p.id,
            request.DATA['number'],
            request.DATA['nick'],
            request.DATA['hand'],
            request.DATA['foot'],
            request.DATA['is_staff']
            )
        return HttpResponse(request.DATA, status=status.HTTP_200_OK)
    else:
        return HttpResponse(request.errors, status=status.HTTP_400_BAD_REQUEST)
#-------------------------------TeamView-------------------------------------------#

@api_view(['GET'])
def teams(request):
    allteam = Team.objects.all()
    serializer = TeamSerializer(allteam,many = True)
    content = JSONRenderer().render(serializer.data)
    return HttpResponse(content, mimetype="application/json")


@api_view(['POST'])
def team_create(request):
    print request.DATA
    serialized = TeamSerializer(data=request.DATA)
    print serialized.data
    print serialized.errors
    if serialized.is_valid():
        Team.objects.create_team(
            serialized.init_data['name'],
            serialized.init_data['location'],
            serialized.init_data['league'],
            serialized.init_data['owner']
        )
        return HttpResponse(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return HttpResponse(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def team_update(request,team_name):
    team = get_object_or_404(Team,name = team_name)
    serialized = TeamSerializer(team, data=request.DATA)
    print serialized.data
    print serialized.errors
   
    if serialized.is_valid():
        Team.objects.update_team(
            team.id,
            serialized.init_data['name'],
            serialized.init_data['location'],
            serialized.init_data['league'],
            serialized.init_data['owner']
        )
        return HttpResponse(serialized.data, status=status.HTTP_200_OK)
    else:
        return HttpResponse(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def team_detile(request, teamsname):
    t = get_object_or_404(Team, name=teamsname)
    teamsmember = [teamMemberships.user for teamMemberships in t.TeamMembership_Team_set.all()]
    print teamsmember
    allitem = [t] + teamsmember
    json = serializers.serialize("json", allitem)
    return HttpResponse(json, mimetype="application/json")


@api_view(['GET'])
def team_member(request, teamname):
    t = get_object_or_404(Team, name=teamname)
    profile = [ teamMemberships.user.get_profile() for teamMemberships in t.TeamMembership_Team_set.all()]
    print profile
    profile_json = serializers.serialize("json", profile)
    return HttpResponse(profile_json, mimetype="application/json")

@api_view(['POST'])
def team_member_request(request,teamname,username):
    u = get_object_or_404(User,username = username)
    t = get_object_or_404(Team,name = teamname)
    result =  TeamRequest.objects.requset_TeamRequest(u,t)
    if result:
        return HttpResponse(result, status=status.HTTP_201_CREATED)
    else:
        return HttpResponse(result, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
def team_member_answer(request,teamname,request_id):
    #{"status":0}
    status = request.DATA['status'];
    r = get_object_or_404(UserRequest,id = request_id)
    result =  UserRequest.objects.answer_UserRequest(r,status)
    if result:
        return HttpResponse(result, status=status.HTTP_200_OK)
    else:
        return HttpResponse(result, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def team_send_member_request_list(request,teamname):
    pass

@api_view(['GET'])
def team_recive_member_request_list(request,teamname):
    pass


#-------------------------------GameView-------------------------------------------#

@api_view(['GET'])
def team_games(request, teamname):
    t = get_object_or_404(Team, name=teamname)

    h_count = Game.objects.filter(hometeam = t ).count()
    a_count = Game.objects.filter(awayteam = t ).count()
    home = list()
    away = list()
    if h_count > 0:
        home = get_list_or_404(Game,hometeam = t)
    if a_count > 0:
        away = get_list_or_404(Game,awayteam = t)
    game_list = home  + away;
    serializer = GameSerializer(game_list,many = True)
    content = JSONRenderer().render(serializer.data)
    return HttpResponse(content, mimetype="application/json")

@api_view(['GET'])
def game_detile(request, game):
    g= get_object_or_404(Game, id=game)
    serializer = GameSerializer(g)
    content = JSONRenderer().render(serializer.data)
    return HttpResponse(content, mimetype="application/json")



@api_view(['POST'])
def game_create(request):
    serialized = GameSerializer(data=request.DATA)
    print serialized.data
    print serialized.errors
    if serialized.is_valid():
        Game.objects.create_game(
            serialized.init_data['name'],
            serialized.init_data['hometeam'],
            serialized.init_data['awayteam'],
            serialized.init_data['location'],
            serialized.init_data['gamedate'],
            serialized.init_data['owner']
        )
        return HttpResponse(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return HttpResponse(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def game_update(request,pk):
    
    game = get_object_or_404(Game,pk = pk)
    serialized = GameSerializer(game, data=request.DATA)
    print serialized.data
    print serialized.errors
   
    if serialized.is_valid():
        Game.objects.update_game(game.id,
            serialized.init_data['name'],
            serialized.init_data['hometeam'],
            serialized.init_data['awayteam'],
            serialized.init_data['location'],
            serialized.init_data['gamedate'],
            serialized.init_data['owner']
        )
        return HttpResponse(serialized.data, status=status.HTTP_200_OK)
    else:
        return HttpResponse(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def game_entrys(request,game_num):
    g = get_object_or_404(Game, id=game_num)
    ge = get_list_or_404(GameEntry,game = g)
    serializer = GameEntrySerializer(ge,many = True)
    content = JSONRenderer().render(serializer.data)
    return HttpResponse(content, mimetype="application/json")

@api_view(['POST'])
def game_entry_add(request,game_id):
    game =get_object_or_404(Game,id=game_id)
    serialized = GameEntrySerializer(data=request.DATA)
    # print serialized.init_data['name']
    print serialized.data
    print serialized.errors
    if serialized.is_valid():
        GameEntry.objects.add_game_entry(
            serialized.init_data['game'],
            serialized.init_data['team'],
            serialized.init_data['player'],
            serialized.init_data['playerstatus']
        )
        return HttpResponse(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return HttpResponse(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
def game_entry_update(request,game_id,game_entry_id):
    game =get_object_or_404(Game,id=game_id)
    game_entry = get_object_or_404(GameEntry,id=game_entry_id)
    if game.id != game_entry.game.id:
         return HttpResponse("Game Not Matching", status=status.HTTP_400_BAD_REQUEST)
    serialized = GameEntrySerializer(game_entry,data=request.DATA)
    # print serialized.init_data['name']
    if serialized.is_valid():
        GameEntry.objects.update_game_entry(game_entry.id,
            serialized.init_data['game'],
            serialized.init_data['team'],
            serialized.init_data['player'],
            serialized.init_data['playerstatus']
        )
        return HttpResponse(serialized.data, status=status.HTTP_200_OK)
    else:
        return HttpResponse(serialized._errors, status=status.HTTP_400_BAD_REQUEST)




#-------------------------------TeamView-------------------------------------------#

@api_view(['GET'])
def leagues(request):
    leagues = League.objects.all()
    print leagues
    json = serializers.serialize("json", leagues)
    return HttpResponse(json, mimetype="application/json")

@api_view(['POST'])
def league_create(request,format=None):
    # permission_classes = (permissions.FullAnonAccess,)
    print request.DATA
    serialized = LeagueSerializer(data=request.DATA)
    if serialized.is_valid():
        League.objects.create_league(
            serialized.init_data['name'],
            serialized.init_data['sporttype'],
            serialized.init_data['creator'],
        )
        return HttpResponse(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return HttpResponse(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def league_detile(request,leaguename):
    u = get_object_or_404(League, name=leaguename)
    print u
    myTeams = [leaguemembership.team for leaguemembership in u.LeagueMembership_League_set.all()]
    json = serializers.serialize("json", myTeams)
    return HttpResponse(json, mimetype="application/json")

#-------------------------------TeamView-------------------------------------------#
@api_view(['GET'])
def sports(request):
    sport = SportType.objects.all()
    json = serializers.serialize("json", [sport])
    return HttpResponse(json, mimetype="application/json")


