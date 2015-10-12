# -*- coding: utf-8 -*-
'''
Title: Teammate models

Created on 2013. 7. 12.

@author: jun-yongbag
'''
from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from datetime import datetime
GAME_CHOICES = ((0,'HOMETEAM'),
                (1,'AWAYTEAM')
                )
PLAYER_STATUS = ((0,'NO_ANSWER'),
                (1,'YES'),
                (2,'NO'),
                (3,'HOLD'),
                )
REQUEST_STATUS = ((0,'NO_ANSWER'),
                (1,'YES'),
                (2,'NO'),
                (3,'HOLD'),
                )

class SportType(models.Model):
    name = models.CharField(max_length=254, unique=True)
    owner = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name

class LeagueManager(models.Manager):
    def create_league(self, name, sporttype, creator, **extra_fields):
        if not name:
            raise ValueError('The given username must be set')
        sport = SportType.objects.get(id = sporttype)
        created = datetime.datetime.today()
        user = User.objects.get(id = creator)
        league = self.model(name=name, sporttype=sport,
                            creator = user,created = created , **extra_fields)
        league.save(using=self._db)
        return league

class League(models.Model):
    name = models.CharField(max_length=254, unique=True)
    sporttype = models.ForeignKey(SportType)
    creator = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    objects = LeagueManager()

    def __unicode__(self):
        return self.name

# 
#     
# 

class TeamManager(models.Manager):
    def create_team(self, name,location,league, owner, **extra_fields):   
        if not name:
            raise ValueError('The given teamname must be set')
        user = User.objects.get(id = owner)
        league = League.objects.get(id = league)
        team = self.model(name=name, location = location,league = league,owner = user, **extra_fields)
        print team
        team.save(using=self._db)
        return team

    def update_team(self, id, name,location,league,owner,  **extra_fields):
        """
        Team 업데이트
        """
        # u = User.objects.get(username = username)  
        team = Team.objects.get(id=id)
        user = User.objects.get(id = owner)
        league = League.objects.get(id = league)  
        if not game:
            raise ValueError('The given game must be set')
        # profile.user = u
        team.name = name
        team.location = location
        team.league = league
        team.owner = user
        
        print team
        team.save(using=self._db)
        return team




class Team(models.Model):
    name = models.CharField(max_length=254, unique=True)
    location = models.CharField(max_length=254,blank=True,)
    league = models.ForeignKey(League, blank=True, null=True)
    sporttype= models.ForeignKey(SportType, blank=True, null=True)
    owner = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    objects = TeamManager() 
    def __unicode__(self):
        return self.name
# 
# 

class GameManager(models.Manager):
    def create_game(self, name,hometeam, awayteam,location,gamedate,owner, **extra_fields):
        #print name,sporttype,owner  
        """
        Creates and saves a User with the given username, email and password.
        """
        if not name:
            raise ValueError('The given username must be set')
                
        user = User.objects.get(id = owner)  
        game = self.model(name=name, hometeam = hometeam,awayteam = awayteam ,location = location,gamedate = gamedate,owner = user, **extra_fields)
        print game
        game.save(using=self._db)
        return game


    def update_game(self, id, name,hometeam,awayteam,location,gamedate,owner,  **extra_fields):
        """
        Game 업데이트
        """
        # u = User.objects.get(username = username)  
        game = Game.objects.get(id=id)
        user = User.objects.get(id = owner)   
        if not game:
            raise ValueError('The given game must be set')
        # profile.user = u
        game.name = name
        game.hometeam = hometeam
        game.awayteam = awayteam
        game.location = location
        game.gamedate = gamedate
        game.owner = user
        
        print game
        game.save(using=self._db)
        return game

    def del_game(self,id):
        """
        Game 삭
        """
        pass



class Game(models.Model):
    name = models.CharField(max_length=254)
    hometeam = models.CharField(max_length=254)
    awayteam = models.CharField(max_length=254)
    location = models.CharField(max_length=254)
    gamedate = models.DateTimeField()
    owner  = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True,)

    objects = GameManager() 

#      
    def __unicode__(self):
            return 'ID: %s `NAME:%s HOMETEAM: %s VS  AWAYTEAM: %s DateTime: %s'%(
                          self.id,    
                          self.name,
                          self.hometeam,
                          self.awayteam,
                          self.gamedate
                          )
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        return super(Game, self).save(*args, **kwargs)

class TeamRequestManager(models.Manager):
    def requset_TeamRequest(self,user,team, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not user:
            raise ValueError('The given username must be set')
                
        user = User.objects.get(id = user.id)  
        team = Team.objects.get(id = team.id)

        getreguest = self.model( user = user,team = team , **extra_fields)
        getrequset.save(using=self._db)
        return True

    def answer_TeamRequest(self,teamrequest,state, **extra_fields):
        if not teamrequest:
            raise ValueError('The given request must be set')
        getreguest = TeamRequest.objects.get(id = teamrequest.id)
        getreguest = self.model(getreguest, state = state, **extra_fields)
        getreguest.save(using=self._db)
        return True


class TeamRequest(models.Model):
    team = models.ForeignKey(Team)
    user = models.ForeignKey(User)
    state = models.IntegerField(choices=REQUEST_STATUS,default=0)
    requestdate = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add=True)
    objects = TeamRequestManager()
    def __unicode__(self):
            return '%s, %s , %s , %s ,%s '%(
                          self.team.name,  
                          self.user.username,
                          self.state,
                          self.requestdate,
                          self.created
                          )
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        return super(TeamRequest, self).save(*args, **kwargs)



