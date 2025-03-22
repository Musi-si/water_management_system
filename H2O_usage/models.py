from django.db import models

# Create your models here.
class Admin( models.Model ):
    id = models.AutoField( primary_key = True )
    name = models.CharField( max_length = 100 )
    email = models.EmailField( unique = True )
    password = models.CharField( unique = True, max_length = 128 )
    created_at = models.DateField( auto_now_add = True )

    def __str__( self ):
        return self.name
    
class Client( models.Model ):
    id = models.AutoField( primary_key = True )
    name = models.CharField( max_length = 100 )
    email = models.EmailField( unique = True )
    password = models.CharField( max_length = 128 )
    created_at = models.DateField( auto_now_add = True )

    def __str__( self ):
        return self.name
    
class Usage( models.Model ):
    client = models.ForeignKey( 'Client', on_delete = models.CASCADE, related_name = 'usages' )
    date = models.DateField()
    quantity = models.FloatField()

    def __str__( self ):
        return f'{ self.client.name } - { self.date } - { self.quantity } liters'