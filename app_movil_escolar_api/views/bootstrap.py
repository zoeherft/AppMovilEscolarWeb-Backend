import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import date, time, datetime
import json

class VersionView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        version = getattr(settings, "APP_VERSION", os.getenv("APP_VERSION", "1.0.0"))
        return Response({"version": version})


class PoblarBaseDatosView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        clave = request.GET.get('clave')
        if clave != 'poblar2025seguro':
            return Response({"error": "Clave incorrecta"}, status=status.HTTP_403_FORBIDDEN)
        
        from app_movil_escolar_api.models import Administradores, Maestros, Alumnos, EventosAcademicos
        
        resultados = {
            'admins_creados': 0,
            'maestros_creados': 0,
            'alumnos_creados': 0,
            'eventos_creados': 0
        }
        
        # ADMINISTRADORES
        admins_data = [
            {'username': 'admin.carlos', 'password': 'Admin123!', 'first_name': 'Carlos', 'last_name': 'García López', 'email': 'carlos.garcia@universidad.edu.mx', 'clave_admin': 'ADM-001', 'telefono': '4771234567', 'rfc': 'GALC850315ABC', 'edad': 39, 'ocupacion': 'Coordinador de Sistemas'},
            {'username': 'admin.maria', 'password': 'Admin123!', 'first_name': 'María', 'last_name': 'Hernández Ruiz', 'email': 'maria.hernandez@universidad.edu.mx', 'clave_admin': 'ADM-002', 'telefono': '4772345678', 'rfc': 'HERM900420DEF', 'edad': 34, 'ocupacion': 'Jefa de Control Escolar'},
            {'username': 'admin.jose', 'password': 'Admin123!', 'first_name': 'José', 'last_name': 'Martínez Soto', 'email': 'jose.martinez@universidad.edu.mx', 'clave_admin': 'ADM-003', 'telefono': '4773456789', 'rfc': 'MASJ880612GHI', 'edad': 36, 'ocupacion': 'Director de Facultad'},
        ]
        
        admin_users = []
        for data in admins_data:
            user, created = User.objects.get_or_create(username=data['username'], defaults={'first_name': data['first_name'], 'last_name': data['last_name'], 'email': data['email']})
            if created:
                user.set_password(data['password'])
                user.save()
                resultados['admins_creados'] += 1
            Administradores.objects.get_or_create(user=user, defaults={'clave_admin': data['clave_admin'], 'telefono': data['telefono'], 'rfc': data['rfc'], 'edad': data['edad'], 'ocupacion': data['ocupacion']})
            Token.objects.get_or_create(user=user)
            admin_users.append(user)
        
        # MAESTROS
        maestros_data = [
            {'username': 'mtro.rodriguez', 'password': 'Maestro123!', 'first_name': 'Roberto', 'last_name': 'Rodríguez Vega', 'email': 'roberto.rodriguez@universidad.edu.mx', 'id_trabajador': 'MTR-2015-001', 'fecha_nacimiento': datetime(1975, 3, 15), 'telefono': '4774567890', 'rfc': 'ROVR750315JKL', 'cubiculo': 'C-101', 'edad': 49, 'area_investigacion': 'Inteligencia Artificial', 'materias_json': json.dumps(['Programación Avanzada', 'Machine Learning'])},
            {'username': 'mtro.gonzalez', 'password': 'Maestro123!', 'first_name': 'Ana', 'last_name': 'González Pérez', 'email': 'ana.gonzalez@universidad.edu.mx', 'id_trabajador': 'MTR-2016-002', 'fecha_nacimiento': datetime(1980, 7, 22), 'telefono': '4775678901', 'rfc': 'GOPA800722MNO', 'cubiculo': 'C-102', 'edad': 44, 'area_investigacion': 'Bases de Datos', 'materias_json': json.dumps(['Bases de Datos I', 'SQL Avanzado'])},
            {'username': 'mtro.lopez', 'password': 'Maestro123!', 'first_name': 'Fernando', 'last_name': 'López Castro', 'email': 'fernando.lopez@universidad.edu.mx', 'id_trabajador': 'MTR-2018-003', 'fecha_nacimiento': datetime(1978, 11, 8), 'telefono': '4776789012', 'rfc': 'LOCF781108PQR', 'cubiculo': 'C-103', 'edad': 46, 'area_investigacion': 'Seguridad Informática', 'materias_json': json.dumps(['Seguridad en Redes', 'Criptografía'])},
            {'username': 'mtro.sanchez', 'password': 'Maestro123!', 'first_name': 'Laura', 'last_name': 'Sánchez Morales', 'email': 'laura.sanchez@universidad.edu.mx', 'id_trabajador': 'MTR-2019-004', 'fecha_nacimiento': datetime(1985, 2, 28), 'telefono': '4777890123', 'rfc': 'SAML850228STU', 'cubiculo': 'C-104', 'edad': 39, 'area_investigacion': 'Desarrollo Web', 'materias_json': json.dumps(['Angular', 'Django'])},
            {'username': 'mtro.ramirez', 'password': 'Maestro123!', 'first_name': 'Miguel', 'last_name': 'Ramírez Torres', 'email': 'miguel.ramirez@universidad.edu.mx', 'id_trabajador': 'MTR-2020-005', 'fecha_nacimiento': datetime(1982, 9, 14), 'telefono': '4778901234', 'rfc': 'RATM820914VWX', 'cubiculo': 'C-105', 'edad': 42, 'area_investigacion': 'Sistemas Operativos', 'materias_json': json.dumps(['Linux', 'Servidores'])},
        ]
        
        maestro_users = []
        for data in maestros_data:
            user, created = User.objects.get_or_create(username=data['username'], defaults={'first_name': data['first_name'], 'last_name': data['last_name'], 'email': data['email']})
            if created:
                user.set_password(data['password'])
                user.save()
                resultados['maestros_creados'] += 1
            Maestros.objects.get_or_create(user=user, defaults={'id_trabajador': data['id_trabajador'], 'fecha_nacimiento': data['fecha_nacimiento'], 'telefono': data['telefono'], 'rfc': data['rfc'], 'cubiculo': data['cubiculo'], 'edad': data['edad'], 'area_investigacion': data['area_investigacion'], 'materias_json': data['materias_json']})
            Token.objects.get_or_create(user=user)
            maestro_users.append(user)
        
        # ALUMNOS
        alumnos_data = [
            {'username': 'alu.perez', 'password': 'Alumno123!', 'first_name': 'Juan', 'last_name': 'Pérez Mendoza', 'email': 'juan.perez@alumnos.edu.mx', 'matricula': '20210001', 'curp': 'PEMJ030512HGTRNNA1', 'rfc': 'PEMJ030512ABC', 'fecha_nacimiento': datetime(2003, 5, 12), 'edad': 21, 'telefono': '4779012345', 'ocupacion': 'Estudiante ICC'},
            {'username': 'alu.torres', 'password': 'Alumno123!', 'first_name': 'Andrea', 'last_name': 'Torres Ruiz', 'email': 'andrea.torres@alumnos.edu.mx', 'matricula': '20210002', 'curp': 'TORA020815MGTRRND2', 'rfc': 'TORA020815DEF', 'fecha_nacimiento': datetime(2002, 8, 15), 'edad': 22, 'telefono': '4770123456', 'ocupacion': 'Estudiante LCC'},
            {'username': 'alu.diaz', 'password': 'Alumno123!', 'first_name': 'Diego', 'last_name': 'Díaz Fernández', 'email': 'diego.diaz@alumnos.edu.mx', 'matricula': '20210003', 'curp': 'DIFD030220HGTZRG03', 'rfc': 'DIFD030220GHI', 'fecha_nacimiento': datetime(2003, 2, 20), 'edad': 21, 'telefono': '4771234567', 'ocupacion': 'Estudiante ITI'},
            {'username': 'alu.moreno', 'password': 'Alumno123!', 'first_name': 'Sofía', 'last_name': 'Moreno Vargas', 'email': 'sofia.moreno@alumnos.edu.mx', 'matricula': '20210004', 'curp': 'MOVS021110MGTRNF04', 'rfc': 'MOVS021110JKL', 'fecha_nacimiento': datetime(2002, 11, 10), 'edad': 22, 'telefono': '4772345678', 'ocupacion': 'Estudiante ICC'},
            {'username': 'alu.cruz', 'password': 'Alumno123!', 'first_name': 'Luis', 'last_name': 'Cruz Jiménez', 'email': 'luis.cruz@alumnos.edu.mx', 'matricula': '20210005', 'curp': 'CUJL030725HGTRMS05', 'rfc': 'CUJL030725MNO', 'fecha_nacimiento': datetime(2003, 7, 25), 'edad': 21, 'telefono': '4773456789', 'ocupacion': 'Estudiante LCC'},
            {'username': 'alu.ortiz', 'password': 'Alumno123!', 'first_name': 'Valentina', 'last_name': 'Ortiz Salazar', 'email': 'valentina.ortiz@alumnos.edu.mx', 'matricula': '20210006', 'curp': 'OISV020318MGTRLT06', 'rfc': 'OISV020318PQR', 'fecha_nacimiento': datetime(2002, 3, 18), 'edad': 22, 'telefono': '4774567890', 'ocupacion': 'Estudiante ITI'},
            {'username': 'alu.reyes', 'password': 'Alumno123!', 'first_name': 'Emiliano', 'last_name': 'Reyes Luna', 'email': 'emiliano.reyes@alumnos.edu.mx', 'matricula': '20220007', 'curp': 'RELE040905HGTYLN07', 'rfc': 'RELE040905STU', 'fecha_nacimiento': datetime(2004, 9, 5), 'edad': 20, 'telefono': '4775678901', 'ocupacion': 'Estudiante ICC'},
            {'username': 'alu.flores', 'password': 'Alumno123!', 'first_name': 'Camila', 'last_name': 'Flores Herrera', 'email': 'camila.flores@alumnos.edu.mx', 'matricula': '20220008', 'curp': 'FLHC040127MGTLRM08', 'rfc': 'FLHC040127VWX', 'fecha_nacimiento': datetime(2004, 1, 27), 'edad': 20, 'telefono': '4776789012', 'ocupacion': 'Estudiante LCC'},
            {'username': 'alu.rivera', 'password': 'Alumno123!', 'first_name': 'Sebastián', 'last_name': 'Rivera Núñez', 'email': 'sebastian.rivera@alumnos.edu.mx', 'matricula': '20220009', 'curp': 'RINS030614HGTVXB09', 'rfc': 'RINS030614YZA', 'fecha_nacimiento': datetime(2003, 6, 14), 'edad': 21, 'telefono': '4777890123', 'ocupacion': 'Estudiante ITI'},
            {'username': 'alu.mendez', 'password': 'Alumno123!', 'first_name': 'Isabella', 'last_name': 'Méndez Rojas', 'email': 'isabella.mendez@alumnos.edu.mx', 'matricula': '20220010', 'curp': 'MERI040830MGTNJSA0', 'rfc': 'MERI040830BCD', 'fecha_nacimiento': datetime(2004, 8, 30), 'edad': 20, 'telefono': '4778901234', 'ocupacion': 'Estudiante ICC'},
        ]
        
        for data in alumnos_data:
            user, created = User.objects.get_or_create(username=data['username'], defaults={'first_name': data['first_name'], 'last_name': data['last_name'], 'email': data['email']})
            if created:
                user.set_password(data['password'])
                user.save()
                resultados['alumnos_creados'] += 1
            Alumnos.objects.get_or_create(user=user, defaults={'matricula': data['matricula'], 'curp': data['curp'], 'rfc': data['rfc'], 'fecha_nacimiento': data['fecha_nacimiento'], 'edad': data['edad'], 'telefono': data['telefono'], 'ocupacion': data['ocupacion']})
            Token.objects.get_or_create(user=user)
        
        # EVENTOS
        eventos_data = [
            {'nombre_evento': 'Introduccion a la Inteligencia Artificial', 'tipo_evento': 'Conferencia', 'fecha_realizacion': date(2025, 12, 10), 'hora_inicio': time(10, 0), 'hora_fin': time(12, 0), 'lugar': 'Auditorio Principal', 'publico_objetivo': json.dumps(['Estudiantes', 'Profesores', 'Público general']), 'programa_educativo': 'ICC', 'responsable': maestro_users[0], 'descripcion': 'Conferencia sobre fundamentos de IA', 'cupo_maximo': 150},
            {'nombre_evento': 'Ciberseguridad en la Era Digital', 'tipo_evento': 'Conferencia', 'fecha_realizacion': date(2025, 12, 12), 'hora_inicio': time(16, 0), 'hora_fin': time(18, 0), 'lugar': 'Sala de Conferencias A', 'publico_objetivo': json.dumps(['Estudiantes', 'Profesores']), 'programa_educativo': 'LCC', 'responsable': maestro_users[2], 'descripcion': 'Amenazas actuales en ciberseguridad', 'cupo_maximo': 80},
            {'nombre_evento': 'El Futuro del Desarrollo Web', 'tipo_evento': 'Conferencia', 'fecha_realizacion': date(2025, 12, 15), 'hora_inicio': time(11, 0), 'hora_fin': time(13, 0), 'lugar': 'Auditorio B', 'publico_objetivo': json.dumps(['Estudiantes']), 'programa_educativo': 'ITI', 'responsable': maestro_users[3], 'descripcion': 'Tendencias en frameworks web', 'cupo_maximo': 100},
            {'nombre_evento': 'Taller de Machine Learning con Python', 'tipo_evento': 'Taller', 'fecha_realizacion': date(2025, 12, 11), 'hora_inicio': time(9, 0), 'hora_fin': time(14, 0), 'lugar': 'Laboratorio de Computo 1', 'publico_objetivo': json.dumps(['Estudiantes']), 'programa_educativo': 'ICC', 'responsable': maestro_users[0], 'descripcion': 'Taller practico de ML con Python', 'cupo_maximo': 30},
            {'nombre_evento': 'Desarrollo de APIs con Django REST', 'tipo_evento': 'Taller', 'fecha_realizacion': date(2025, 12, 13), 'hora_inicio': time(10, 0), 'hora_fin': time(15, 0), 'lugar': 'Laboratorio de Computo 2', 'publico_objetivo': json.dumps(['Estudiantes']), 'programa_educativo': 'LCC', 'responsable': maestro_users[3], 'descripcion': 'APIs RESTful con Django', 'cupo_maximo': 25},
            {'nombre_evento': 'Taller de Git y Control de Versiones', 'tipo_evento': 'Taller', 'fecha_realizacion': date(2025, 12, 14), 'hora_inicio': time(9, 0), 'hora_fin': time(12, 0), 'lugar': 'Laboratorio de Computo 3', 'publico_objetivo': json.dumps(['Estudiantes', 'Profesores']), 'programa_educativo': None, 'responsable': maestro_users[1], 'descripcion': 'Git desde basico hasta avanzado', 'cupo_maximo': 35},
            {'nombre_evento': 'Configuracion de Servidores Linux', 'tipo_evento': 'Taller', 'fecha_realizacion': date(2025, 12, 16), 'hora_inicio': time(14, 0), 'hora_fin': time(18, 0), 'lugar': 'Laboratorio de Redes', 'publico_objetivo': json.dumps(['Estudiantes']), 'programa_educativo': 'ITI', 'responsable': maestro_users[4], 'descripcion': 'Configuracion de Ubuntu Server', 'cupo_maximo': 20},
            {'nombre_evento': 'Seminario de Investigacion en IA', 'tipo_evento': 'Seminario', 'fecha_realizacion': date(2025, 12, 17), 'hora_inicio': time(10, 0), 'hora_fin': time(12, 0), 'lugar': 'Sala de Juntas', 'publico_objetivo': json.dumps(['Profesores']), 'programa_educativo': None, 'responsable': maestro_users[0], 'descripcion': 'Avances de investigacion en IA', 'cupo_maximo': 40},
            {'nombre_evento': 'Seminario de Bases de Datos NoSQL', 'tipo_evento': 'Seminario', 'fecha_realizacion': date(2025, 12, 18), 'hora_inicio': time(16, 0), 'hora_fin': time(18, 0), 'lugar': 'Aula Magna', 'publico_objetivo': json.dumps(['Estudiantes', 'Profesores']), 'programa_educativo': 'LCC', 'responsable': maestro_users[1], 'descripcion': 'MongoDB y Redis', 'cupo_maximo': 60},
            {'nombre_evento': 'Tendencias en Cloud Computing', 'tipo_evento': 'Seminario', 'fecha_realizacion': date(2025, 12, 19), 'hora_inicio': time(11, 0), 'hora_fin': time(13, 0), 'lugar': 'Sala de Conferencias B', 'publico_objetivo': json.dumps(['Estudiantes', 'Profesores', 'Público general']), 'programa_educativo': None, 'responsable': maestro_users[4], 'descripcion': 'AWS Azure y Google Cloud', 'cupo_maximo': 70},
            {'nombre_evento': 'Hackathon Universitario 2025', 'tipo_evento': 'Concurso', 'fecha_realizacion': date(2025, 12, 20), 'hora_inicio': time(8, 0), 'hora_fin': time(20, 0), 'lugar': 'Centro de Innovacion', 'publico_objetivo': json.dumps(['Estudiantes']), 'programa_educativo': 'ICC', 'responsable': admin_users[0], 'descripcion': 'Competencia de 12 horas', 'cupo_maximo': 50},
            {'nombre_evento': 'Concurso de Programacion Competitiva', 'tipo_evento': 'Concurso', 'fecha_realizacion': date(2025, 12, 21), 'hora_inicio': time(9, 0), 'hora_fin': time(14, 0), 'lugar': 'Laboratorio de Computo 1', 'publico_objetivo': json.dumps(['Estudiantes']), 'programa_educativo': 'LCC', 'responsable': maestro_users[0], 'descripcion': 'Problemas algoritmicos', 'cupo_maximo': 40},
            {'nombre_evento': 'Rally de Innovacion Tecnologica', 'tipo_evento': 'Concurso', 'fecha_realizacion': date(2025, 12, 22), 'hora_inicio': time(10, 0), 'hora_fin': time(16, 0), 'lugar': 'Explanada Principal', 'publico_objetivo': json.dumps(['Estudiantes', 'Público general']), 'programa_educativo': 'ITI', 'responsable': admin_users[1], 'descripcion': 'Proyectos de innovacion', 'cupo_maximo': 30},
        ]
        
        for data in eventos_data:
            evento, created = EventosAcademicos.objects.get_or_create(nombre_evento=data['nombre_evento'], defaults=data)
            if created:
                resultados['eventos_creados'] += 1
        
        return Response({
            "mensaje": "Base de datos poblada exitosamente",
            "resultados": resultados,
            "credenciales": {
                "admin": "admin.carlos / Admin123!",
                "maestro": "mtro.rodriguez / Maestro123!",
                "alumno": "alu.perez / Alumno123!"
            }
        }, status=status.HTTP_200_OK)
