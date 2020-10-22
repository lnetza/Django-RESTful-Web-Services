from django.db import models

# Create your models here.
class DroneCategory(models.Model): 
    name = models.CharField(max_length=250) 
 
    class Meta: 
        ordering = ('name',) 
 
    def __str__(self): 
        return self.name 
 
#El valor de 'drones' especificado para el 
# argumento related_name crea una relación hacia
#  atrás desde el modelo DroneCategory al modelo Drone.
class Drone(models.Model): 
    name = models.CharField(max_length=250) 
    drone_category = models.ForeignKey( 
        DroneCategory, 
        related_name='drones', 
        on_delete=models.CASCADE) 
    manufacturing_date = models.DateTimeField() 
    has_it_competed = models.BooleanField(default=False) 
    inserted_timestamp = models.DateTimeField(auto_now_add=True) 
 
    class Meta: 
        ordering = ('name',) 
 
    def __str__(self): 
        return self.name 

class Pilot(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE,'Male'),
        (FEMALE, 'Female'),
    )
    name= models.CharField(max_length=150, blank=False, default='')
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        default=MALE,
    )
    races_count = models.IntegerField()
    inserted_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name

#El valor de 'competiciones' especificado para el argumento 
# related_name crea una relación hacia atrás del modelo Pilot 
# al modelo Competición
class Competition(models.Model):
    pilot = models.ForeignKey(
        Pilot,
        related_name='competitions',
        on_delete=models.CASCADE)
    drone = models.ForeignKey(
        Drone,
        on_delete=models.CASCADE)
    distance_in_feet = models.IntegerField()
    distance_achievement_date = models.DateTimeField()

    class Meta:
        #Order distance in descending order
        ordering = ('-distance_in_feet',)