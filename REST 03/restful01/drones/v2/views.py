from rest_framework import generics 
from rest_framework.response import Response 
from rest_framework.reverse import reverse 
from drones import views   

#La clase ApiRootVersion2 es una subclase de la clase rest_framework.generics.GenericAPIView y 
#declara el método get. Trabajar con relaciones avanzadas y 
#serialización, la clase GenericAPIView es la clase base para todas las vistas genéricas con 
#las que hemos estado trabajando. Haremos que el marco Django REST use esta clase en lugar de
#la clase ApiRoot cuando las solicitudes funcionen con la versión 2

#La clase ApiRootVersion2 define el método get que devuelve un objeto Response con pares de 
#cadenas clave / valor que proporcionan un nombre descriptivo para la vista y su URL, generado
#con la función rest_framework.reverse.reverse. Esta función de resolución de URL devuelve una 
#URL totalmente calificada para la vista. Siempre que llamamos a la función inversa, incluimos 
#el valor de solicitud para el argumento de solicitud. Es muy importante hacer esto para asegurarse
#de que la clase NameSpaceVersioning pueda funcionar como se espera para configurar el esquema de control de versiones.

#En este caso, la respuesta define claves llamadas 'categorías de vehículos' y 'vehículos' en lugar de las claves 
#drone-cagories' y 'drones' que se incluyen en el archivo views.py, en la clase ApiRoot que se utilizará para versión 1.
class ApiRootVersion2(generics.GenericAPIView):     
    name = 'api-root'     
    def get(self, request, *args, **kwargs):         
        return Response({             
            'vehicle-categories': reverse(views.DroneCategoryList.name, request=request),             
            'vehicles': reverse(views.DroneList.name, request=request),             
            'pilots': reverse(views.PilotList.name, request=request),             
            'competitions': reverse(views.CompetitionList.name, request=request)             
            }) 