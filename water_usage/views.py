import json
from .services import H2O_management
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import pandas as pd

# Create your views here.
# QUERY OK
def signup_page_view( request ):
    return render( request, 'signup.html' )

# QUERY OK
def get_clients_view( request ):
    id = request.GET.get( 'admin' )
    admin = H2O_management.get_admin( id )
    usages = H2O_management.get_usages()

    usage_data = []
    for usage in usages:
        usage_data.append( {
            'client_id': usage.client.id,
            'name': usage.client.name,
            'email': usage.client.email,
            'date': usage.date,
            'quantity': usage.quantity
        } )

    cdf = pd.DataFrame( usage_data )
    final = cdf.groupby( [ 'client_id', 'name', 'email' ], as_index = False )[ 'quantity' ].sum()

    page_nbr = request.GET.get( 'page', 1 )
    paginator = Paginator( final.to_dict( 'records' ), 20 )
    page_objects = paginator.get_page( page_nbr )
    
    return render( request, 'admin.html', {
        'admin': admin,
        'admins': H2O_management.get_admins(),
        'clients': page_objects
    } )

# QUERY OK
def client_graph_view( request, id, usages ):
    client = H2O_management.get_client( id )
    dates = [ usage.date.strftime( '%Y-%m-%d' ) for usage in usages ]
    quantities = [ usage.quantity for usage in usages ]
    print( dates, quantities)
    return render( request, 'client.html', {
        'client': client,
        'usages': usages,
        'labels': json.dumps( dates ),
        'data': json.dumps( quantities )
    } )

# QUERY OK
def signup_view( request ):
    if request.method == 'POST':
        account_type = request.POST.get( 'account_type' )
        if account_type == 'admin':
            pin = request.POST.get( 'pin' )
            if pin != '159732684':
                messages.error( request, 'Invalid PIN. Please enter the correct PIN to sign up.' )
                return render( request, 'signup.html' )
            elif pin == '159732684':
                return signup_admin_view( request )
        else:
            return signup_client_view( request )
    else:
        return signup_page_view( request )

# QUERY OK
def signup_admin_view( request ):
    if request.method == 'POST':
        name = request.POST.get( 'name' )
        email = request.POST.get( 'email' )
        password = make_password( request.POST.get( 'password' ) )
        H2O_management.add_admin( name, email, password )
        return signin_admin_view( request )

# QUERY OK
def signup_client_view( request ):
    if request.method == 'POST':
        name = request.POST.get( 'name' )
        email = request.POST.get( 'email' )
        password = make_password( request.POST.get( 'password' ) )
        H2O_management.add_client( name, email, password )
        return signin_client_view( request )

# QUERY OK
def signin_view( request ):
    if request.method == 'POST':
        account_type = request.POST.get( 'account_type' )
        if account_type == 'admin':
            pin = request.POST.get( 'pin' )
            if pin != '159732684':
                messages.error( request, 'Invalid PIN. Please enter the correct PIN to sign in.' )
                return render( request, 'signup.html' )
            elif pin == '159732684':
                return signin_admin_view( request )
        else:
            return signin_client_view( request )
    else:
        return signup_page_view( request )

# QUERY OK
def signin_admin_view( request ):
    if request.method == 'POST':
        email = request.POST.get( 'email' )
        password = request.POST.get( 'password' )
        results = H2O_management.signin_admin( email, password )
        if results.get( 'status' ) == 'success':
            return redirect( f'get-clients/?admin={ results.get( 'admin' ).id }' )
        else:
            return render( request, 'signup.html', {
                'error_message': results.get( 'message' )
            } )

# QUERY OK
def signin_client_view( request ):
    if request.method == 'POST':
        email = request.POST.get( 'email' )
        password = request.POST.get( 'password' )
        results = H2O_management.signin_client( email, password )
        if results.get( 'status' ) == 'success':
            id = results.get( 'client' ).id
            usages = H2O_management.get_client_usage( id )
            return client_graph_view( request, id, usages )
        else:
            return render( request, 'signup.html', {
                'error_message': results.get( 'message' )
            } )

