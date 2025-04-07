import sys
import os
from tqdm import tqdm
import logging
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from spellchecker import SpellChecker

#IMPORTACIONES LOCALES
from process.ingestion.ingestion import Ingestion
from process.transformation.dictionary import Dictionary
from process.cloud.conection import cloud


def main():
    #Configuración del logger
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s - %(module)s', handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ])
    logger = logging.getLogger()

    #INICIO DEL PROCESO
    try:
        #cred = credentials.Certificate('C:/Users/jalex/Documents/TESIS/Dictaminador/Dictaminador/test_resources/keys/dictaminador3312-firebase-adminsdk-x5dq4-91a0021b87.json')
        #firebase_admin.initialize_app(cred, {
        #                                        'databaseURL': 'https://dictaminador3312-default-rtdb.firebaseio.com/'
        #                                    })
        logger.info("Conexión a Firebase exitosa")
        '''
        Ingreso de datos
        '''
        pathlibro = "C:/Users/jalex/Documents/TESIS/Dictaminador/Dictaminador/test_resources/input/libro/el-agua-manuel-guerrero.pdf"
        pathresumen = "C:/Users/jalex/Documents/TESIS/Dictaminador/Dictaminador/test_resources/input/resumen/resumen del libro el agua.pdf"
        isbn = "278-84-376-0494-7"

        logger.info("Iniciando proceso de ingestión")  

        book_name = os.path.splitext(os.path.basename(pathlibro))[0]
        resumen_name = os.path.splitext(os.path.basename(pathresumen))[0]

        book_words, original_book_words  = Ingestion.text_preprocess(pathlibro, logger)
        logger.info(f"Proceso de ingestión de libro finalizado para el libro {book_name} + {isbn}")

        resumen_words, original_resumen_words = Ingestion.text_preprocess(pathresumen, logger)
        logger.info(f"Proceso de ingestión de resumen finalizado para el resumen {resumen_name} + {isbn}")
        
        data_book = Dictionary.create_dict_book(isbn, book_name, book_words)
        data_resumen = Dictionary.create_dict_resumen(isbn, resumen_name, resumen_words)
        
        # logger.info(f"Iniciando proceso de guardado en Firebase")
        #cloud.post_data(data_book, data_resumen)
        # logger.info(f"Datos guardados en Firebase")

        df_book = pd.DataFrame(data_book[isbn]['book_words'])
        df_resumen = pd.DataFrame(data_resumen[isbn + "_resumen_" + resumen_name]['resumen_words'])

        texts = book_words + resumen_words
        vectorizer = TfidfVectorizer()

        tfidf_matrix = vectorizer.fit_transform(texts)

        tfidf_libro = tfidf_matrix[:len(df_book)]
        tfidf_resumen = tfidf_matrix[len(df_book):]

        similarities = cosine_similarity(tfidf_libro, tfidf_resumen)

        threshold = 0.8

        copied_fragments = (similarities > threshold).sum()

        total_fragments = similarities.shape[0]
        percentage_copied = (copied_fragments / total_fragments)

        print(f"El porcentaje de copia exacta es: {percentage_copied:.2f}%")

        #MODULO DE ORTOGRAFIA
        logger.info("Iniciando evaluación ortográfica")

        spell = SpellChecker(language='es')

        # Unifica palabras de ambos textos
        all_words =  resumen_words

        # Lista de palabras mal escritas
        misspelled = spell.unknown(all_words)

        logger.info(f"Número de palabras mal escritas: {len(misspelled)}")
        #logger.info(f"Palabras mal escritas: {misspelled}")

        #calcular el porcentaje de palabras mal escritas
        total_words = len(all_words)
        total_misspelled = len(misspelled)
        percentage_misspelled = (total_misspelled / total_words) * 100
        logger.info(f"Porcentaje de palabras mal escritas: {percentage_misspelled:.2f}%")

        #MODULO DE GRAMATICA
        logger.info("Iniciando evaluación gramatical")
        import language_tool_python

        def evaluar_gramatica_ltool(texto):
            tool = language_tool_python.LanguageTool('es')
            
            matches = tool.check(texto)
            total_errores = len(matches)
            total_palabras = len(texto.split())
            
            # Puntuación: 100 si no hay errores, menos si hay muchos errores
            if total_palabras == 0:
                return 1.0
            
            porcentaje_errores = total_errores / total_palabras
            puntuacion = max(1, min(100, 100 - (porcentaje_errores * 100)))
            
            return round(puntuacion, 2), total_errores, matches

        puntuacion, errores, detalles = evaluar_gramatica_ltool(original_resumen_words)

        print(f"Calificación gramatical: {puntuacion}/100")
        print(f"Número de errores detectados: {errores}")
        for err in detalles:
            print(f"- {err.message} | → {err.context}")


    except Exception as e:
        print(e)

main()

