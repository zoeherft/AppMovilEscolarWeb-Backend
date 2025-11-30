from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.utils import timezone
import json

from app_movil_escolar_api.models import EventosAcademicos, Maestros, Administradores, Alumnos, BearerTokenAuthentication
from app_movil_escolar_api.serializers import EventoAcademicoSerializer, ResponsableSerializer


class EventosView(APIView):
    """Vista para CRUD de Eventos Académicos"""
    authentication_classes = [BearerTokenAuthentication]
    
    def get(self, request):
        """Obtener un evento por ID o lista filtrada por rol"""
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return Response({"error": "Token requerido"}, status=status.HTTP_401_UNAUTHORIZED)
        
        id_evento = request.GET.get('id')
        
        if id_evento:
            # Obtener evento específico por ID
            try:
                evento = EventosAcademicos.objects.get(id=id_evento)
                serializer = EventoAcademicoSerializer(evento)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except EventosAcademicos.DoesNotExist:
                return Response({"error": "Evento no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "ID requerido"}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        """Crear un nuevo evento académico (solo administradores)"""
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return Response({"error": "Token requerido"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Verificar que el usuario es administrador
        user = request.user
        if not Administradores.objects.filter(user=user).exists():
            return Response({"error": "Solo los administradores pueden crear eventos"}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        
        try:
            # Validar campos requeridos
            campos_requeridos = ['nombre_evento', 'tipo_evento', 'fecha_realizacion', 
                                'hora_inicio', 'hora_fin', 'lugar', 'publico_objetivo', 
                                'descripcion', 'cupo_maximo']
            
            for campo in campos_requeridos:
                if campo not in data or not data[campo]:
                    return Response({"error": f"El campo {campo} es requerido"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Procesar público objetivo (viene como array)
            publico_objetivo = data.get('publico_objetivo')
            if isinstance(publico_objetivo, list):
                publico_objetivo_str = json.dumps(publico_objetivo)
            else:
                publico_objetivo_str = publico_objetivo
            
            # Obtener responsable si existe
            responsable = None
            if data.get('responsable_id'):
                try:
                    responsable = User.objects.get(id=data['responsable_id'])
                except User.DoesNotExist:
                    return Response({"error": "Responsable no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            
            # Crear evento
            evento = EventosAcademicos.objects.create(
                nombre_evento=data['nombre_evento'],
                tipo_evento=data['tipo_evento'],
                fecha_realizacion=data['fecha_realizacion'],
                hora_inicio=data['hora_inicio'],
                hora_fin=data['hora_fin'],
                lugar=data['lugar'],
                publico_objetivo=publico_objetivo_str,
                programa_educativo=data.get('programa_educativo'),
                responsable=responsable,
                descripcion=data['descripcion'],
                cupo_maximo=data['cupo_maximo']
            )
            
            return Response({"evento_created_id": evento.id}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        """Actualizar un evento académico (solo administradores)"""
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return Response({"error": "Token requerido"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Verificar que el usuario es administrador
        user = request.user
        if not Administradores.objects.filter(user=user).exists():
            return Response({"error": "Solo los administradores pueden editar eventos"}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        id_evento = data.get('id')
        
        if not id_evento:
            return Response({"error": "ID del evento requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            evento = EventosAcademicos.objects.get(id=id_evento)
            
            # Actualizar campos
            if 'nombre_evento' in data:
                evento.nombre_evento = data['nombre_evento']
            if 'tipo_evento' in data:
                evento.tipo_evento = data['tipo_evento']
            if 'fecha_realizacion' in data:
                evento.fecha_realizacion = data['fecha_realizacion']
            if 'hora_inicio' in data:
                evento.hora_inicio = data['hora_inicio']
            if 'hora_fin' in data:
                evento.hora_fin = data['hora_fin']
            if 'lugar' in data:
                evento.lugar = data['lugar']
            if 'publico_objetivo' in data:
                publico = data['publico_objetivo']
                if isinstance(publico, list):
                    evento.publico_objetivo = json.dumps(publico)
                else:
                    evento.publico_objetivo = publico
            if 'programa_educativo' in data:
                evento.programa_educativo = data['programa_educativo']
            if 'responsable_id' in data:
                if data['responsable_id']:
                    try:
                        evento.responsable = User.objects.get(id=data['responsable_id'])
                    except User.DoesNotExist:
                        pass
                else:
                    evento.responsable = None
            if 'descripcion' in data:
                evento.descripcion = data['descripcion']
            if 'cupo_maximo' in data:
                evento.cupo_maximo = data['cupo_maximo']
            
            evento.update = timezone.now()
            evento.save()
            
            serializer = EventoAcademicoSerializer(evento)
            return Response({
                "message": "Evento actualizado correctamente",
                "evento": serializer.data
            }, status=status.HTTP_200_OK)
            
        except EventosAcademicos.DoesNotExist:
            return Response({"error": "Evento no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request):
        """Eliminar un evento académico (solo administradores)"""
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return Response({"error": "Token requerido"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Verificar que el usuario es administrador
        user = request.user
        if not Administradores.objects.filter(user=user).exists():
            return Response({"error": "Solo los administradores pueden eliminar eventos"}, status=status.HTTP_403_FORBIDDEN)
        
        id_evento = request.GET.get('id')
        
        if not id_evento:
            return Response({"error": "ID del evento requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            evento = EventosAcademicos.objects.get(id=id_evento)
            evento.delete()
            return Response({"message": "Evento eliminado correctamente"}, status=status.HTTP_200_OK)
        except EventosAcademicos.DoesNotExist:
            return Response({"error": "Evento no encontrado"}, status=status.HTTP_404_NOT_FOUND)


class EventosAllView(APIView):
    """Vista para obtener todos los eventos (filtrados por rol del usuario)"""
    authentication_classes = [BearerTokenAuthentication]
    
    def get(self, request):
        """Obtener lista de eventos según el rol del usuario"""
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return Response({"error": "Token requerido"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = request.user
        
        # Determinar rol del usuario
        es_admin = Administradores.objects.filter(user=user).exists()
        es_maestro = Maestros.objects.filter(user=user).exists()
        es_alumno = Alumnos.objects.filter(user=user).exists()
        
        # Obtener todos los eventos
        eventos = EventosAcademicos.objects.all()
        
        if es_admin:
            # Admin ve todos los eventos
            pass
        elif es_maestro:
            # Maestro ve eventos para Profesores y Público general
            eventos_filtrados = []
            for evento in eventos:
                try:
                    publico = json.loads(evento.publico_objetivo)
                except:
                    publico = []
                if 'Profesores' in publico or 'Público general' in publico:
                    eventos_filtrados.append(evento)
            eventos = eventos_filtrados
        elif es_alumno:
            # Alumno ve eventos para Estudiantes y Público general
            eventos_filtrados = []
            for evento in eventos:
                try:
                    publico = json.loads(evento.publico_objetivo)
                except:
                    publico = []
                if 'Estudiantes' in publico or 'Público general' in publico:
                    eventos_filtrados.append(evento)
            eventos = eventos_filtrados
        else:
            # Usuario sin rol definido, solo eventos de público general
            eventos_filtrados = []
            for evento in eventos:
                try:
                    publico = json.loads(evento.publico_objetivo)
                except:
                    publico = []
                if 'Público general' in publico:
                    eventos_filtrados.append(evento)
            eventos = eventos_filtrados
        
        serializer = EventoAcademicoSerializer(eventos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResponsablesView(APIView):
    """Vista para obtener la lista de responsables (maestros y administradores)"""
    authentication_classes = [BearerTokenAuthentication]
    
    def get(self, request):
        """Obtener lista de usuarios que pueden ser responsables de eventos"""
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return Response({"error": "Token requerido"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Obtener IDs de usuarios que son maestros o administradores
        maestros_user_ids = Maestros.objects.values_list('user_id', flat=True)
        admins_user_ids = Administradores.objects.values_list('user_id', flat=True)
        
        # Combinar IDs únicos
        user_ids = set(list(maestros_user_ids) + list(admins_user_ids))
        
        # Obtener usuarios
        usuarios = User.objects.filter(id__in=user_ids)
        
        serializer = ResponsableSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
