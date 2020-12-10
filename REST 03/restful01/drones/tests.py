from django.test import TestCase
from django.utils.http import urlencode 
from django.urls import reverse 
from rest_framework import status 
from rest_framework.test import APITestCase 
from drones.models import DroneCategory 
from drones import views

from drones.models import Pilot 
from rest_framework.authtoken.models import Token 
from django.contrib.auth.models import User

#La clase DroneCategoryTests es una subclase de la superclase rest_framework.test.APITestCase 
# y declara el método post_drone_category que recibe el nombre deseado para la nueva categoría de drones como argumento.

#Este método crea la URL y el diccionario de datos para redactar y enviar una solicitud HTTP POST a la vista asociada 
# con el nombre views.DroneCategoryList.name (dronecategory-list) y devuelve la respuesta generada por esta solicitud.

#El código usa el atributo self.client para acceder a la instancia APIClient que nos permite componer y enviar fácilmente 
# solicitudes HTTP para probar nuestro servicio web RESTful que usa el marco REST de Django. Para esta prueba, el código 
# llama al método de publicación con la URL construida, el diccionario de datos(data) y el formato deseado para los datos: 'json'.
class DroneCategoryTests(APITestCase):     
    def post_drone_category(self, name):         
        url = reverse(views.DroneCategoryList.name)         
        data = {'name': name}         
        response = self.client.post(url, data, format='json')         
        return response     

#El método test_post_and_get_drone_category prueba si podemos crear una nueva categoría DroneCategory y luego recuperarla. 
#El método llama al método post_drone_category y luego llama a assert muchas veces para verificar los siguientes resultados esperados:
#1.-El atributo status_code para la respuesta es igual a HTTP 201 Creado (status.HTTP_201_CREATED)
#2.-El número total de objetos DroneCategory recuperados de la base de datos es 1
#3.-El valor del atributo de nombre para el objeto DroneCategory recuperado es igual a la variable new_drone_category_name 
# pasada como parámetro al método post_drone_category
    def test_post_and_get_drone_category(self):         
        """         
        Asegúrese de que podamos crear una nueva categoría de drones y luego recuperarla        
        """         
        new_drone_category_name = 'Hexacopter'         
        response = self.post_drone_category(new_drone_category_name)
        #n para salto de linea
        print("\nPK {0}\n".format(DroneCategory.objects.get().pk))         
        assert response.status_code == status.HTTP_201_CREATED         
        assert DroneCategory.objects.count() == 1         
        assert DroneCategory.objects.get().name == new_drone_category_name
    
#El nuevo método prueba si la RESTRICCION UNICA (Constraint) para el nombre de la categoría de drones funciona como se esperaba y no 
# nos permite crear dos categorías de drones con el mismo nombre. La segunda vez que redactamos y enviamos una solicitud 
# HTTP POST con un nombre de dron duplicado, debemos recibir un código de estado HTTP 400 Bad Request (status.HTTP_400_BAD_REQUEST).
    def test_post_existing_drone_category_name(self):         
        """Asegúrese de que no podamos crear una categoría de drones con un nombre existente"""         
        url = reverse(views.DroneCategoryList.name)         
        new_drone_category_name = 'Duplicated Copter'         
        data = {'name': new_drone_category_name}         
        response1 = self.post_drone_category(new_drone_category_name)         
        assert response1.status_code == status.HTTP_201_CREATED         
        response2 = self.post_drone_category(new_drone_category_name)         
        print(response2)         
        assert response2.status_code == status.HTTP_400_BAD_REQUEST


#El nuevo método prueba si podemos filtrar una categoría de drones por nombre y, por lo tanto, verifica el uso del campo de filtro que hemos 
#configurado para la vista basada en la clase DroneCategoryList. El código crea dos categorías de drones y luego llama a la función 
#django.utils.http.urlencode para construir una URL codificada desde el diccionario filter_by_name. Este diccionario incluye el nombre del 
#campo como clave y la cadena deseada para el campo como valor. En este caso, drone_category_name1 es igual a 'Hexacopter' y, por lo tanto, 
#la URL codificada guardada en la variable url será 'name = Hexacopter'.

