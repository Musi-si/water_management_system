from .models import Admin, Client, Usage
from django.contrib.auth.hashers import check_password

class H2O_management:
    @staticmethod
    def get_admins():
        return Admin.objects.all().order_by( 'id' )
    
    @staticmethod
    def get_admin( id ):
        return Admin.objects.get( id = id )
    
    @staticmethod
    def get_clients():
        return Client.objects.all()
    
    @staticmethod
    def get_client( id ):
        return Client.objects.get( id = id )

    @staticmethod
    def get_usages():
        return Usage.objects.select_related( 'client' ).all()

    @staticmethod
    def insert_clients( clients ):
        for client in clients:
            client.save()

    @staticmethod
    def insert_usages( usages ):
        for usage in usages:
            usage.save()

    @staticmethod
    def get_client_usage( id ):
        return Usage.objects.filter( client_id = id ).order_by( 'date' )

    @staticmethod
    def add_admin( name, email, password ):
        admin = Admin( name = name, email = email, password = password )
        admin.save()
        
    @staticmethod
    def add_client( name, email, password ):
        client = Client( name = name, email = email, password = password )
        client.save()

    @staticmethod
    def signin_admin( email, password ):
        try:
            admin = Admin.objects.get( email = email )
            if check_password( password, admin.password ):
                return { 'status': 'success', 'admin': admin }
            else:
                return { 'status': 'error', 'message': 'Invalid password' }
        except Admin.DoesNotExist:
            return { 'status': 'error', 'message': 'Invalid email' }
        except Exception as e:
            return { 'status': 'error', 'message': f'An error occured: { str( e ) }' } 

    @staticmethod
    def signin_client( email, password ):
        try:
            client = Client.objects.get( email = email )
            if check_password( password, client.password ):
                return { 'status': 'success', 'client': client }
            else:
                return { 'status': 'error', 'message': 'Invalid password' }
        except Client.DoesNotExist:
            return { 'status': 'error', 'message': 'Invalid email' }
        except Exception as e:
            return { 'status': 'error', 'message': f'An error occured: { str( e ) }' } 
    
    @staticmethod
    def record_usage( client_id, date, quantity ):
        client = Client.objects.get( id = client_id )
        try:
            usage = Usage.objects.get( client = client, date = date )
            usage.quantity += quantity
            usage.save()
        except Usage.DoesNotExist:
            try:
                usage = Usage( client = client, date = date, quantity = quantity )
                usage.save()
            except Exception as e:
                return { 'status': 'error', 'message': f'An error occurred while creating usage: { str( e ) }' }
        return { 'status': 'success' }
    
    @staticmethod
    def filter_admin_usage( start_date, end_date, client_id ):
    # def filter_admin_usage( start_date, end_date, client_id, max_quantity, min_quantity ):
        try:
            usages = Usage.objects.all()
            if start_date and end_date:
                usages = usages.filter( date__range = [ start_date, end_date ] )
            if client_id:
                usages = usages.filter( client_id = client_id )
            # if max_quantity:
            #     usages = usages.filter( quantity__lte = max_quantity )
            # if min_quantity:
            #     usages = usages.filter( quantity__gte = min_quantity )
            return { 'status': 'success', 'usages': usages.order_by( 'client_id' ) }
        except Exception as e:
            return { 'status': 'error', 'message': f'An error occured: { str( e ) }' }
    
    @staticmethod
    def filter_client_usage( id, start_date, end_date, max_quantity, min_quantity ):
        try:
            usages = Usage.objects.filter( client_id = id )
            if start_date and end_date:
                usages = usages.filter( date__range = [ start_date, end_date ] )
            if max_quantity:
                usages = usages.filter( quantity__lte = max_quantity )
            if min_quantity:
                usages = usages.filter( quantity__gte = min_quantity )
            return { 'status': 'success', 'usages': usages.order_by( 'date' ) }
        except Exception as e:
            return { 'status': 'error', 'message': f'An error occured: { str( e ) }' }
    
    @staticmethod
    def delete_admin( admin_id ):
        try:
            admin = Admin.objects.get( id = admin_id )
            admin.delete()
            return { 'status': 'success' }
        except Admin.DoesNotExist:
            return { 'status': 'error', 'message': 'Invalid admin ID' }
        except Exception as e:
            return { 'status': 'error', 'message': f'An error occured: { str( e ) }' } 
    
    @staticmethod
    def delete_client( client_id ):
        try:
            client = Client.objects.get( id = client_id )
            client.delete()
            return { 'status': 'success' }
        except Admin.DoesNotExist:
            return { 'status': 'error', 'message': 'Invalid client ID' }
        except Exception as e:
            return { 'status': 'error', 'message': f'An error occured: { str( e ) }' }