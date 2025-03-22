import pandas as pd
from H2O_usage.models import Usage
from django.core.management.base import BaseCommand
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

class Command( BaseCommand ):
    def handle( self, *args, **kwargs ):

        data = Usage.objects.all().values( 'date', 'quantity' )

        df = pd.DataFrame( data )

        df[ 'date' ] = pd.to_datetime( df[ 'date' ] )

        df[ 'year' ] = df[ 'date' ].dt.year
        df[ 'month' ] = df[ 'date' ].dt.month
        df[ 'day' ] = df[ 'date' ].dt.day
        df[ 'weekday' ] = df[ 'date' ].dt.weekday

        df = df.drop( columns = [ 'date' ] )

        print( df.head() )

        x = df[ [ 'year', 'month', 'day', 'weekday' ] ]
        y = df[ 'quantity' ]

        x_train, x_test, y_train, y_test = train_test_split( x, y, test_size = 0.2, random_state = 42 )

        model = LinearRegression()
        model.fit( x_train, y_train )

        joblib.dump( model, 'water_usage_model.pkl' )

        print( 'Model training complete and saved as "water_usage_model.pkl"' )