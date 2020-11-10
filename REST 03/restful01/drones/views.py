from django.shortcuts import render
from rest_framework import generics 
from rest_framework.response import Response 
from rest_framework.reverse import reverse 
from drones.models import DroneCategory 
from drones.models import Drone 
from drones.models import Pilot 
from drones.models import Competition 
from drones.serializers import DroneCategorySerializer 
from drones.serializers import DroneSerializer 
from drones.serializers import PilotSerializer 
from drones.serializers import PilotCompetitionSerializer 
 
 

#ListCreateAPIView: esta vista de clase implementa el método get que recupera una 
# lista de un conjunto de consultas y el método post que crea una instancia de modelo

#RetrieveUpdateDestroyAPIView: esta vista de clase implementa los métodos de obtención, eliminación, 
# colocación y parche para recuperar, eliminar, actualizar completamente o actualizar parcialmente una instancia de modelo

class DroneCategoryList(generics.ListCreateAPIView): 
    queryset = DroneCategory.objects.all() 
    serializer_class = DroneCategorySerializer 
    name = 'dronecategory-list' 
 
 
class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView): 
    queryset = DroneCategory.objects.all() 
    serializer_class = DroneCategorySerializer 
    name = 'dronecategory-detail' 
 
 
class DroneList(generics.ListCreateAPIView): 
    queryset = Drone.objects.all() 
    serializer_class = DroneSerializer 
    name = 'drone-list' 
 
 
class DroneDetail(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Drone.objects.all() 
    serializer_class = DroneSerializer 
    name = 'drone-detail' 
 
 
class PilotList(generics.ListCreateAPIView): 
    queryset = Pilot.objects.all() 
    serializer_class = PilotSerializer 
    name = 'pilot-list' 
 
 
class PilotDetail(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Pilot.objects.all() 
    serializer_class = PilotSerializer 
    name = 'pilot-detail' 
 
 
class CompetitionList(generics.ListCreateAPIView): 
    queryset = Competition.objects.all() 
    serializer_class = PilotCompetitionSerializer 
    name = 'competition-list' 
 
 
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
