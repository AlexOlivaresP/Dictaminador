import pandas as pd

class Dictionary:
    def __init__(self):
        pass

    def create_dict(isbn, book_name, book_words) -> dict:
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
            data = [{
            "ID" :  isbn,
            "book_name": book_name, 
            "book_words": book_words,
            "book_words_count": len(book_words)
            }]
        
            df = pd.DataFrame(data)
            data_dict = df.to_dict(orient='records')
            return data_dict
        except Exception as e:
            print(f"Error en la función create_dict: {e}")
            return None