#Después de la llamada a self.client.get con la URL construida para recuperar la lista filtrada de categorías de drones, el método verifica 
# los datos incluidos en el cuerpo JSON de la respuesta inspeccionando el atributo de datos para la respuesta. La segunda línea que llama a 
# assert comprueba si el valor de count es igual a 1 y las siguientes líneas verifican si la clave del nombre del primer elemento en la matriz 
# de resultados es igual al valor mantenido en la variable drone_category_name1. El código es fácil de leer y comprender.
    def test_filter_drone_category_by_name(self): 
        """ 
        Se asegura de que podamos filtrar una categoría de drones por nombre
        """ 
        drone_category_name1 = 'Hexacopter' 
        self.post_drone_category(drone_category_name1) 
        drone_category_name2 = 'Octocopter' 
        self.post_drone_category(drone_category_name2) 
        filter_by_name = { 'name' : drone_category_name1 } 
        url = '{0}?{1}'.format( 
            reverse(views.DroneCategoryList.name), 
            urlencode(filter_by_name)) 
        print(url) 
        response = self.client.get(url, format='json') 
        print(response) 
        assert response.status_code == status.HTTP_200_OK 
        # Se asegura de recibir solo un elemento en la respuesta
        assert response.data['count'] == 1 
        assert response.data['results'][0]['name'] == drone_category_name1
    
#El método prueba si podemos recuperar la colección de categorías de drones. Primero, el código crea una nueva categoría 
#de drones y luego realiza una solicitud HTTP GET para recuperar la colección de drones. Las líneas que llaman a assert 
#comprueban que los resultados incluyan el único dron creado y persistente y que su nombre sea igual al nombre utilizado
#para la llamada al método POST para crear la nueva categoría de drones
    def test_get_drone_categories_collection(self): 
        """ 
        Se asegura de que podamos recuperar la colección de categorías de drones
        """ 
        new_drone_category_name = 'Super Copter' 
        self.post_drone_category(new_drone_category_name) 
        url = reverse(views.DroneCategoryList.name) 
        response = self.client.get(url, format='json') 
        assert response.status_code == status.HTTP_200_OK 
        # Make sure we receive only one element in the response 
        assert response.data['count'] == 1 
        assert response.data['results'][0]['name'] == new_drone_category_name
    
#El nuevo método prueba si podemos actualizar un solo campo para una categoría de drones. Primero, el código crea una nueva 
#categoría de drones y luego realiza una solicitud HTTP PATCH para actualizar el campo de nombre para la categoría de drones 
#previamente persistente. Las líneas que llaman a assert comprueban que el código de estado devuelto sea HTTP 200 OK y que 
#el valor de la clave del nombre en el cuerpo de la respuesta sea igual al nuevo nombre que especificamos en la solicitud HTTP PATCH.
    def test_update_drone_category(self): 
        """ 
        Se asegura de que podamos actualizar un solo campo para una categoría de drones
        """ 
        drone_category_name = 'Category Initial Name' 
        response = self.post_drone_category(drone_category_name) 
        url = reverse( 
            views.DroneCategoryDetail.name,  
            None,  
            {response.data['pk']}) 
        updated_drone_category_name = 'Updated Name' 
        data = {'name': updated_drone_category_name} 
        patch_response = self.client.patch(url, data, format='json') 
        assert patch_response.status_code == status.HTTP_200_OK 
        assert patch_response.data['name'] == updated_drone_category_name

#El nuevo método prueba si podemos recuperar una sola categoría con una solicitud HTTP GET. Primero, el código crea una nueva categoría 
#de drones y luego realiza una solicitud HTTP GET para recuperar la categoría de drones previamente persistente. Las líneas que llaman 
#a assert comprueban que el código de estado devuelto sea HTTP 200 OK y que el valor de la clave del nombre en el cuerpo de la respuesta 
#sea igual al nombre que especificamos en la solicitud HTTP POST que creó la categoría de dron.
    def test_get_drone_category(self): 
        """ 
        Ensure we can get a single drone category by id 
        """ 
        drone_category_name = 'Easy to retrieve' 
        response = self.post_drone_category(drone_category_name) 
        url = reverse( 
            views.DroneCategoryDetail.name,  
            None,  
            {response.data['pk']}) 
        get_response = self.client.get(url, format='json') 
        assert get_response.status_code == status.HTTP_200_OK 
        assert get_response.data['name'] == drone_category_name

