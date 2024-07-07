from firebase_admin import db
import pandas as pd


class cloud:
    def __init__(self):
        self.ref = db.reference('dictaminador3312')

    def post_data(data_book: dict, data_resumen: dict):
        """
        Esta función recibe un diccionario y lo guarda en la base de datos de firebase.
        
        Args:
            data (dict): diccionario con los datos a guardar
        """
        try:
            ref_book = db.reference('book')
            ref_resume = db.reference('resumen')

            for key, value in data_book.items():
                ref_book.child(key).set(value)
            for key, value in data_resumen.items():
                ref_resume.child(key).set(value)

        except Exception as e:
            print(f"Error en la funcion post_data: {e}")
            return None