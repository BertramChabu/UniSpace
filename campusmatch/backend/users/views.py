from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth
from .models import User, Match, Message, Notification, Swipe
from .serializers import UserSerializer , MessageSerializer, MatchSerializer, NotificationSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Match, Message, Notification
import 

config={
    "apiKey": "AIzaSyAG2PkTRA-BSP1Re4Jvz-Nv9GqxEd4NkLE",
    "authDomain": "campusmatch-a7033.firebaseapp.com",
    "databaseURL": "https://console.firebase.google.com/project/campusmatch-a7033/database/campusmatch-a7033-default-rtdb/data/~2F",
    "projectId": "campusmatch-a7033",
    "storageBucket": "campusmatch-a7033.firebasestorage.app",
    "messagingSenderId": "777412564645",
    "appId": "1:777412564645:web:76485b605dff7f10401f4c",
    "measurementId": "G-N34CQ2FLNP",
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database =  firebase.database()

def index(request):
    userid = database.child('users').child('uid123').get().val()
    username = database.child('users').child('name').get().val()
    userage = database.child('users').child('age').get().val()
    userbio = database.child('users').child('bio').get().val()
    useremail = database.child('users').child('email').get().val()
    return render(request, 'index.html', {
        "userid":userid,
        "username":username,
        "userage":userage,
        "userbio":userbio,
        "useremail":useremail,
    })




class RegisterUserView(APIView):
    def post(self, request):
        token= request.data.get('token')
        decoded_token = auth.verify_id_token(token)
        uid =  decoded_token['uid']
        email = decoded_token['email']
        name = decoded_token['name', '']

        if not email.endswith('.ac.ke') and not email.endswith('.edu'):
            return Response({'error': 'Only university emails are allowed'}, status=status.HTTP_403_FORBIDDEN)


        user, created = User.objects.get_or_create(uid=uid, defaults={'email': email, 'name': name})
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class LoginUserView(APIView):
    def post(self, request):
        token = request.data.get('token')
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']

        try:
            user = User.obkects.get(uid=uid)
            serializer= UserSerializer(user)
            return Response(serializer.data, stattus=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)




class UpdateProfileView(APIView):
    def put(self, request):
        token = request.data.get('token')
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']

        try:
            user = User.objects.get(uid=uid)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class MatchUsersView(APIView):
    def post(self, request):
        user1_id = request.data.get('user1_id')
        user2_id = request.data.get('user2_id')

        try:
            user1 = User.objects.get(uid=user1_id)
            user2 = User.objects.get(uid=user2_id)

            match, created = Match.objects.get_or_create(user1=user1, user2=user2, defaults={'is_matched': True})
            serializer = MatchSerializer(match)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class SendMessageView(APIView):
    def post(self, request):
        sender_id = request.data.get('sender_id')
        receiver_id = request.data.get('receiver_id')
        content = request.data.get('content')

        try:
            sender = User.objects.get(uid=sender_id)
            receiver = User.objects.get(uid=receiver_id)
            message = Message.objects.create(sender=sender, receiver=receiver, content=content)
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class NotificationView(APIView):
    def get(self, request, uid):
        notifications = Notification.objects.filter(user__uid=uid, is_read=False)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_id = request.data.get('user_id')
        message = request.data.get('message')

        try:
            user = User.objects.get(uid=user_id)
            notification = Notification.objects.create(user=user, message=message)
            serializer = NotificationSerializer(notification)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class SwipeUserView(APIView):
    def post(self, request):
        swiper_uid = request.data.get('swiper_uid')
        swiped_uid = request.data.get('swiped_uid')
        liked = request.data.get('liked', False)

        try:
            swiper = User.objects.get(uid=swiper_uid)
            swiped = User.objects.get(uid=swiped_uid)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        Swipe.objects.create(swiper=swiper, swiped=swiped, liked=liked)

        # Check for mutual match
        if liked and Swipe.objects.filter(swiper=swiped, swiped=swiper, liked=True).exists():
            Match.objects.create(user1=swiper, user2=swiped, is_matched=True)
            return Response({"message": "It's a match!"}, status=status.HTTP_201_CREATED)

        return Response({"message": "Swipe recorded"}, status=status.HTTP_201_CREATED)



def register(request):
    return render(request, "register.html")

def chat(request, match_id):
    return render(request, "chat.html", {"match_id": match_id})

def login(request):
    return render(request, "login.html")


@login_required
def profile_settings(request):
    user = request.user
    profile = User.objects.get(user=user)

    if request.method == "POST":
        profile.bio = request.POST.get("bio", profile.bio)
        profile.interests = request.POST.get("interests", profile.interests)
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profile_settings")

    return render(request, "profile_settings.html", {"profile": profile})

@login_required
def chat(request, match_id):
    match = Match.objects.get(id=match_id)
    messages = Message.objects.filter(match=match).order_by("timestamp")

    if request.method == "POST":
        message_text = request.POST.get("message")
        if message_text:
            Message.objects.create(match=match, sender=request.user, text=message_text)

    return render(request, "chat.html", {"match": match, "messages": messages})

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-timestamp")

    return render(request, "notifications.html", {"notifications": notifications})