#Cada método de prueba que requiera una condición específica en la base de datos debe ejecutar todo el código necesario para generar los datos requeridos. 
#Por ejemplo, para actualizar el nombre de una categoría de drones existente, era necesario crear una nueva categoría de drones antes de realizar la 
#solicitud HTTP PATCH para actualizarla. Pytest y el marco REST de Django ejecutarán cada método de prueba sin datos de los métodos de prueba ejecutados 
#previamente en la base de datos, es decir, cada prueba se ejecutará con una base de datos limpia de datos de las pruebas anteriores


#Se ejecutan las pruebas con el comando: pytest
#El comando pytest y el marco Django REST realizarán las siguientes acciones:
#1 Cree un nombre de base de datos de prueba limpio test_drones.
#2 Ejecute todas las migraciones necesarias para la base de datos.
#3 Descubra las pruebas que deben ejecutarse en función de la configuración especificada en el archivo pytest.ini.
#4 Ejecute todos los métodos cuyo nombre comience con el prefijo test_ en la clase DroneCategoryTests y muestre los resultados. Declaramos esta clase en el archivo tests.py 
# y coincide con el patrón especificado para la configuración python_files en el archivo pytest.ini.
#5 Elimine la base de datos de prueba denominada test_drones.

#Comando pytest -v para ver el nombre de las pruebas que pasarón


#La clase PilotTests es una subclase de la superclase rest_framework.test.APITestCase y declara el método post_pilot que 
# recibe el nombre y el género deseados para el nuevo piloto como argumentos.

