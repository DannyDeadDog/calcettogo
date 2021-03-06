from rest_framework import serializers
from core.models import *
from math import *

class UserSerializer(serializers.ModelSerializer):
    vote = serializers.SerializerMethodField('calculate_vote')
    number_of_feedbacks_received  = serializers.SerializerMethodField('num_of_feeds')
    number_of_positive_feedbacks_received = serializers.SerializerMethodField('num_of_feeds_p')


    def calculate_vote(self,user):
        base = 6
        votes = Vote.objects.all().filter(user=user)
        if votes.count()==0:
            return base
        cnt = 0
        for vote in votes:
            cnt += vote.value
        cnt /= votes.count()
        cnt -= 0.5
        return base + (cnt*8)

    def num_of_feeds(self,user):
        return user.feedbacks_received.count()

    def num_of_feeds_p(self, user):
        return user.feedbacks_received.filter(positive=True).count()

    class Meta:
        model = User
        fields = ('id', 'user_name', 'password', 'vote', 'number_of_feedbacks_received','number_of_positive_feedbacks_received')

class UserNoPwdSerializer(serializers.ModelSerializer):
    vote = serializers.SerializerMethodField('calculate_vote')
    number_of_feedbacks_received  = serializers.SerializerMethodField('num_of_feeds')
    number_of_positive_feedbacks_received = serializers.SerializerMethodField('num_of_feeds_p')


    def calculate_vote(self,user):
        base = 6
        votes = Vote.objects.all().filter(user=user)
        if votes.count()==0:
            return base
        cnt = 0
        for vote in votes:
            cnt += vote.value
        cnt /= votes.count()
        cnt -= 0.5
        return base + (cnt*8)

    def num_of_feeds(self,user):
        return user.feedbacks_received.count()

    def num_of_feeds_p(self, user):
        return user.feedbacks_received.filter(positive=True).count()

    class Meta:
        model = User
        fields = ('id', 'user_name', 'vote', 'number_of_feedbacks_received','number_of_positive_feedbacks_received')



class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields=('id', 'sender', 'receiver', 'description', 'positive')



class MatchSerializer(serializers.ModelSerializer):
    number_of_found_players = serializers.SerializerMethodField('num_of_found_players')
    distance = serializers.SerializerMethodField('dist')

    def num_of_found_players(self, match):
        return Plays.objects.all().filter(match=match).count();

    def dist(self,match):
	EARTH_RADIUS_KM = 6371;
        lat1Rad = radians(match.place_lat)
        lat2Rad = radians(self.context['m_lat'])
        deltaLonRad = radians(self.context['m_lon']-match.place_lon)
        dist = acos(sin(lat1Rad) * sin(lat2Rad) + cos(lat1Rad) * cos(lat2Rad) * cos(deltaLonRad)) * EARTH_RADIUS_KM;
	return dist
	
    class Meta:
        model = Match
        fields = ('id', 'organizer', 'date', 'place_lon', 'place_lat', 'place_name', 'players_number', 'number_of_found_players','distance')

class MatchPostSerializer(serializers.ModelSerializer):
 
      class Meta:
        model = Match
        fields = ('id', 'organizer', 'date', 'place_lon', 'place_lat', 'place_name', 'players_number')


class VoteSerializer(serializers.ModelSerializer):
    match_organizer  = serializers.SerializerMethodField('match_org')

    def match_org(self,vote):
        return vote.match.organizer.id

    class Meta:
        model = Vote
        fields = ('id','user','match','description','value','match_organizer')

class PlaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plays
        fields = ('id','user','match')

    
