import sys
import os
from tqdm import tqdm
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from process.ingestion.ingestion import Ingestion
from process.transformation.dictionary import Dictionary
from process.cloud.conection import cloud


def main():
    
    try:
        path = "C:/Users/jalex/Documents/TESIS/Dictaminador/Dictaminador/test_resources/input/pdf/test.pdf"
        isbn = "278-84-376-0494-7"
        book_name = os.path.splitext(os.path.basename(path))[0]
        
        total_steps = 3
        with tqdm(total=total_steps, desc="Procesando", unit="paso") as pbar:
            
            book_words = Ingestion.text_preprocess(path)
            pbar.update(1)  
            
            data = Dictionary.create_dict(isbn, book_name, book_words)
            pbar.update(1)  
            
            cloud.post_data(data)
            pbar.update(1)  

    except Exception as e:
        print(e)

main()