#Este método crea la URL y el diccionario de datos para componer y enviar una solicitud HTTP POST a la vista asociada con 
#el nombre views.PilotList.name (lista piloto) y devuelve la respuesta generada por esta solicitud.
class PilotTests(APITestCase):        
    #Muchos métodos de prueba llamarán al método post_pilot para crear un nuevo piloto y luego redactarán y enviarán otras solicitudes HTTP al servicio web RESTful. 
    #Tenga en cuenta que el método post_pilot no configura las credenciales de autenticación y, por lo tanto, podremos llamar a este método para usuarios autenticados
    #o no autenticados. Ya sabemos que los usuarios no autenticados no deberían poder publicar un piloto, y una prueba llamará a este método sin un token y 
    #se asegurará de que no quede ningún piloto en la base de datos.
    def post_pilot(self, name, gender, races_count):         
        url = reverse(views.PilotList.name)         
        print(url)         
        data = {
            'name': name,             
            'gender': gender,             
            'races_count': races_count,             
            }         
        response = self.client.post(url, data, format='json')         
        return response      
    
    #1 Crea un usuario de Django con una llamada al método User.objects.create_user.
    #2 Crea un token para el usuario de Django creado previamente con una llamada al método Token.objects.create.
    #3 Incluye el token generado para el usuario de Django como valor para la clave de encabezado HTTP de autorización con la cadena 'Token' como prefijo 
    #del token. La última línea llama al método self.client.credentials para establecer el encabezado HTTP generado como el valor del argumento con 
    #nombre HTTP_AUTHORIZATION. el atributo self.client nos permite acceder a la instancia APIClient.
    
    def create_user_and_set_token_credentials(self):         
        user = User.objects.create_user(
            'user01', 'user01@example.com', 'user01P4ssw0rD')         
        token = Token.objects.create(user=user)         
        self.client.credentials(
            HTTP_AUTHORIZATION='Token {0}'.format(token.key))      
    

    #Siempre que una prueba quiera realizar una solicitud HTTP con un token, el código llamará al método create_user_and_set_token_credentials. 
    #Para limpiar las credenciales configuradas para la instancia APIClient guardada en self.client, es necesario llamar al método self.client.credentials () sin argumentos
    
    #-----------------------------------------------
    #La función se asegura que podemos crear un nuevo piloto con el servicio web RESTful y el requisito de autenticación 
    # apropiado que configuramos, el piloto persiste en la base de datos y el serializador hace su trabajo como se esperaba. 
    # Además, los usuarios no autenticados no pueden acceder a un piloto.

    #Podemos crear un nuevo piloto con una solicitud HTTP POST que tenga un token de autenticación apropiado
    #Podemos recuperar el piloto creado recientemente con una solicitud HTTP GET que tenga un token de autenticación apropiado
    #No podemos recuperar el piloto creado recientemente con una solicitud HTTP GET no autenticada

    #El código llama al método create_user_and_set_token_credentials y luego llama al método post_pilot. 
    # Luego, las llamadas al código se afirman muchas veces para verificar los siguientes resultados esperados:
    def test_post_and_get_pilot(self):
        """
        Se segura de que podamos crear un nuevo piloto y luego recuperarlo
        Se asegura de que no podamos recuperar el piloto persistente sin un token
        """         
        self.create_user_and_set_token_credentials()         
        new_pilot_name = 'Gaston'         
        new_pilot_gender = Pilot.MALE         
        new_pilot_races_count = 5         
        response = self.post_pilot(
            new_pilot_name,             
            new_pilot_gender,             
            new_pilot_races_count)         
        print("nPK {0}n".format(Pilot.objects.get().pk))
        #El atributo status_code para la respuesta es igual a HTTP 201 Creado (status.HTTP_201_CREATED  
        # El valor de los atributos de nombre, sexo y recuento de razas para el objeto Piloto recuperado 
        # es igual a los valores pasados ​​como parámetros al método post_pilot       
        assert response.status_code == status.HTTP_201_CREATED         
        assert Pilot.objects.count() == 1         
        saved_pilot = Pilot.objects.get()         
        assert saved_pilot.name == new_pilot_name         
        assert saved_pilot.gender == new_pilot_gender         
        assert saved_pilot.races_count == new_pilot_races_count         
        url = reverse(
            views.PilotDetail.name,              
            None,             
            {saved_pilot.pk})
        #Luego, el código llama a self.client.get con la URL construida para recuperar el piloto persistente previamente. 
        # Esta solicitud utilizará las mismas credenciales aplicadas a la solicitud HTTP POST y, por lo tanto, la nueva solicitud 
        # se autentica mediante un token válido. El método verifica los datos incluidos en el cuerpo JSON de la respuesta 
        # inspeccionando el atributo de datos de la respuesta. Las llamadas de código se afirman dos veces para comprobar los 
        # siguientes resultados esperados: 
        # 1-El atributo status_code para la respuesta es igual a HTTP 201 Creado (status.HTTP_201_CREATED)
        # 2 El valor de la clave de nombre en el cuerpo de la respuesta es igual al nombre que especificamos en la solicitud HTTP POST        
        authorized_get_response = self.client.get(url, format='json')         
        assert authorized_get_response.status_code == status.HTTP_200_OK         
        assert authorized_get_response.data['name'] == new_pilot_name         
          
        # Luego, el código llama al método self.client.credentials sin argumentos para limpiar las credenciales y vuelve a llamar al
        # método self.client.get con la misma URL construida, esta vez, sin un token. Finalmente, las llamadas de código afirman para 
        # verificar que el atributo status_code para la respuesta sea igual a HTTP 401 No autorizado (status.HTTP_401_UNAUTHORIZED).       
        self.client.credentials()    # Clean up credentials     
        unauthorized_get_response = self.client.get(url, format='json')         
        assert unauthorized_get_response.status_code ==  status.HTTP_401_UNAUTHORIZED
    
    #El nuevo método prueba que la combinación de clases de permiso y autenticación configuradas para la clase PilotList no hace 
    #posible que una solicitud HTTP POST no autenticada cree un piloto. El código llama al método post_pilot sin configurar 
    #ninguna credencial y, por lo tanto, la solicitud se ejecuta sin autenticación. Luego, las llamadas al código afirman 
    #dos veces para verificar los siguientes resultados esperados
    #1-El atributo status_code para la respuesta es igual a HTTP 401 No autorizado (status.HTTP_401_UNAUTHORIZED)
    #2-El número total de objetos Pilot recuperados de la base de datos es 0 porque los datos recibidos para 
    # crear un nuevo piloto no se procesaron
    def test_try_to_post_pilot_without_token(self):         
        """Ensure we cannot create a pilot without a token"""         
        new_pilot_name = 'Unauthorized Pilot'         
        new_pilot_gender = Pilot.MALE         
        new_pilot_races_count = 5         
        response = self.post_pilot(new_pilot_name,new_pilot_gender,new_pilot_races_count)         
        print(response)         
        print(Pilot.objects.count())         
        assert response.status_code == status.HTTP_401_UNAUTHORIZED         
        assert Pilot.objects.count() == 0