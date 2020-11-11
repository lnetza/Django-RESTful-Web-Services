from rest_framework.pagination import LimitOffsetPagination 
class LimitOffsetPaginationWithUpperBound(LimitOffsetPagination):    
    # Se asigna limite maximo con valor a 8       
    max_limit = 8