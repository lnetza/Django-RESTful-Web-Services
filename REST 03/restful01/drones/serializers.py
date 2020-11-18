from rest_framework import serializers
from drones.models import DroneCategory
from drones.models import Drone
from drones.models import Pilot
from drones.models import Competition
import drones.views
from django.contrib.auth.models import User 

#No queremos usar la clase de serializador DroneSerializer para los drones
#relacionados con un usuario porque queremos serializar menos campos y, por 
#lo tanto, creamos la clase UserDroneSerializer. Esta clase es una subclase
#de la clase HyperlinkedModelSerializer. Este nuevo serializador nos permite 
#serializar los drones relacionados con un Usuario. La clase UserDroneSerializer
#define una clase interna Meta que declara los dos atributos siguientes:

#modelo: Este atributo especifica el modelo relacionado con el serializador, es decir, la clase Drone.

#fields: este atributo especifica una tupla de cadena cuyos valores indican los
#  nombres de campo que queremos incluir en la serialización del modelo relacionado. 
# Solo queremos incluir la URL y el nombre del dron y, por lo tanto, el código incluye 
# 'url' y 'nombre' como miembros de la tupla.

class UserDroneSerializer(serializers.HyperlinkedModelSerializer):     
    class Meta:
        model = Drone        
        fields = (          
            'url', 
            'name')   

#UserSerializer es una subclase de la clase HyperlinkedModelSerializer. 
#Esta nueva clase de serializador declara un atributo de drones como una
#instancia de la clase UserDroneSerializer explicada anteriormente, con
#los argumentos many y read_only iguales a True porque es una relación de
#uno a muchos y es de solo lectura. El código especifica el nombre de los
#drones que especificamos como el valor de cadena para el argumento 
#related_name cuando agregamos el campo propietario como una instancia 
#de model.ForeignKey en el modelo de Drone. De esta manera, el campo de 
#drones nos proporcionará una serie de URL y nombres para cada dron que pertenece al usuario.
class UserSerializer(serializers.HyperlinkedModelSerializer): 
    drones = UserDroneSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = User    
        fields = (  
            'url',
            'pk', 
            'username', 
            'drone')

#La clase DroneCategorySerializer es una subclase de la clase HyperlinkedModelSerializer.
#La clase DroneCategorySerializer declara un atributo de drones que contiene una instancia
# de serializers.HyperlinkedRelatedField con many=true y read_only igual a True.
class DroneCategorySerializer(serializers.HyperlinkedModelSerializer):
    #El código usa el nombre de drones que especificamos como el valor de la cadena related_name 
    # cuando creamos el campo drone_category como una instancia de models.ForeignKey en el modelo de Drone.
    
    #El valor de view_name es 'drone-detail' para indicar la función de la API navegable para usar la vista 
    # de detalles de drone para representar el hipervínculo cuando el usuario hace clic o toca en él. 
    # De esta manera, hacemos posible que la API navegable nos permita navegar entre modelos relacionados.
    drones =serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='drone-detail')
    
    class Meta:
        #modelo: este atributo especifica el modelo relacionado con el serializador, es decir, la clase DroneCategory.
        #Este atributo especifica una tupla de cadena cuyos valores indican los nombres de campo que queremos incluir 
        #en la serialización del modelo relacionado con el serializador, es decir, la clase DroneCategory.
        model = DroneCategory
        #Además, queremos incluir el nombre y el campo que proporciona hipervínculos a cada dron que pertenece a la 
        # categoría de drones. Por lo tanto, el código también especifica 'nombre' y 'drones' como miembros de la tupla.
        fields = (
            'url',
            'pk',
            'name',
            'drones')


class DroneSerializer(serializers.HyperlinkedModelSerializer):
    #Un SlugRelatedField es un campo de lectura y escritura que representa el objetivo de la relación mediante un atributo slug exclusivo, 
    # es decir, la descripción. En el modelo Drone, creamos el campo drone_category como una instancia de models.ForeignKey.
    
    #Queremos mostrar el nombre de la categoría de drones como la descripción (campo slug) para la categoría DroneCategory relacionada y, 
    # por lo tanto, especificamos 'nombre' como el valor para el argumento slug_field.
    drone_category = serializers.SlugRelatedField(queryset=DroneCategory.objects.all(), slug_field='name')

    #Ahora, agregaremos un campo propietario a la clase DroneSerializer existente.
    #Mostrar el nombre de usuario del propietario (solo lectura)

    #La nueva versión de la clase DroneSerializer declara un atributo de propietario como una instancia de serializadores.ReadOnlyField con 
    #el argumento de origen igual a 'owner.username'. De esta manera, el serializador serializará el valor para el campo de nombre de usuario 
    #de la instancia relacionada django.contrib.auth.User almacenada en el campo propietario.
    
    #El código usa la clase ReadOnlyField porque el propietario se completa automáticamente cuando un usuario autenticado crea un nuevo dron.
    #Será imposible cambiar el propietario después de que se haya creado un dron con una llamada al método HTTP POST. De esta manera, el campo 
    #del propietario mostrará el nombre de usuario que creó el dron relacionado. Además, agregamos 'propietario' a la tupla de cadenas de campos
    #dentro de la clase interna Meta.
    #Hicimos los cambios necesarios en el modelo de Drone y su serializador (la clase DroneSerializer) para que los drones tengan propietarios.
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        #Modelo Drone
        model = Drone
        #En este caso, no queremos incluir la PKey y, por lo tanto, la tupla no incluye la cadena 'pk'. El campo drone_category 
        # representará el campo de nombre para la DroneCategory relacionada.
        fields = (
            'url',
            'name', 
            'drone_category',
            'owner',
            'manufacturing_date', 
            'has_it_competed', 
            'inserted_timestamp')

