from rest_framework import permissions   


#Las líneas declaran la clase IsCurrentUserOwnerOrReadOnly y anulan 
#el método has_object_permission definido en la superclase BasePermission que
#devuelve un valor bool que indica si el permiso debe otorgarse o no.

#La tupla permissions.SAFE_METHODS de cadena incluye los tres métodos HTTP 
# o verbos que se consideran seguros porque son de solo lectura y no producen
# cambios en el recurso o colección de recursos relacionados: 'GET', 'HEAD' y 'OPTIONS '. 
# El código del método has_object_permission comprueba si el verbo HTTP especificado en 
# el atributo request.method es alguno de los tres métodos seguros especificados en 
# allow.SAFE_METHODS. Si esta expresión se evalúa como True, el método has_object_permission 
# devuelve True y otorga permiso a la solicitud.

#Si el verbo HTTP especificado en el atributo request.method no es ninguno 
# de los tres métodos seguros, el código devuelve True y concede permiso 
# solo cuando el atributo propietario del objeto obj recibido (obj.owner) 
# coincide con el usuario que originó la solicitud ( request.user). 
# El usuario que originó la solicitud siempre será el usuario autenticado.
# De esta forma, solo el propietario del recurso relacionado tendrá permiso 
# para aquellas solicitudes que incluyan verbos HTTP que no sean seguros.

#Usaremos la nueva clase de permiso personalizado IsCurrentUserOwnerOrReadOnly
#  para asegurarnos de que solo los propietarios de drones puedan realizar 
# cambios en un dron existente. Combinaremos esta clase de permiso con 
# rest_framework.permissions.IsAuthenticatedOrReadOnly uno que solo permite
#  el acceso de solo lectura a los recursos cuando la solicitud no pertenece 
# a un usuario autenticado. De esta forma, siempre que un usuario anónimo realice 
# una solicitud, solo tendrá acceso de solo lectura a los recursos.
#La tupla de cadena permissions.SAFE_METHODS incluye los siguientes métodos 
# HTTP o verbos que se consideran seguros:'GET', 'HEAD' y 'OPTIONS'

class IsCurrentUserOwnerOrReadOnly(permissions.BasePermission):     
    def has_object_permission(self, request, view, obj): 
        if request.method in permissions.SAFE_METHODS:  
           # The method is a safe method   
           # Message "detail": "You do not have permission to perform this action."   
           return True        
        else:           
            # El método no es un método seguro   
            # Solo a los propietarios se les otorgan permisos para métodos inseguros       
            return obj.owner == request.user 