from django.shortcuts import render
from rest_framework import generics 
from rest_framework.response import Response 
from rest_framework.reverse import reverse 
from drones.models import DroneCategory 
from drones.models import Drone 
from drones.models import Pilot 
from drones.models import Competition 
from drones.serializers import DroneCategorySerializer
#token-based authentication
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authentication import TokenAuthentication 
from rest_framework import permissions 
from drones import custompermission 
from drones.serializers import DroneSerializer 
from drones.serializers import PilotSerializer 
from drones.serializers import PilotCompetitionSerializer 
#Para los filters

from django_filters import FilterSet, AllValuesFilter, DateTimeFilter, NumberFilter 

#ListCreateAPIView: esta vista de clase implementa el método get que recupera una 
# lista de un conjunto de consultas y el método post que crea una instancia de modelo

#RetrieveUpdateDestroyAPIView: esta vista de clase implementa los métodos de obtención, eliminación, 
# colocación y parche para recuperar, eliminar, actualizar completamente o actualizar parcialmente una instancia de modelo

#filter_fields: este atributo especifica una tupla de cadenas cuyos valores indican los nombres de los campos contra los 
#que queremos poder filtrar. Bajo el capó, el marco Django REST creará automáticamente una clase rest_framework.filters.
#FilterSet y la asociará a la vista basada en clases en la que declaramos el atributo. Podremos filtrar por los nombres 
#de campo incluidos en la tupla de cadenas.

#search_fields: este atributo especifica una tupla de cadenas cuyos valores indican los nombres de los campos de tipo de 
#texto que queremos incluir en la función de búsqueda. En todos los usos, querremos realizar una coincidencia de inicio con. 
#Para hacer esto, incluiremos '^' como prefijo del nombre del campo para indicar que queremos restringir el comportamiento
# de búsqueda a una coincidencia que comience con.

#ordering_fields: este atributo especifica una tupla de cadenas cuyos valores indican los nombres de campo que la solicitud HTTP 
#puede especificar para ordenar los resultados. Si la solicitud no especifica un campo para ordenar, la respuesta utilizará los
#campos de ordenación predeterminados especificados en el modelo relacionado con la vista basada en clases.

#Podremos filtrar, buscar y ordenar por el campo de nombre.


class DroneCategoryList(generics.ListCreateAPIView): 
    queryset = DroneCategory.objects.all() 
    serializer_class = DroneCategorySerializer 
    name = 'dronecategory-list'
    filter_fields=(
         'name',
        )
    search_fields=(
        '^name',
        )
    ordering_fields=(
        'name',
        )
 
 
class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView): 
    queryset = DroneCategory.objects.all() 
    serializer_class = DroneCategorySerializer 
    name = 'dronecategory-detail' 
 
 
class DroneList(generics.ListCreateAPIView): 
    queryset = Drone.objects.all() 
    serializer_class = DroneSerializer 
    name = 'drone-list' 
    filter_fields = (         
        'name',          
        'drone_category',          
        'manufacturing_date',          
        'has_it_competed',          
        )     
    search_fields = (         
        '^name',         
        )     
    ordering_fields = (       
        'name',         
        'manufacturing_date',        
        )
    #Establecer políticas de permisos
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custompermission.IsCurrentUserOwnerOrReadOnly,
    )

