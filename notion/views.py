from django.contrib.auth.models import User as UserDjangoModel
from django.contrib.auth.models import Group as GroupDjangoModel
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CreateDjangoUserSerializer, GetDjangoUserSerializer, CreateDjangoGroupSerializer, GetDjangoGroupSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User, Group
from .serializers import CreateDjangoUserSerializer
from NotionHackton.apiCreatePage import create_notion_page
from NotionHackton.apiUpdatePage import update_notion_page
from NotionHackton.apiGetPages import search_notion_pages

class CreateDjangoUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        print("---CREATE DJANGO USER---")
        print(request.data)
        print("---CREATE DJANGO USER---")

        serializer = CreateDjangoUserSerializer(data=request.data)
        if not serializer.is_valid():
            error = serializer.errors
            campos_con_error = ', '.join(error.keys())
            mensaje_error = "Falta dato(s) en el campo(s): " + campos_con_error
            res = { 
                "error": "No se pudo crear el usuario, campos no válidos.", 
                "errorMessage" : mensaje_error,
                "errorAction" : "Error al evaluar campos únicos, no todos los campos son válidos"
                }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        print("---SERIALIZER DATA CORRECT---")

        try:
            user = User.objects.create_user(
                username=data['user'],
                password=data['password'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            group = Group.objects.get(name=data['group'])
            user.groups.add(group)
            user.save()
            print("---USER CREATED AND SAVED---")
            res = {
                "message": "User created successfully.",
                "user": user.username,
            }
            return Response(res, status=status.HTTP_201_CREATED)
        
        except Group.DoesNotExist:
            res = {
                "error": "No se pudo crear el usuario.",
                "errorMessage" : "El grupo especificado no existe.",
                "errorAction" : "Error al encontrar el grupo especificado"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            res = {
                "error": "No se pudo crear el usuario.",
                "errorMessage" : str(e),
                "errorAction" : "Error al insertar en la base de datos"
            }
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetDjangoUser(APIView):
    def post(self, request):
        print("---GET DJANGO USER---")
        
        serializer = GetDjangoUserSerializer(data=request.data)
        if not serializer.is_valid():
            error = serializer.errors
            campos_con_error = ', '.join(error.keys())
            mensaje_error = "Falta dato(s) en el campo(s): " + campos_con_error
            res = { 
                "error": "No se pudo obtener el usuario, campos no válidos.", 
                "errorMessage" : mensaje_error,
                "errorAction" : "Error al evaluar campos requeridos, no todos los campos son válidos"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            data = serializer.validated_data
            user = User.objects.filter(username=data['user']).first()
            if not user:
                res = {
                    "error": "No se encontró el usuario.",
                    "errorMessage": "El usuario especificado no existe en la base de datos.",
                    "errorAction": "Verifique que el nombre de usuario sea correcto"
                }
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            print("---USER RETRIEVED---")
            res = {
                "message": "User retrieved successfully.",
                "user": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "group": user.groups.first().name
                
             

            }
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            res = {
                "error": "No se pudo obtener el usuario.",
                "errorMessage": str(e),
                "errorAction": "Error al recuperar datos de la base de datos"
            }
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CreateGroup(APIView):
    def post(self, request):
        print("---CREATE GROUP---")
        print(request.data)
        print("---CREATE GROUP---")

        serializer = CreateDjangoGroupSerializer(data=request.data)
        if not serializer.is_valid():
            error = serializer.errors
            campos_con_error = ', '.join(error.keys())
            mensaje_error = "Falta dato(s) en el campo(s): " + campos_con_error
            res = { 
                "error": "No se pudo crear el grupo, campos no válidos.", 
                "errorMessage" : mensaje_error,
                "errorAction" : "Error al evaluar campos requeridos, no todos los campos son válidos"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        print("---SERIALIZER DATA CORRECT---")

        try:
            group = Group.objects.create(name=data['name'])
            print("---GROUP CREATED---")
            res = {
                "message": "Group created successfully.",
                "group": group.name,
            }
            return Response(res, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            res = {
                "error": "No se pudo crear el grupo.",
                "errorMessage": str(e),
                "errorAction": "Error al insertar en la base de datos"
            }
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetGroup(APIView):
    def get(self, request):
        groups = GroupDjangoModel.objects.all()
        serializer = GetDjangoGroupSerializer(groups, many=True)
        return Response(serializer.data, status=200)

class UpdateNotionPageView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        new_title = request.data.get("new_title")
        new_groups = request.data.get("new_groups")

        if not new_title or not new_groups:
            return Response({"error": "new_title and new_groups are required"}, status=status.HTTP_400_BAD_REQUEST)
        print("new_title", new_title)
        result = update_notion_page(new_title, new_groups)

        if result:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to update the Notion page"}, status=status.HTTP_400_BAD_REQUEST)