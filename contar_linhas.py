from glob import glob
import os
from pprint import pprint

with open('total.txt', 'w') as f:
    f.write('')

numero_de_linhas = 0

def document_in_list_of_directories(document, directories):
    check = False
    for directory in directories:
        if directory in document:
            check = True

    return check

LIBS = [
    'contar_linhas.py',
]

DIRECTORIES = ['.mypy_cache', '.venv', '__pycache__',
            'worker_rmq', 'worker_loop', 'src/main/static/bootstrap']

def contar_linhas(documento: str) -> int:
    with open(documento) as f:
        content = f.readlines()
        content = [line.strip() for line in content if line.strip() != '']
        len_content = len(content)
    return len_content


FORMATOS = ['html', 'css', 'js', 'py', 'yml',
            'conf', 'dockerfile', 'sql']

GLOBS = [
    glob(f'**/*.{formato}', recursive=True)
    for formato in FORMATOS
]
dic = {}
last = None

n = 0
for GLOB in GLOBS:
    try:
        formato = GLOB[0].split('.')[-1]
        l = 0
        if GLOB:
            for i, documento in enumerate(GLOB):
                if not document_in_list_of_directories(documento, DIRECTORIES): 
                    print(documento)
                    numero_de_linhas += contar_linhas(documento)
                    l += contar_linhas(documento)
                    n += 1

        dic[formato] = l
    except IndexError:
        pass
        
# pprint(dic)
print(f"O número total de linhas em todos os {n} arquivos é {numero_de_linhas}.")