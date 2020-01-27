from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserDataSerializer, UserRegistrationSerializer, ChanagePasswordSerializer, DeleteUserSerializer,
    ResetPassowrdEmailSerializer, ResetPasswordConfirmSerializer
)
from .models import UserAccount
from rest_framework.authtoken.models import Token

from django.core.mail import send_mail
from .helper import get_token
from django.conf import settings
from django.utils import timezone
# Create your views here.


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def api_detail_view(request, username):
    try:
        data = UserAccount.objects.get(username=username)
    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user
    if user.id != data.id:
        return Response({"response": "You dont have permission to access "}, status=status.HTTP_400_BAD_REQUEST)
    # data = json.dumps(data)
    serializer = UserDataSerializer(data)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated, ))
def api_profile_update_view(request, username):
    try:
        user_data = UserAccount.objects.get(username=username)
    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user
    if user.id != user_data.id:
        return Response({"response": "You dont have permission to access "}, status=status.HTTP_400_BAD_REQUEST)
    serializer = UserDataSerializer(user_data, data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data["success"] = "updated successfuly"
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', ])
@permission_classes((IsAuthenticated, ))
def api_profile_partial_update(request, username):
    try:
        user_data = UserAccount.objects.get(username=username)
    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user.id != user_data.id:
        return Response({"response": "You dont have permission to access "}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserDataSerializer(user_data, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated, ))
def api_profile_delete_view(request, username):
    try:
        user_data = UserAccount.objects.get(username=username)
    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    serializer = DeleteUserSerializer(data=request.data)
    if user.id != user_data.id:
        return Response({"response": "You dont have permission to access "}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():

        check_password = user.check_password(serializer.data.get("password"))
        if not check_password:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    operation = user_data.delete()
    data = {}
    if operation:
        data["success"] = "deleted successfuly"
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        data["failure"] = "delete failed"
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
def registration_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['response'] = 'successfully registered a new user'
        data['email'] = account.email
        data['name'] = account.name
        token = Token.objects.get(user=account).key
        data['token'] = token
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def api_password_change_view(requset):
    user = requset.user
    serializer = ChanagePasswordSerializer(data=requset.data)

    if serializer.is_valid():
        # check old passord
        # check_password = bcrypt.checkpw(serializer.data.get("old_password").encode('utf-8'), user.password)
        check_password = user.check_password(serializer.data.get("old_password"))
        if check_password == False:
            return Response({"old_password": "wrong password"}, status=status.HTTP_400_BAD_REQUEST)
        # set_password also hashes the password that the user will get
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response("Success.", status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def api_reset_password(request):
    serializer = ResetPassowrdEmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get("email")
        random_str = get_token()
        user = UserAccount.objects.filter(email=email).first()
        if user:
            subject = "ANIMA"
            message = f"miha hamodi {random_str}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)
            user.reset_password_token = random_str
            user.token_sent_time = timezone.now()
            user.save()
            print(user.reset_password_token)
            print(user.token_sent_time)
            return Response("Success", status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def api_reset_password_confirm(request):
    serializer = ResetPasswordConfirmSerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.data.get("token")
        print(token)
        user = UserAccount.objects.filter(reset_password_token=token).first()
        print(f'{user} user')
        print(serializer.data.get("new_password"))
        if user and user.reset_password_token != "":
            # checking time out
            if user.token_sent_time + timezone.timedelta(minutes=30) > timezone.now():
                # cheking password if mutchs
                if serializer.data.get("new_password") == serializer.data.get("confirm_password"):
                    print(serializer.data.get("new_password"))
                    # setting new password
                    user.set_password(serializer.data.get("new_password"))
                    user.reset_password_token = ""
                    user.save()
                else:
                    return Response("passwords don't match", status=status.HTTP_400_BAD_REQUEST)
                return Response("password was successfully reset", status=status.HTTP_200_OK)
            else:
                # time out
                user.reset_password_token = ""
                return Response("Time out token not found", status=status.HTTP_400_BAD_REQUEST)
        else:
            # token not found
            return Response("reset password request not found", status=status.HTTP_400_BAD_REQUEST)





