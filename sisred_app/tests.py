from django.test import TestCase

from .models import Perfil, Recurso, Metadata

from sisred_app.views.views_equipo4 import createNotification
from .models import User, Perfil, RED, Fase, ProyectoConectate, Recurso, NotificacionTipo, Rol, RolAsignado, \
    Notificacion
from django.contrib.auth.models import User
import json


# Create your tests here.

class BuscarRecursoTestCase(TestCase):

    def test_buscar_recurso_byName_status(self):

class sisRedTestCase(TestCase):

    def test_login(self):
        username = "gl.pinto10@uniandes.edu.co"
        first_name = "first_name"
        last_name = "last_name"
        password = "Test12345"
        id_conectate = "1"
        numero_identificacion = "123455"
        user_model = User.objects.create_user(username=username, password=password, first_name=first_name,
                                              last_name=last_name, email=username)
        user_profile = Perfil.objects.create(usuario=user_model, id_conectate=id_conectate,
                                             numero_identificacion=numero_identificacion, estado=1)
        user_profile.save()
        response = self.client.post('/api/login/', json.dumps({"username": username, "password": password}),
                                    content_type='application/json')
        current_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(current_data['token'])
        self.assertEqual(id_conectate, current_data['idConectate'])
        self.assertEqual(first_name, current_data['firstName'])
        self.assertEqual(last_name, current_data['lastName'])
        self.assertEqual(numero_identificacion,
                         current_data['numeroIdentificacion'])

    def test_cambiar_fase(self):
        print("test_cambiar_fase")
        proyecto_conectate = ProyectoConectate.objects.create(id_conectate='2', nombre='namepy',
                                                              nombre_corto='nameShort',
                                                              codigo='code', fecha_inicio='1999-12-19',
                                                              fecha_fin='2001-12-20')
        fase = Fase.objects.create(
            id_conectate='2',
            nombre_fase='produccion',
        )
        red = RED.objects.create(
            id_conectate='1',
            nombre='nombre',
            nombre_corto='nombre_corto',
            descripcion='descripcion',
            fecha_inicio=None,
            fecha_cierre=None,
            porcentaje_avance=50,
            tipo='tipo',
            solicitante='solicitante',
            proyecto_conectate=proyecto_conectate,
            horas_estimadas=8,
            horas_trabajadas=7,
            fase=fase,
        )
        fase2 = Fase.objects.create(
            id_conectate='3',
            nombre_fase='preproduccion',
        )
        response = self.client.put(
            '/api/red/' + str(red.id_conectate)
            + '/cambiarfase/' + str(fase2.id_conectate) + '/',
            content_type='application/json')

        print("response", response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_list_fases(self):
        url = '/api/fases/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_add_metadata_recurso_status(self):

        user = User.objects.create(username='user1', password='1234ABC', first_name='nombre1',
                                   last_name='apellido1', email='user@uniandes.edu.co')
        perfil = Perfil.objects.create(id_conectate='1', usuario=user, tipo_identificacion='CC',
                                       numero_identificacion='1234', estado=1)

        recurso = Recurso.objects.create(nombre='Recurso5', archivo='archivo1', thumbnail='thumbnail1',
                                         fecha_creacion='2019-04-25',
                                         fecha_ultima_modificacion='2019-04-25', tipo='jpg',
                                         descripcion='descripcion1', autor=perfil, usuario_ultima_modificacion=perfil)

        buscarNombre = "Recurso5"

        recurso = Recurso.objects.create(nombre='Recurso1', archivo='archivo1', thumbnail='thumbnail1',
                                         fecha_creacion='2019-04-11',
                                         fecha_ultima_modificacion='2019-04-11', tipo='jpg',
                                         descripcion='descripcion1', autor=perfil, usuario_ultima_modificacion=perfil)


        url = f'/api/buscarRecurso/?name={buscarNombre}'

        response =  self.client.get(url, format='json')

        self.assertEqual(response.status_code, 200)



    def test_buscar_recurso_byFechaCreacion(self):

    def test_add_metadata_existente_recurso(self):

        user = User.objects.create(username='user1', password='1234ABC', first_name='nombre1',
                                   last_name='apellido1', email='user@uniandes.edu.co')
        perfil = Perfil.objects.create(id_conectate='1', usuario=user, tipo_identificacion='CC',
                                       numero_identificacion='1234', estado=1)
        Recurso.objects.create(nombre='Recurso1', archivo='archivo1', thumbnail='thumbnail1',
                                         fecha_creacion='2019-01-25',
                                         fecha_ultima_modificacion='2019-01-25', tipo='jpg',
                                         descripcion='descripcion1', autor=perfil, usuario_ultima_modificacion=perfil)
        Recurso.objects.create(nombre='Recurso2', archivo='archivo2', thumbnail='thumbnail1',
                                         fecha_creacion='2019-02-25',
                                         fecha_ultima_modificacion='2019-02-25', tipo='jpg',
                                         descripcion='descripcion2', autor=perfil, usuario_ultima_modificacion=perfil)
        Recurso.objects.create(nombre='Recurso3', archivo='archivo3', thumbnail='thumbnail1',
                                          fecha_creacion='2019-03-25',
                                          fecha_ultima_modificacion='2019-03-25', tipo='jpg',
                                          descripcion='descripcion3', autor=perfil, usuario_ultima_modificacion=perfil)

        buscarNombre = ""
        fecha_desde = "2019-01-01"
        fecha_hasta = "2019-02-28"

        url = f'/api/buscarRecurso/?name={buscarNombre}&fdesde={fecha_desde}&fhasta={fecha_hasta}'

        response = self.client.get(url, format='json')
        recursos = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(recursos), 2)

    def test_buscar_recurso_byTag(self):
        user = User.objects.create(username='user1', password='1234ABC', first_name='nombre1',
                                   last_name='apellido1', email='user@uniandes.edu.co')
        perfil = Perfil.objects.create(id_conectate='1', usuario=user, tipo_identificacion='CC',
                                       numero_identificacion='1234', estado=1)
        recurso1 = Recurso.objects.create(nombre='Recurso1', archivo='archivo1', thumbnail='thumbnail1',
                                          fecha_creacion='2019-01-25',
                                          fecha_ultima_modificacion='2019-01-25', tipo='jpg',
                                          descripcion='descripcion1', autor=perfil, usuario_ultima_modificacion=perfil)
        Recurso.objects.create(nombre='Recurso2', archivo='archivo2', thumbnail='thumbnail1',
                               fecha_creacion='2019-02-25',
                               fecha_ultima_modificacion='2019-02-25', tipo='jpg',
                               descripcion='descripcion2', autor=perfil, usuario_ultima_modificacion=perfil)
        Recurso.objects.create(nombre='Recurso3', archivo='archivo3', thumbnail='thumbnail1',
                               fecha_creacion='2019-03-25',
                               fecha_ultima_modificacion='2019-03-25', tipo='jpg',
                               descripcion='descripcion3', autor=perfil, usuario_ultima_modificacion=perfil)

        tag = Metadata.objects.create(id=1, tag="tag1")
        recurso1.metadata.add(tag)

        metadata = "tag1"

        url = f'/api/buscarRecurso/?text={metadata}'

        response = self.client.get(url, format='json')
        recursos = json.loads(response.content)


        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(recursos), 1)

        self.assertEqual((recursoFiltrado.metadata).count(), 1)

    def test_list_notificaciones_un_usuario(self):
        user = User.objects.create(username='user1', password='1234ABC', first_name='nombre1',
                                   last_name='apellido1', email='user@uniandes.edu.co')
        perfil = Perfil.objects.create(id_conectate=1, usuario=user, numero_identificacion='123',
                                       tipo_identificacion='CC', estado='1')
        proyecto_conectate = ProyectoConectate.objects.create(id_conectate='2', nombre='namepy',
                                                              nombre_corto='nameShort',
                                                              codigo='code', fecha_inicio='1999-12-19',
                                                              fecha_fin='2001-12-20')
        fase = Fase.objects.create(
            id_conectate='2',
            nombre_fase='produccion',
        )

        red = RED.objects.create(
            id_conectate='1',
            nombre='nombre',
            nombre_corto='nombre_corto',
            descripcion='descripcion',
            fecha_inicio=None,
            fecha_cierre=None,
            porcentaje_avance=50,
            tipo='tipo',
            solicitante='solicitante',
            proyecto_conectate=proyecto_conectate,
            horas_estimadas=8,
            horas_trabajadas=7,
            fase=fase,
        )
        rol = Rol.objects.create(id_conectate=1, nombre='Productor')
        tipoNotificacion = NotificacionTipo.objects.create(
            nombre='ASIGNAR_RED', descripcion='El red fue asignado.')
        notificacion = Notificacion.objects.create(mensaje='prueba', fecha='2019-01-26', visto=False,
                                                   tipo_notificacion=tipoNotificacion)

        rolAsignado = RolAsignado.objects.create(
            id_conectate=1, estado=1, red=red, rol=rol, usuario=perfil)
        rolAsignado.notificaciones.add(notificacion)
        url = '/api/notificaciones/' + str(perfil.id_conectate) + '/'

        response = self.client.get(url, format='json')
        current_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(current_data), 1)

    def test_numero_notificaciones_no_vistas(self):
        user = User.objects.create(username='user1', password='1234ABC', first_name='nombre1',
                                   last_name='apellido1', email='user@uniandes.edu.co')
        perfil = Perfil.objects.create(
            id_conectate=1, usuario=user, numero_identificacion='123', tipo_identificacion='CC', estado='1')
        proyecto_conectate = ProyectoConectate.objects.create(id_conectate='2', nombre='namepy',
                                                              nombre_corto='nameShort',
                                                              codigo='code', fecha_inicio='1999-12-19',
                                                              fecha_fin='2001-12-20')
        fase = Fase.objects.create(
            id_conectate='2',
            nombre_fase='produccion',
        )

        red = RED.objects.create(
            id_conectate='1',
            nombre='nombre',
            nombre_corto='nombre_corto',
            descripcion='descripcion',
            fecha_inicio=None,
            fecha_cierre=None,
            porcentaje_avance=50,
            tipo='tipo',
            solicitante='solicitante',
            proyecto_conectate=proyecto_conectate,
            horas_estimadas=8,
            horas_trabajadas=7,
            fase=fase,
        )
        rol = Rol.objects.create(id_conectate=1, nombre='Productor')
        tipoNotificacion = NotificacionTipo.objects.create(
            nombre='ASIGNAR_RED', descripcion='El red fue asignado.')
        notificacion = Notificacion.objects.create(
            mensaje='prueba', fecha='2019-01-26', visto=False, tipo_notificacion=tipoNotificacion)
        notificacion2 = Notificacion.objects.create(
            mensaje='prueba2', fecha='2019-01-26', visto=True, tipo_notificacion=tipoNotificacion)

        rolAsignado = RolAsignado.objects.create(
            id_conectate=1, estado=1, red=red, rol=rol, usuario=perfil)
        rolAsignado.notificaciones.add(notificacion)
        rolAsignado.notificaciones.add(notificacion2)
        url = '/api/notificaciones/' + str(perfil.id_conectate) + '/novistos/'

        response = self.client.get(url, format='json')
        current_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(current_data, 1)

    def test_updateNotificaction(self):
        tipoNotificacion = NotificacionTipo.objects.create(
            nombre='nombre', descripcion='descripcion')
        notificationTest = Notificacion.objects.create(mensaje='texto', visto=False,
                                                       tipo_notificacion=tipoNotificacion)

        response = self.client.put('/api/putNotification/' + str(notificationTest.id) + '/',
                                   content_type='application/json')

        print("response.content", response.content)
        dataRsp = json.loads(response.content)
        print("dataRsp", dataRsp)

        self.assertEqual(
            dataRsp, {"mensaje": 'La notificacion ha sido actualizada'})

    def test_createNotification(self):
        print("test_createNotification")
        proyecto_conectate = ProyectoConectate.objects.create(id_conectate='1', nombre='name',
                                                              nombre_corto='nameShort',
                                                              codigo='123456', fecha_inicio='2020-09-01',
                                                              fecha_fin='2020-09-01')
        fase = Fase.objects.create(
            id_conectate='2',
            nombre_fase='produccion',
        )
        red = RED.objects.create(
            id_conectate='1',
            nombre='nombre',
            nombre_corto='nombre_corto',
            descripcion='descripcion',
            fecha_inicio='2020-09-01',
            fecha_cierre='2020-09-01',
            fecha_creacion='2019-09-01',
            porcentaje_avance=22,
            tipo='tipo',
            solicitante='solicitante',
            proyecto_conectate=proyecto_conectate,
            horas_estimadas=23,
            horas_trabajadas=11,
            fase=fase,
        )
        rol = Rol.objects.create(id_conectate='1', nombre='nombreROL')
        user_model = User.objects.create_user(
            username='username', password='password')
        user_model.first_name = 'first_name'
        user_model.last_name = 'last_name'
        user_model.email = 'email'
        user_profile = Perfil.objects.create(usuario=user_model, id_conectate='1', numero_identificacion='1022',
                                             estado=1)
        rol_asignado = RolAsignado.objects.create(id_conectate='1', estado=1, red=red, rol=rol,
                                                  usuario=user_profile)
        notificacionTipo = NotificacionTipo.objects.create(
            nombre='nombre', descripcion='descripcion')

        self.assertEqual(createNotification(red.id_conectate, notificacionTipo.pk),
                         {"mensaje": 'La notificacion ha sido creada'})
