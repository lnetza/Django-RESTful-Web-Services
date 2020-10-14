from rest_framework import serializers
from toys.models import Toy

#La clase ModelSerializer completa automáticamente un conjunto 
# de campos predeterminados y validadores predeterminados recuperando
#  metadatos de la clase de modelo relacionada que debemos especificar. 
# Además, la clase ModelSerializer proporciona implementaciones 
# predeterminadas para los métodos de creación y actualización. 
# En este caso, aprovecharemos estas implementaciones predeterminadas 
# porque serán adecuadas para proporcionar nuestros métodos de creación y 
# actualización necesarios.
# En resumen ModelSerializer nos ahorra lineas de código cosa que no sucede
# con Serializer

class ToySerializer(serializers.ModelSerializer):
    class Meta:
        #Especificamos el modelo Toy
        model = Toy
        #Se especifican en una Tupla los campos a serializar
        fields = ('id',
                  'name',
                  'description',
                  'toy_category',
                  'was_included_in_home')