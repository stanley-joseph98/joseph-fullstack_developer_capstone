from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # modelling many-to-one relationships
    name = models.CharField(max_length=100)
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('HATCHBACK', 'Hatchback'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
        ('MINIVAN', 'Minivan'),
        ('PICKUP', 'Pickup Truck'),
        ('SPORTS', 'Sports Car'),
        ('LUXURY', 'Luxury Car'),
        ('CROSSOVER', 'Crossover'),
        ('ROADSTER', 'Roadster'),
        ('VAN', 'Van'),
        ('MICRO', 'Microcar'),
        ('SUBCOMPACT', 'Subcompact'),
        ('COMPACT', 'Compact'),
        ('FULLSIZE', 'Full-Size'),
        ('OFFROAD', 'Off-Road Vehicle'),
        ('ELECTRIC', 'Electric Vehicle'),
        ('HYBRID', 'Hybrid Vehicle'),
        ('DIESEL', 'Diesel Vehicle'),
        ('FLEET', 'Fleet Vehicle'),
        ('MOTORHOME', 'Motorhome'),
        ('TARGA', 'Targa'),
        ('SALOON', 'Saloon'),
        ('EXECUTIVE', 'Executive Car'),
        ('CITY', 'City Car'),
        ('PERFORMANCE', 'Performance Car'),
        ('SUPER', 'Supercar'),
        ('CLASSIC', 'Classic Car'),
        ('TAXI', 'Taxi'),
        ('AMBULANCE', 'Ambulance'),
        ('POLICE', 'Police Car'),
        ('STATION_WAGON', 'Station Wagon'),
        ('FAMILY', 'Family Car'),
        ('MIDSIZE', 'Midsize Car'),
        ('LIMOUSINE', 'Limousine'),
    ]
    
    type = models.CharField(max_length=25, choices=CAR_TYPES, default='SUV')
    
    year = models.IntegerField(
        default=2024,
        validators=[
            MaxValueValidator(2024),
            MinValueValidator(2015)
        ]
    )

    def __str__(self):
        return self.name  # returns the name as string representation