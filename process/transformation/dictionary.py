import pandas as pd

class Dictionary:
    def __init__(self):
        pass

    def create_dict_book(isbn, book_name, book_words) -> dict:
        """
        Esta función recibe un dataframe y lo convierte en un diccionario.
        
        Args:
            isbn (str): ISBN del libro
            book_name (str): nombre del libro
            book_words (list): lista con las palabras del libro
            
        Returns:
            dict: diccionario con los datos del dataframe
        """
        try:
            data = {
            "ID" :  isbn,
            "book_name": book_name, 
            "book_words": book_words,
            "book_words_count": len(book_words)
            }
        
            return {isbn: data}
        except Exception as e:
            print(f"Error en la función create_dict: {e}")
            return None
    
    def create_dict_resumen(isbn, resumen_name, resumen_words) -> dict:
        """
        Esta función recibe un dataframe y lo convierte en un diccionario.
        
        Args:
            isbn (str): ISBN del libro
            resumen_name (str): nombre del resumen
            resumen_words (list): lista con las palabras del resumen

        Returns:

            dict: diccionario con los datos del dataframe
        """
        try:
            data = {
            "ID" :  isbn,
            "resumen_name": resumen_name, 
            "resumen_words": resumen_words,
            "resumen_words_count": len(resumen_words)
            }
            id_resume = isbn + "_resumen_" + resumen_name

            return {id_resume: data}
        except Exception as e:
            print(f"Error en la función create_dict: {e}")
            return None