#Capitulo - Guardar información sobre los usuarios que realizan solicitudes
#La clase generics.ListCreateAPIView hereda de la clase CreateModelMixin 
#y otras clases. La clase DroneList hereda el método perform_create de 
#la clase rest_framework.mixins.CreateModelMixin   
# El código que anula el método perform_create proporciona un campo 
# propietario adicional al método create estableciendo un valor para 
# el argumento propietario en la llamada al método serializer.save.
# El código establece el argumento propietario en el valor de 
# self.request.user, es decir, en el usuario autenticado que realiza la solicitud.
# De esta manera, siempre que se cree y persista un nuevo Drone, 
# guardará al Usuario asociado a la solicitud como su propietario.     
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DroneDetail(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Drone.objects.all() 
    serializer_class = DroneSerializer 
    name = 'drone-detail'
    #Establecer políticas de permisos
    permission_classes =(
        permissions.IsAuthenticatedOrReadOnly,
        custompermission.IsCurrentUserOwnerOrReadOnly,
    ) 
 
 
class PilotList(generics.ListCreateAPIView): 
    queryset = Pilot.objects.all() 
    serializer_class = PilotSerializer 
    name = 'pilot-list'
    filter_fields = (         
        'name',          
        'gender',         
        'races_count',         
        )     
    search_fields = (         
        '^name',         
        )     
    ordering_fields = (         
        'name',         
        'races_count'        
        )
    #Token Autenticated 
    # We will configure authentication and permission policies for the 
    # class-based views that work with the Pilot model. We will override
    # the values for the authentication_classes and permission_classes
    # class attributes for the PilotDetail and PilotList classes.   
    authentication_classes = (  
        TokenAuthentication,  
        )  
    permission_classes = (   
        IsAuthenticated,   
        )
 
 
class PilotDetail(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Pilot.objects.all() 
    serializer_class = PilotSerializer 
    name = 'pilot-detail' 
    #Token Authenticated
    authentication_classes = (       
        TokenAuthentication,  
        )    
    permission_classes = (    
        IsAuthenticated, 
        )
 
#from_achievement_date: este atributo es una instancia de django_filters.DateTimeFilter 
#que permite que la solicitud filtre las competiciones cuyo valor de DateTime de logro_date
#es mayor o igual que el valor de DateTime especificado. El valor especificado en el argumento 
#de nombre indica el campo al que se aplica el filtro de fecha y hora, 'distancia_actualización_fecha',
#y el valor del argumento lookup_expr indica la expresión de búsqueda, 'gte', que significa mayor o igual que.

#to_achievement_date: este atributo es una instancia de django_filters.DateTimeFilter que permite que la solicitud 
#filtre las competiciones cuyo valor de fecha y hora de logro es menor o igual que el valor de DateTime especificado. 
#El valor especificado en el argumento de nombre indica el campo al que se aplica el filtro de fecha y hora, 
#'distancia_actualización_fecha', y el valor del argumento lookup_expr indica la expresión de búsqueda, 'lte',lo que significa menor o igual a.

#drone_name: este atributo es una instancia de django_filters.AllValuesFilter que permite que la solicitud filtre las 
#competiciones cuyos nombres de drones coinciden con el valor de cadena especificado. El valor del argumento de nombre 
#indica el campo al que se aplica el filtro, 'drone__name'. Tenga en cuenta que hay un guión bajo doble (__) entre el 
#dron y el nombre, y puede leerlo como el campo de nombre del modelo del dron o simplemente reemplazar el guión bajo 
#doble con un punto y leer drone.name. El nombre usa la sintaxis de subrayado doble de Django. Sin embargo, no queremos 
#que la solicitud use drone__name para especificar el filtro para el nombre del dron. Por lo tanto, la instancia se almacena 
#en el atributo de clase llamado drone_name, con solo un guión bajo entre el jugador y el nombre, para que sea más fácil
#de usar. Haremos configuraciones para que la API navegable muestre un menú desplegable con todos los valores posibles para
#que el nombre del dron lo use como filtro. El menú desplegable solo incluirá los nombres de los drones que hayan registrado competencias.
#que significa menor o igual a.

#pilot_name: este atributo es una instancia de django_filters.AllValuesFilter que permite que la solicitud filtre las competiciones cuyos 
#nombres de pilotos coinciden con el valor de cadena especificado. El valor del argumento de nombre indica el campo al que se aplica el filtro,
#'pilot__name'. El nombre usa la sintaxis de subrayado doble de Django. Como sucedió con drone_name, no queremos que la solicitud use pilot__name 
#para especificar el filtro para el nombre del piloto y, por lo tanto, almacenamos la instancia en el atributo de clase llamado pilot_name, con
#solo un guión bajo entre el piloto y el nombre. La API navegable mostrará un menú desplegable con todos los valores posibles para que el nombre 
#del piloto lo utilice como filtro. El menú desplegable solo incluirá los nombres de los pilotos que se hayan inscrito en competencias porque 
#usamos la clase AllValuesFilter.
class CompetitionFilter(FilterSet):
    from_achievement_date = DateTimeFilter(
        field_name='distance_achievement_date', lookup_expr='gte')     
    to_achievement_date = DateTimeFilter(         
        field_name='distance_achievement_date', lookup_expr='lte')     
    min_distance_in_feet = NumberFilter(         
        field_name='distance_in_feet', lookup_expr='gte')     
    max_distance_in_feet = NumberFilter(         
        field_name='distance_in_feet', lookup_expr='lte')    
    drone_name = AllValuesFilter(         
        field_name='drone__name')     
    pilot_name = AllValuesFilter(         
        field_name='pilot__name')    
#La clase CompetitionFilter define una clase interna Meta que declara los dos atributos siguientes:
    class Meta:
        #Este atributo especifica el modelo relacionado con el conjunto de filtros, es decir, la clase Competición
        model = Competition 
        #fields Este atributo especifica una tupla de cadenas cuyos valores indican los nombres de campo y 
        #los nombres de filtro que queremos incluir en los filtros para el modelo relacionado. 
        #Incluimos 'distance_in_feet' y los nombres de todos los filtros explicados anteriormente.
        #La cadena 'distance_in_feet' se refiere al campo con este nombre. Queremos aplicar el 
        #filtro numérico predeterminado que se construirá bajo el capó para permitir que la 
        #solicitud se filtre por una coincidencia exacta en el campo distance_in_feet. 
        #De esta manera, la solicitud tendrá muchas opciones para filtrar las competiciones.        
        fields = (             
            'distance_in_feet',             
            'from_achievement_date',             
            'to_achievement_date',             
            'min_distance_in_feet',            
            'max_distance_in_feet',       
            # drone__name will be accessed as drone_name   
            'drone_name',      
            # pilot__name will be accessed as pilot_name   
            'pilot_name',     
        ) 

class CompetitionList(generics.ListCreateAPIView): 
    queryset = Competition.objects.all() 
    serializer_class = PilotCompetitionSerializer 
    name = 'competition-list' 
    #El atributo filter_class especifica CompetitionFilter 
    #como su valor, es decir, la subclase FilterSet que declara
    #los filtros personalizados que queremos usar para esta vista
    #basada en clases. En este caso, el código no especificó una
    #tupla de cadenas para el atributo filter_class porque hemos
    #definido nuestra propia subclase FilterSet.
    filter_class = CompetitionFilter 
    #La tupla de cadenas ordering_fields especifica los dos nombres de
    #campo que la solicitud podrá utilizar para ordenar las competiciones.  
    ordering_fields = (         
        'distance_in_feet',         
        'distance_achievement_date',        
        ) 
 
class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Competition.objects.all() 
    serializer_class = PilotCompetitionSerializer 
    name = 'competition-detail' 

#ApiRoot como una subclase de la clase generics.GenericAPIView.
#La clase ApiRoot define el método get que devuelve un objeto Response con pares de cadenas clave / valor 
# que proporcionan un nombre descriptivo para la vista y su URL, generado con la función rest_framework.reverse.reverse. 
# Esta función de resolución de URL devuelve una URL totalmente calificada para la vista.
class ApiRoot(generics.GenericAPIView): 
    name = 'api-drone' 
    def get(self, request, *args, **kwargs): 
        return Response({ 
            'drone-categories': reverse(DroneCategoryList.name, request=request), 
            'drones': reverse(DroneList.name, request=request), 
            'pilots': reverse(PilotList.name, request=request), 
            'competitions': reverse(CompetitionList.name, request=request) 
            })
# La siguiente tabla resume los verbos HTTP que cada vista basada en clases va a procesar y el alcance al que se aplica.

#Scope	                                                         Nombre de la clase basada en vistas	    Verbos HTTP que procesará
#Colección de categorías de drones:: /drone-categories/	            DroneCategoryList	                      GET, POST, and OPTIONS
#Categoría de drones: /drone-category/{id}	                        DroneCategoryDetail	                      GET, PUT, PATCH, DELETE, and OPTIONS
#Colección de drones: /drones/	                                    DroneList	                              GET, POST, and OPTIONS
#Drone: /drone/{id}	                                                DroneDetail	                              GET, PUT, PATCH, DELETE, and OPTIONS
#Colección de pilotos: /pilots/	                                    PilotList	                              GET, POST and OPTIONS
#Pilot: /Pilot/{id}	                                                PilotDetail	                              GET, PUT, PATCH, DELETE and OPTIONS
#Colección de concursos: /competitions/	                            CompetitionList	                          GET, POST and OPTIONS
#Score: /competition/{id}	                                        CompetitionDetail	                      GET, PUT, PATCH, DELETE and OPTIONS





