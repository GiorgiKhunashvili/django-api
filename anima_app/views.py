from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import UserDataSerializer, UserRegistrationSerializer, ChanagePasswordSerializer
from .models import UserAccount
from rest_framework.authtoken.models import Token
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

    return Response(serializer.data)


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


@api_view(['PATCH'])
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
    # serializer = UserDeleteChecker(user_data, data=request.data)
    # if serializer.is_valid():
    #     password_data = serializer.validated_data['confirm_password']
    #     print(user.password)
    #     if password_data != user.password:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if user.id != user_data.id:
        return Response({"response": "You dont have permission to access "}, status=status.HTTP_400_BAD_REQUEST)

    operation = user_data.delete()
    data = {}
    if operation:
        data["success"] = "deleted successfuly"
        return Response(data=data)
    else:
        data["failure"] = "delete failed"
        return Response(data=data)


@api_view(['POST', ])
def registration_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['response'] = 'successfully registered a new user'
        data['email'] = account.email
        data['username'] = account.username
        data['name'] = account.name
        token = Token.objects.get(user=account).key
        data['token'] = token
    else:
        data = serializer.errors
    return Response(data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def api_password_change_view(requset):
    user = requset.user
    serializer = ChanagePasswordSerializer(data=requset.data)

    if serializer.is_valid():
        # check old passord
        if not user.check_password(serializer.data.get("old_password")):
            return Response({"old_password": "wrong password"}, status=status.HTTP_400_BAD_REQUEST)
        # set_password also hashes the password that the user will get
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response("Success.", status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





