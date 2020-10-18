from django.shortcuts import render
from rest_framework import status
from toys.models import Toy
from toys.serializers import ToySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

#El decorador @api_view nos permite especificar cuáles son los verbos HTTP que puede procesar 
# la función a la que se aplica. Si la solicitud que se ha enrutado a la función de vista tiene 
# un verbo HTTP que no está incluido en la lista de cadenas especificada como el argumento 
# http_method_names (ejemplo: http PATCH :8000/toys/) para el decorador @api_view, 
# el comportamiento predeterminado devuelve una respuesta con un código de estado HTTP 405 Método no permitido
# al usar @api_view ya traé configurado lo sigiente
#('rest_framework.parsers.JSONParser', 'rest_framework.parsers.FormParser', 'rest_framework.parsers.MultiPartParser') y viene
#especificado en DEFAULT_PARSER_CLASSES
#Cuando usamos el decorador @api_view, el servicio web RESTful podrá manejar cualquiera de los siguientes 
# tipos de contenido a través de los analizadores apropiados es decir:
#application/json: es parseado por rest_framework.parsers.JSONParser class
#application/x-www-form-urlencoded:es parseado por rest_framework.parsers.FormParser class
#multipart/form-data: es parseado por rest_framework.parsers.MultiPartParser class


@api_view(['GET','POST'])
def toy_list(request):
    if request.method == 'GET':
        #si get Serialización
        toys = Toy.objects.all()
        toys_serializer = ToySerializer(toys, many=True)
        return Response(toys_serializer.data)
    
    elif request.method == 'POST':
        #Se crea una instancia del serializador que recibe como parametro el request HTTP de tipo POST
        toy_serializer = ToySerializer(data=request.data)
        
        if toy_serializer.is_valid():
            #Se guarda en la BDD
            toy_serializer.save()
            #Retorna Response con los datos guardados y 201 status
            return Response(toy_serializer.data,
                status=status.HTTP_201_CREATED)
        return Response(toy_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#Función para recuperar, actualizar o eliminar un juguete
@api_view(['GET','PUT','DELETE'])
def toy_detail(request,pk):
    try:
        #Obtenemos el juguete con la pk igual al parametro pk
        toy = Toy.objects.get(pk=pk)
    except Toy.DoesNotExist:
        #Si no exite, retorna 404
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        #Se serializa el juguete buscado y devuelve un JSONResponse con el status 200 HTTP
        toy_serializer = ToySerializer(toy)
        return Response(toy_serializer.data)
    
    elif request.method == 'PUT':
        # la siguiente línea única que pasa toy como primer argumento y request.data como argumento de datos para crear
        #  una nueva instancia de ToySerializer:
        toy_serializer = ToySerializer(toy, data=request.data)
        #Se valida si la instancia de toy es valida con .is_valid()
        if toy_serializer.is_valid():
            toy_serializer.save()
            #Retorna los datos serializados
            return Response(toy_serializer.data)
        #Si los datos analizados en la request no generan una instancia valida de Toy, retorna 400
        return Response(toy_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        #Si el método es delete, se recupera la instancia de TOY y se elimina
        toy.delete()
        #una vez elimininado se devuelve 204 es decir sin contenido
        return Response(status=status.HTTP_204_NO_CONTENT)