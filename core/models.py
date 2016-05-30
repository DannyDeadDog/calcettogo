from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length=40)
    password = models.CharField(max_length=40)


class Feedback(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name='feedbacks_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name='feedbacks_received')
    description = models.CharField(max_length=200)
    positive = models.BooleanField(null=False)

class Match(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('date published')
    place_lon = models.FloatField(null=False)
    place_lat = models.FloatField(null=False)
    place_name = models.CharField(max_length=200)
    players_number = models.IntegerField(null=False)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    value = models.FloatField(null=False)

class Plays(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

