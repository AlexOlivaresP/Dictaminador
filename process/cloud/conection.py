import firebase_admin
from firebase_admin import credentials, db
import pandas as pd


class cloud:
    def __init__(self):
        self.ref = db.reference('dictaminador3312')

    def post_data(data: dict):
        """
        Esta función recibe un diccionario y lo guarda en la base de datos de firebase.
        
        Args:
            data (dict): diccionario con los datos a guardar
        """
        try:
            cred = credentials.Certificate('C:/Users/jalex/Documents/TESIS/Dictaminador/Dictaminador/test_resources/keys/dictaminador3312-firebase-adminsdk-x5dq4-91a0021b87.json')
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://dictaminador3312-default-rtdb.firebaseio.com/'
            })
            ref = db.reference('book')
            ref.push(data)
            print("\nDatos guardados en la base de datos de firebase")

        except Exception as e:
            print(f"Error en la funcion post_data: {e}")


