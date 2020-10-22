from rest_framework import serializers
from drones.models import DroneCategory
from drones.models import Drone
from drones.models import Pilot
from drones.models import Competition
import drones.views

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