class UserRequestManager(models.Manager):
    def requset_UserRequest(self,user,team, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not user:
            raise ValueError('The given username must be set')
                
        user = User.objects.get(id = user.id)  
        team = Team.objects.get(id = team.id)
        getreguest = self.model( user = user,team = team ,**extra_fields)
        getreguest.save(using=self._db)
        return True

        
    def answer_UserRequest(self,userrequest,state, **extra_fields):
        #print name,sporttype,owner  
        """
        Creates and saves a User with the given username, email and password.
        """
        if not userrequest:
            raise ValueError('The given username must be set')
        userrequest = UserRequest.objects.get(id = userrequest.id)
        getreguest = self.model(userrequest, state = state, **extra_fields)
        getreguest.save(using=self._db)
        return True

class UserRequest(models.Model):
    team = models.ForeignKey(Team)
    user = models.ForeignKey(User)
    state = models.IntegerField(choices=REQUEST_STATUS,default=0)
    requestdate = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add=True)
    objects = UserRequestManager()

    def __unicode__(self):
            return '%s, %s , %s , %s ,%s '%(
                          self.team.name,  
                          self.user.username,
                          self.state,
                          self.requestdate,
                          self.created,
                          )
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        return super(UserRequest, self).save(*args, **kwargs)

    
#     
class TeamMembership(models.Model):
    team = models.ForeignKey(Team,related_name='TeamMembership_Team_set')
    user = models.ForeignKey(User ,related_name='TeamMembership_User_set')
    created = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(auto_now_add=True)
      
    def __unicode__(self):
        return '%s, %s' %(
                          self.user.username,
                          self.team.name,
                          )
    class Meta:
        unique_together = (('team', 'user'))
# 




class LeagueMembership(models.Model):
    league = models.ForeignKey(League,related_name='LeagueMembership_League_set')
    team = models.ForeignKey(Team,related_name='LeagueMembership_Team_set')
    date_joined = models.DateTimeField()
     
    def __unicode__(self):
        return '%s, %s' %(
                          self.league.name,
                          self.team.name,)



class GameEntryManager(models.Manager):
    def add_game_entry(self, game,team,player,playerstatus, **extra_fields):
       
        if not game:
            raise ValueError('The given game must be set')
        user = User.objects.get(username = player)     
        game = Game.objects.get(id = game)
        gameentry = self.model(game=game, team = team,gamedate=game.gamedate,
                            player = user,playerstatus = playerstatus , **extra_fields)

        print gameentry
        gameentry.save(using=self._db)
        return gameentry

    def update_game_entry(self, entry_id,game,team,player,playerstatus, **extra_fields):
        if not player:
            raise ValueError('The given game must be set')

        game = Game.objects.get(id = game)
        player = User.objects.get(username=player)

        entry = GameEntry.objects.get(id = entry_id)     
        entry.game = game
        entry.team = team
        entry.player = player
        entry.playerstatus = playerstatus
        
        print entry
        entry.save(using=self._db)
        return entry

    def del_game_entry(self,gameentry_id):
        pass


class GameEntry(models.Model):
    game = models.ForeignKey(Game,related_name='GameMembership_Game_set')
    team = models.CharField(max_length=254)
    gamedate = models.DateTimeField()
    player = models.ForeignKey(User,related_name='GameMembership_User_set')
    created = models.DateTimeField(auto_now_add=True)
    playerstatus = models.IntegerField(choices=PLAYER_STATUS,default=0)

    objects = GameEntryManager()
# home or away
    def __unicode__(self):
         return '%s, %s, %s, %s' %(
        self.game.id,
        self.team,
        self.player.username,
        self.playerstatus,
    )


class ProfileManager(models.Manager):
    def create_profile(self, user, **extra_fields):
        #print name,sporttype,creator  
        """
        사용자 프로필 생
        """
        
        if not user:
            raise ValueError('The given game must be set')
        user = User.objects.get(username = user)     
       
        profile = self.model(user = user ,**extra_fields)
        print profile
        profile.save(using=self._db)
        return profile


    def update_profile(self, id, number,nick,hand,foot,is_staff,  **extra_fields):
        #print name,sporttype,creator  
        """
        사용자 프로필 업데이트
        """
        # u = User.objects.get(username = username)  
        profile = Profile.objects.get(id=id)   
        if not profile:
            raise ValueError('The given game must be set')
        # profile.user = u
        profile.number = number
        profile.nick = nick
        profile.hand = hand
        profile.foot = foot
        profile.is_staff = is_staff
        
        print profile
        profile.save(using=self._db)
        return profile


 
class Profile(models.Model):
    class Meta:
        verbose_name = u'프로필'
        verbose_name_plural = u'프로필'
    user = models.ForeignKey(User, unique=True)
    number = models.IntegerField(verbose_name=u'번호',null =True)
    nick = models.CharField(verbose_name=u'별명', max_length=50, blank=True,null = True)
    hand = models.CharField(verbose_name=u'주손', max_length=20, blank=True,null = True)
    foot = models.CharField(verbose_name=u'주발', max_length=20, blank=True,null = True)
    created = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    objects = ProfileManager()

    def __unicode__(self):
        return '%s, %s, %s' %(
        self.user.username,
        self.number,
        self.nick,
    )


 