# QUERY OK
def record_usage_view( request ):
    if request.method == 'POST':
        id = request.POST.get( 'id' )
        date = request.POST.get( 'date' )
        quantity = float( request.POST.get( 'quantity' ) )
        results = H2O_management.record_usage( id, date, quantity )
        usages = H2O_management.get_client_usage( id )
        if results.get( 'status' ) == 'success':
            return client_graph_view( request, id, usages )
        else:
            return render( request, 'client.html', {
                'error_message_record': results.get( 'message' )
            } )
    
# QUERY OK
def filter_admin_usage_view( request ):
    if request.method == 'GET':
        id = request.GET.get( 'admin_id' )
        start_date = request.GET.get( 'start_date' )
        end_date = request.GET.get( 'end_date' )
        client_id = request.GET.get( 'id' )
        max_quantity = request.GET.get( 'max_quantity' )
        min_quantity = request.GET.get( 'min_quantity' )

        admin = H2O_management.get_admin( id )
        results = H2O_management.get_usages()
        usage_data = [
            {
                'client_id': usage.client.id,
                'name': usage.client.name,
                'email': usage.client.email,
                'date': usage.date,
                'quantity': usage.quantity
            }
            for usage in results
        ]
        cdf = pd.DataFrame( usage_data )

        if start_date and end_date:
            cdf = cdf[ ( pd.to_datetime( cdf[ 'date' ] ) > pd.to_datetime( start_date ) ) & ( pd.to_datetime( cdf[ 'date' ] ) < pd.to_datetime( end_date ) ) ]

        cdf = cdf.groupby( [ 'client_id', 'name', 'email' ], as_index = False )[ 'quantity' ].sum()
        
        if client_id:
            cdf = cdf[ cdf[ 'client_id' ] == int( client_id ) ]

        if max_quantity:
            cdf = cdf[ cdf[ 'quantity' ] < float( max_quantity ) ]

        if min_quantity:
            cdf = cdf[ cdf[ 'quantity' ] > float( min_quantity ) ]

        page_nbr = request.GET.get( 'page', 1 )
        paginator = Paginator( cdf.to_dict( 'records' ), 20 )
        page_objects = paginator.get_page( page_nbr )
        
        return render( request, 'admin.html', {
            'admin': admin,
            'admins': H2O_management.get_admins(),
            'clients': page_objects
        } )
    else:
        return render( request, 'admin.html', {
            'error_message': results.get( 'message' )
        } )
    
# QUERY OK
def filter_client_usage_view( request ):
    if request.method == 'GET':
        id = request.GET.get( 'id' )
        start_date = request.GET.get( 'start_date' )
        end_date = request.GET.get( 'end_date' )
        max_quantity = request.GET.get( 'max_quantity' ) 
        min_quantity = request.GET.get( 'min_quantity' )
        results = H2O_management.filter_client_usage( id, start_date, end_date, max_quantity, min_quantity )
        usages = results.get( 'usages' )
        if results.get( 'status' ) == 'success':
            return client_graph_view( request, id, usages )
        else:
            return render( request, 'client.html', {
                'error_message': results.get( 'message' )
            } )
    
# QUERY OK
def delete_admin_view( request ):
    if request.method == 'POST':
        admin_id = request.POST.get( 'admin_id' )
        id = request.POST.get( 'id' )
        results = H2O_management.delete_admin( id )
        if results.get( 'status' ) == 'success':
            return redirect( f'get-clients/?admin={ admin_id }' )
        else:
            return render( request, 'admin.html', {
                'error_message_admin': results.get( 'message' )
            } )

# QUERY OK
def delete_client_view( request ):
    if request.method == 'POST':
        client_id = request.POST.get( 'id' )
        id = request.POST.get( 'admin_id' )
        results = H2O_management.delete_client( client_id )
        if results.get( 'status' ) == 'success':
            return redirect( f'get-clients/?admin={ id }' )
        else:
            return render( request, 'admin.html', {
                'error_message_client': results.get( 'message' )
            } )