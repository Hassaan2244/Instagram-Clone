from rest_framework import generics
from app.serializer import UserSerializer,UserLoginSerializer, UserProfileSerializer
from app.models import User
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginUserView(APIView):

    def post(self, request):
        # request.data (email, password)
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data["email"])
                if user.password == serializer.validated_data["password"]:
                    token = Token.objects.get_or_create(user=user)
                    return Response({ "success": True, "token": token[0].key })
                else:
                    return Response({ "success": False, "message": "incorrect password" })



            except:
                return Response({ "success": False, "message": "user does not exist" })

class RetrieveUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UpdateUser(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({ "success": True, "message": "user updated" })
        else:
            print(serializer.errors)
            return Response({ "success": False, "message": "error updating user" })
        

class DestroyUser(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            if pk == request.user.id:
                self.perform_destroy(request.user)
                return Response({ "success": True, "message": "user deleted" })
            else:
                return Response({ "success": False, "message": "not enough permissions" })
        except:
            return Response({ "success": False, "message": "user does not exist" })
        

class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        user = get_object_or_404(User, pk=pk) if pk else request.user
        serializer = UserProfileSerializer(user)
        return Response({"success": True, "profile": serializer.data})

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Profile updated", "profile": serializer.data})
        return Response({"success": False, "errors": serializer.errors}, status=400)