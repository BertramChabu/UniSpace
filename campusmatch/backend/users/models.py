from django.db import models

class User(models.Model):
    uid = models.CharField(max_length=255, unique=True)  # Firebase UID
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=50, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    age = models.IntegerField(blank=True, null=True)
    preferred_gender = models.CharField(max_length=50, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'), ('Any', 'Any')], default='Any')
    preferred_age_min = models.IntegerField(blank=True, null=True, default=18)
    preferred_age_max = models.IntegerField(blank=True, null=True, default=30)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    swiped_users = models.ManyToManyField('self', through='Swipe', symmetrical=False)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name

class Match(models.Model):
    user1 = models.ForeignKey(User, related_name='match_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='match_user2', on_delete=models.CASCADE)
    is_matched = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Swipe(models.Model):
    swiper = models.ForeignKey(User, related_name='swiper', on_delete=models.CASCADE)
    swiped = models.ForeignKey(User, related_name='swiped', on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
