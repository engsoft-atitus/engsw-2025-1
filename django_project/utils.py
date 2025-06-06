import hashlib
import vercel_blob
from comunidade.models import Community
from django_project.settings import BLOB_READ_WRITE_TOKEN


"""
Basicamente essa função pega uma imagem enviada (ou seja inMemory, nada local)
e pega a hash dela

Resumindo o seek, ele volta o arquivo pro inicio do ponteiro
depois dele ser lido

Ele é importante porque caso o ponteiro do arquivo não
seja resetado, ele fica imposivel de ler e impossibilita
o upload para vercel blob
"""
def get_hash_file_256(file) -> str:
    hash = hashlib.sha256(file.read()).hexdigest()
    file.seek(0) # Esse seek é extremamente importante
    return hash

"""
Caso um arquivo já exista no vercel, ele negará
o upload. 

Como eu creio que não haja uma forma do vercel 
retornar a url, eu fiz essa função para verificar
se o arquivo já existe no nosso banco de dados
(hash do arquivo) e caso exista ele retorna a 
url e hash do arquivo existente.

Caso o contrário, ele enviará a imagem para o banco.

***IMPORTANTE***
Ele só verifica se a hash existe na tabela da comunidade.

Caso alguém criar uma tabela que tenha upload de arquivos
é importante também modifcar essa função para que verifique
se o arquivo já existe no banco (É só seguir da linha 44 até 47)
"""
def upload_vercel_image(file) -> dict:
    file_hash = get_hash_file_256(file) # Pega a hash do arquivo
    existe = Community.objects.filter(profile_picture_hash=file_hash).first() # Pega o primeiro resultado
    file.seek(0) # Eu não sei se esse seek é necessário
    if existe != None: # Caso exista, exista, ele retorna a url que conseguiu
        return {"existe":True, "url":existe.profile_picture,"file_hash":file_hash,"erro":False}
    # Caso contrário ele tenta fazer um upload para o vercel
    try:
        response = vercel_blob.put(file.name,file.read(),options={"token":BLOB_READ_WRITE_TOKEN})
        file.seek(0)
        blob_url = response["url"]
        return {"existe":False,"url":blob_url,"file_hash":file_hash,"erro":False}
    except Exception:
        file.seek(0)
        return {"existe":False,"erro":True}
    