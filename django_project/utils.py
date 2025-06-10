import uuid
import hashlib
import vercel_blob
from comunidade.models import Community
from usuario.models import Profile
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

Ele também modifica o nome do arquivo para um uuid
junto com a extensão da imagem

Caso o contrário, ele enviará a imagem para o banco.

***IMPORTANTE***
Ele só verifica se a hash existe na tabela da comunidade.

Caso alguém criar uma tabela que tenha upload de arquivos
é importante também modifcar essa função para que verifique
se o arquivo já existe no banco (É só seguir da linha 48 até 51(ou linha do existe até return {existe:true}(seila)))
"""
def upload_vercel_image(file) -> dict:
    file_hash = get_hash_file_256(file)  # Pega a hash do arquivo
    existe = Community.objects.filter(profile_picture_hash=file_hash).first()  # Pega o primeiro resultado
    existe_profile = Profile.objects.filter(imagem_perfil_hash=file_hash).first()
    file.seek(0)  # Reseta o ponteiro do arquivo para garantir que ele será lido corretamente

    # Verifica se a imagem já existe na comunidade
    if existe is not None:
        return {"existe": True, "url": existe.profile_picture, "file_hash": file_hash, "erro": False, "source": "community"}

    # Se a imagem já existe no perfil de outro usuário, retorna a URL correspondente
    if existe_profile:
        return {"existe": True, "url": existe_profile.imagem_perfil, "file_hash": file_hash, "erro": False, "source": "profile"}

    # Caso contrário, tenta fazer o upload para o Vercel
    try:
        # Realiza o upload para o Vercel Blob
        response = vercel_blob.put(f"{uuid.uuid4()}.{file.name.split('.')[-1]}", file.read(), options={"token": BLOB_READ_WRITE_TOKEN})
        file.seek(0)  # Reseta o ponteiro para o arquivo após a leitura para garantir integridade do processo

        # Extrai a URL do arquivo carregado no Vercel
        blob_url = response["url"]

        # Retorna o resultado com a URL do arquivo carregado
        return {"existe": False, "url": blob_url, "file_hash": file_hash, "erro": False, "source": "upload"}

    except Exception as e:
        file.seek(0)  # Reseta o ponteiro em caso de erro
        # Retorna um erro caso o upload falhe
        return {"existe": False, "erro": True, "message": str(e)}

    