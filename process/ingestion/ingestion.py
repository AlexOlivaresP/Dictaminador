import fitz 
import logging
import re
import spacy


class Ingestion:

    def __init__(self, path: str):
        self.path = path

    def pdf_reader(path) -> str:
        """
        Esta función recibe el path de un archivo pdf y devuelve el texto del mismo.
        
        Args:
            path (str): path del archivo pdf
            
        Returns:
            str: texto del archivo pdf
                
        """
        try:
            doc = fitz.open(path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            print(f"Error en la funcion pdf_reader: {e}")
    
    def text_tokenizer(text, nlp) -> list:
        """
        Esta función recibe un texto y devuelve una lista con los tokens del mismo.

        Args:
            text (str): texto a tokenizar
            nlp (spacy.lang): modelo de lenguaje spacy

        Returns:
            list: lista con los tokens del texto
        """
        try:
            doc = nlp(text)
            tokens = [token.text for token in doc]
            return tokens
        except Exception as e:
            print(f"Error en la funcion text_tokenizer: {e}")

    def text_lemmatizer(text, nlp) -> list:
        """
        Esta función recibe un texto y devuelve una lista con los lemas del mismo.
        
        Args:
            text (list): texto a lemmatizar
            nlp (spacy.lang): modelo de lenguaje spacy

        Returns:
            list: lista con los lemas del texto
        """
        try:
            lemmas = []
            for token in text:
                doc = nlp(token)
                lemmas.append(doc[0].lemma_)
            return lemmas
        except Exception as e:
            print(f"Error en la funcion text_lemmatizer: {e}")

    def clean_text(tokens) -> list:
        """
        Esta función recibe un texto y devuelve el mismo texto limpio de caracteres especiales y conexiones.

        Args:
            tokens (list): texto a limpiar

        Returns:
            text: lista texto limpio
        """
        try:
            clean_text = []
            connections = ['uno', 'unos', 'unas', 'una', 'un', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'e', 'i', 'o', 'u','y', 'el', 'yo', 'me', 'mí', 'conmigo', 'tú', 'te', 'ti', 'contigo', 'él', 'ella', 'ello', 'le', 'lo', 'la', 'se', 'sí', 'consigo', 'nosotros', 'nosotras', 'nos', 'vosotros', 'vosotras', 'os', 'ustedes', 'ellos', 'ellas', 'les', 'los', 'las', 'mi', 'mis', 'tu', 'tus', 'su', 'sus', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros', 'vuestras', 'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas', 'aquel', 'aquella', 'aquellos', 'aquellas', 'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 'cuyo', 'cuya', 'cuyos', 'cuyas', 'que', 'cual', 'quien', 'quienes', '', 'a', 'o', 'la', 'ante', 'bajo', 'cabe', 'con', 'contra', 'de', 'desde', 'durante', 'en', 'entre', 'hacia', 'hasta', 'mediante', 'para', 'por', 'según', 'sin', 'sobre', 'tras', 'versus', 'vía', 'so', 'pro']
            
            for token in tokens:
                token = token.lower()
                token = re.sub(r'\n|\t', '', token)
                token = re.sub(r'[^\w\s]', '', token)
                token = re.sub(r'\d', '', token)
                token = re.sub(r'[.*\s.*]', '', token)
                if token not in connections:
                    clean_text.append(token)
            
            return clean_text
        except Exception as e:
            print(f"Error en la funcion clean_text: {e}")

    def text_preprocess(path: str):
        """
        Esta función recibe el path de un archivo pdf y devuelve el texto preprocesado.

        Args:
            path (str): path del archivo pdf

        Returns:
            list: texto preprocesado
        """
        nlp = spacy.load("es_core_news_sm")
        try:
            ingestion = Ingestion.pdf_reader(path)
            tokens = Ingestion.text_tokenizer(ingestion, nlp)
            clean_text = Ingestion.clean_text(tokens)
            lemmas = Ingestion.text_lemmatizer(clean_text, nlp)
            return lemmas

        except Exception as e:
            print(e)