#Esta clase es una subclase de HyperlinkedModelSerializer
#mostrar todas las competencias en las que ha participado un Piloto específico cuando serializamos un Piloto
#Queremos mostrar todos los detalles del Dron relacionado, pero no incluimos el Piloto 
# relacionado porque el Piloto usará este serializador CompetitionSerializer.
class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    #Creamos el campo de drone como una instancia de models.ForeignKey en el modelo Competition y queremos 
    # serializar los mismos datos para el drone que codificamos en la clase DroneSerializer.
    drone = DroneSerializer()
    class Meta:
        model = Competition
        #Como se explicó anteriormente, no incluimos el nombre del campo 'Pilot' en la tupla de campos de la 
        # cadena para evitar serializar el Pilot nuevamente. Usaremos un PilotSerializer como maestro y el
        # CompetitionSerializer como detalle.
        fields = (
            'url',
            'pk',
            'distance_in_feet',
            'distance_achievement_date',
            'drone')

#La clase PilotSerializer es una subclase de la clase HyperlinkedModelSerializer. Usaremos la clase PilotSerializer
#para serializar instancias Pilot y usaremos la clase CompetitionSerializer previamente codificada para serializar 
# todas las instancias Competition relacionadas con Pilot.
#El argumento de muchos se establece en Verdadero porque es una relación de uno a muchos (un piloto tiene muchas 
# instancias de Competición relacionadas). Usamos el nombre de las competiciones que especificamos como el valor de 
# la cadena related_name cuando creamos el campo Pilot como instancia de model.ForeignKey en el modelo Competition.
#De esta manera, el campo de competencias renderizará cada Competencia que pertenece al Piloto usando el CompetitionSerializer 
# previamente declarado.
class PilotSerializer(serializers.HyperlinkedModelSerializer):
    competitions = CompetitionSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(choices=Pilot.GENDER_CHOICES)
    gender_description = serializers.CharField(
        source='get_gender_display',
        read_only=True)

    class Meta:
        model=Pilot
        fields = (
            'url',
            'name',
            'gender',
            'gender_description',
            'races_count',
            'inserted_timestamp',
            'competitions'
        )

#La clase PilotCompetitionSerializer declara un atributo piloto que contiene una instancia de serializers.
# SlugRelatedField con su argumento queryset establecido en Pilot.objects.all () y su argumento slug_field establecido en 'nombre'. 
# Creamos el campo piloto como una instancia de Model.ForeignKey en el modelo Competition y queremos mostrar 
# el nombre del piloto como descripción (campo slug) para el piloto relacionado. Por lo tanto, especificamos 'nombre' como slug_field.
#  Cuando la API navegable tiene que mostrar las posibles opciones para el piloto relacionado en un menú desplegable en un formulario,
#  Django usará la expresión especificada en el argumento del conjunto de consultas para recuperar todos los pilotos posibles y mostrar 
# su campo slug especificado.
#La clase PilotCompetitionSerializer declara un atributo de drone que contiene una instancia de serializers.SlugRelatedField con 
# su argumento queryset establecido en Drone.objects.all () y su argumento slug_field establecido en 'nombre'. Creamos el campo de
#  drones como una instancia de modelo de ForeignKey en el modelo Competition y queremos mostrar el nombre del dron como descripción
#  (campo slug) para el Drone relacionado.
class PilotCompetitionSerializer(serializers.ModelSerializer): 
    
    pilot = serializers.SlugRelatedField(queryset=Pilot.objects.all(), slug_field='name') 
    
    drone = serializers.SlugRelatedField(queryset=Drone.objects.all(), slug_field='name') 
 
    class Meta: 
        model = Competition 
        fields = ( 
            'url', 
            'pk', 
            'distance_in_feet', 
            'distance_achievement_date', 
            'pilot', 
            'drone') 

# Tenemos dos serializadores diferentes para el modelo Competition:
#Resumen de las clases serializadas con sus superclases y modelos 
#Serializer 
#class name	                            Superclass	                          Related model
#DroneCategorySerializer	               HyperlinkedModelSerializer	          DroneCategory
#DroneSerializer	                       HyperlinkedModelSerializer	          Drone
#CompetitionSerializer	                   HyperlinkedModelSerializer	          Competition
#PilotSerializer	                       HyperlinkedModelSerializer	          Pilot
#PilotCompetitionSerializer	               ModelSerializer	                      Competition

    