from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from toys.models import Toy
from toys.serializers import ToySerializer
#La clase JSONResponse es una subclase de la clase django.http.HttpResponse. 
# La superclase django.http.HttpResponse representa una respuesta HTTP con contenido de cadena.
#La clase simplemente declara el método __init__ que crea una instancia rest_framework.renderers.JSONRenderer
#  y llama a su método render para representar los datos recibidos en JSON y guardar la cadena de bytes devuelta
#  en la variable local de contenido.
#Luego, el código agrega la clave 'content_type' al encabezado de respuesta con 'application / json' como su valor. 
# Finalmente, el código llama al inicializador para la clase base con la cadena de bytes JSON y el par clave-valor agregado al encabezado.
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type']='application/json'
        super(JSONResponse, self).__init__(content,**kwargs)

#garantizar que la vista establezca una cookie CSRF (abreviatura de Cross-Site Request Forgery).
#many true= De esta forma, Django es capaz de serializar una lista de objetos
@csrf_exempt
def toy_list(request):
    if request.method == 'GET':
        #si get Serialización
        toys = Toy.objects.all()
        toys_serializer = ToySerializer(toys, many=True)
        return JSONResponse(toys_serializer.data)
    
    elif request.method == 'POST':
        #Si POST Deserealizacion de request
        toy_data = JSONParser().parse(request)
        toy_serializer = ToySerializer(data=toy_data)
        
        if toy_serializer.is_valid():
            #Se guarda en la BDD
            toy_serializer.save()
            #Retorna JSONResponse con los datos guardados y 201 status
            return JSONResponse(toy_serializer.data,
                status=status.HTTP_201_CREATED)
        return JSONResponse(toy_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#Función para recuperar, actualizar o eliminar un juguete
@csrf_exempt
def toy_detail(request,pk):
    try:
        #Obtenemos el juguete con la pk igual al parametro pk
        toy = Toy.objects.get(pk=pk)
    except Toy.DoesNotExist:
        #Si no exite, retorna 404
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        #Se serializa el juguete buscado y devuelve un JSONResponse con el status 200 HTTP
        toy_serializer = ToySerializer(toy)
        return JSONResponse(toy_serializer.data)
    
    elif request.method == 'PUT':
        #Si el verbo en el request es PUT, se deserealiza el JSON contenida en el request con JSONParser y el analizador .parse(request) 
        toy_data = JSONParser().parse(request)
        #Se crea una instancia del serializador con parametros Toy y data=al JSON contenida en el request, 
        # que reemplazara la info del juguete especificado con pk
        toy_serializer = ToySerializer(toy, data=toy_data)
        #Se valida si la instancia de toy es valida con .is_valid()
        if toy_serializer.is_valid():
            toy_serializer.save()
            return JSONResponse(toy_serializer.data)
        return JSONResponse(toy_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        toy.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)