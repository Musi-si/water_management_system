from faker import Faker
from H2O_usage.models import Client, Usage
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

class Command( BaseCommand ):
    def handle( self, *args, **kwargs ):
        fake = Faker()

        clients_count = 25000
        usages_count = 480000
        size = 3000

        existing_c = set( Client.objects.values_list( 'email', flat =  True ) )
        clients = []
        for _ in range( clients_count ):
            name = fake.name()
            email = fake.email()
            if email not in existing_c:
                password = make_password( '12345678' )
                created_at = fake.date_this_year()
                client = Client( name = name, email = email, password = password, created_at = created_at )
                clients.append( client )
                existing_c.add( email )

            if len( clients ) == size:
                Client.objects.bulk_create( clients )
                print( f'Successfully created { size } clients' )
                clients = []

        clients = list( Client.objects.all() )
        usages = []
        for _ in range( usages_count ):
            client = random.choice( clients )
            date = fake.date_this_year()
            quantity = round( random.uniform( 20, 50 ), 2 )
            usage = Usage( client = client, date = date, quantity = quantity )
            usages.append( usage )

            if len( usages ) == size:
                Usage.objects.bulk_create( usages )
                print( f'Successfully created { size } usage records' )
                usages = []