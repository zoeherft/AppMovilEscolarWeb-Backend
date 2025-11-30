from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        fields = '__all__'
        
class AlumnoSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Alumnos
        fields = "__all__"

class MaestroSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Maestros
        fields = '__all__'

class ResponsableSerializer(serializers.ModelSerializer):
    """Serializer simplificado para mostrar responsables (maestros y admins)"""
    nombre_completo = serializers.SerializerMethodField()
    rol = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'nombre_completo', 'rol')
    
    def get_nombre_completo(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def get_rol(self, obj):
        # Determinar si es maestro o administrador
        if Maestros.objects.filter(user=obj).exists():
            return 'maestro'
        elif Administradores.objects.filter(user=obj).exists():
            return 'administrador'
        return 'desconocido'

class EventoAcademicoSerializer(serializers.ModelSerializer):
    responsable_info = ResponsableSerializer(source='responsable', read_only=True)
    
    class Meta:
        model = EventosAcademicos
        fields = '__all__'