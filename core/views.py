from django.contrib.auth import mixins
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import mixins

from core.serializers import *


class MatchList(APIView):
    """
    List all matches in a certain ray, or create a new match.
    """

    def get(self, request,lat,lon,page,count):
        page = int(page)
        count = int(count)
        if page<0 or count <0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        i = page*count
        j = (page+1)*count;
        query = "SELECT * FROM core_match m WHERE m.date > NOW() ORDER BY ((ACOS(SIN(" + lat + " * PI() / 180) * SIN(m.place_lat * PI() / 180) + COS(" + lat + " * PI() / 180) * COS(m.place_lat * PI() / 180) * COS((" + lon + " - m.place_lon) * PI() / 180)) * 180 / PI()) * 60 * 1.60934 ) ;"
        matches = Match.objects.all().raw(query)
        serializer = MatchSerializer(matches[i:j],context={'m_lon': float(lon), 'm_lat': float(lat)},many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MatchPostSerializer(data=request.data)
	if authenticate_user(request.data['organizer'],request.data['user_password']):
        	if serializer.is_valid():
        	    serializer.save()
                    match = Match.objects.get(pk=serializer.data['id'])
                    serializer = MatchSerializer(match,context={'m_lon': match.place_lon, 'm_lat': match.place_lat})
        	    return Response(serializer.data, status=status.HTTP_201_CREATED)
		print (serializer.errors)
        	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	return Response(status=status.HTTP_401_UNAUTHORIZED)

class UserMatchList(APIView):
    """
    List all matches organized by a user.
    """

    def get(self, request,user,lat,lon,page,count):
        page = int(page)
        count = int(count)
        if page<0 or count <0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        i = page*count
        j = (page+1)*count;
        matches = Match.objects.all().filter(organizer=user)
        serializer = MatchSerializer(matches[i:j],context={'m_lon': float(lon), 'm_lat': float(lat)},many=True)
        return Response(serializer.data)


class MatchDetail(APIView):

    def get(self, request, match, lat, lon, *args, **kwargs):
        try:
		ris = Match.objects.all().get(pk=int(match))
	except:
		return Response(status=status.HTTP_400_BAD_REQUEST)
	serializer = MatchSerializer(ris,context={'m_lon': float(lon), 'm_lat': float(lat)})
	return Response(serializer.data)
	"""
    def put(self, request, *args, **kwargs):
	if authenticate_user(request.data['organizer'],request.data['user_password']):
        	return self.update(request, *args, **kwargs)
	return Response(status=status.HTTP_401_UNAUTHORIZED)


    def delete(self, request, *args, **kwargs):
	if authenticate_user(request.data['organizer'],request.data['user_password']):
        	return self.destroy(request, *args, **kwargs)
	return Response(status=status.HTTP_401_UNAUTHORIZED)

	"""
class UserDetail(APIView):


    def get(self, request, user, *args, **kwargs):
        try:
		ris = User.objects.all().get(id=user)
	except:
		return Response(status=status.HTTP_400_BAD_REQUEST)
	serializer = UserNoPwdSerializer(ris)
	return Response(serializer.data)




class MatchVoteList(APIView):
    """
    List all votes in a certain match, or create a new vote for that match.
    """

    def get(self, request, match,format=None):
        votes = Vote.objects.all().filter(match=match)
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VoteSerializer(data=request.data)
        user = Match.objects.get(id=request.data['match']).organizer
        if authenticate_user(user.id,request.data['user_password']):
            votes = Vote.objects.all().filter(user=request.data['user']).filter(match=request.data['match'])
            if votes.count():
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class UserVoteList(APIView):
    """
    List all votes given to a user.
    """

    def get(self, request, user,format=None):
        votes = Vote.objects.all().filter(user=user)
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)


class VoteDetail(APIView):
    """
    List all votes in a certain match, or create a new vote for that match.
    """

    def get(self, request, match, user,format=None):
        try:
            vote = Vote.objects.all().filter(match=match).filter(user=user)[0:1].get()
            serializer = VoteSerializer(vote)
            return Response(serializer.data)
        except:
            raise Http404

    def delete(self, request,format=None):
        if match!=request.data['match'] or user != request.data['user']:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            vote = Vote.objects.all().filter(match=request.data['match']).filter(user=request.data['user'])[0:1].get()
            user = vote.match.organizer
            if authenticate_user(user.id,request.data['user_password']):
                vote.delete()
                return Response(request.data, status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class MatchPlayersList(APIView):
    """
    List all players, or create a new player.
    """
    def get(self, request, match, format=None):
        users = User.objects.all().filter(plays__match_id=match)
        serializer = UserNoPwdSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
	if authenticate_user(request.data['user'],request.data['user_password']):
            number_of_players = Plays.objects.all().filter(match=request.data['match']).count()
            m_match = Match.objects.get(pk=request.data['match'])
            if number_of_players >= m_match.players_number:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if Plays.objects.all().filter(match=request.data['match']).filter(user=request.data['user']).count()>1:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer = PlaysSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, format=None):
        if authenticate_user(request.data['user'],request.data['user_password']):
            try:
                plays = Plays.objects.get(request.data['id'])
                plays.delete()
                return  Response(status=status.HTTP_204_NO_CONTENT)
            except:
                raise Http404
        return Response(status=status.HTTP_401_UNAUTHORIZED) 

class Login(APIView):

    def post(self, request, format=None):
        userName = request.data["user_name"]
        password = request.data["password"]
        try:
            user = User.objects.get(user_name=userName)
        except:
            user = User(user_name=userName,password=password)
            user.save()
        if user.password != password:
            raise Http404
        else:
            serializer = UserSerializer(user)
            return Response(serializer.data)

class FeedbackList(APIView):
    """
    List all votes in a certain match, or create a new vote for that match.
    """

    def get(self, request, receiver,format=None):
        feeds = Feedback.objects.all().filter(receiver=receiver)
        serializer = FeedbackSerializer(feeds, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FeedbackSerializer(data=request.data)
        if authenticate_user(request.data['sender'],request.data['user_password']):
            feeds = Feedback.objects.all().filter(sender=request.data['sender']).filter(receiver=request.data['receiver'])
            if feeds.count():
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, format=None):
        try:
            feed = Feedback.objects.get(id=request['id'])
            if authenticate_user(feed.sender.id, request.data['user_password']):
                feed.delete()
                return Response(request.data, status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


def authenticate_user(user_id, password):
    return User.objects.all().filter(id=user_id).filter(password=password).count()


