# engsw-2025-1

# Nome do Projeto

Um breve descrição do que o projeto faz e seu propósito.
*O aplicativo possibilita reprodução de música de forma mais interativa com outros usuários. Ouvir e falar sobre música, artistas, álbuns e trilhas, tudo num mesmo lugar. Com criação de comunidades, a plataforma proporciona conversas, discussões, compartilhamento entre seguidores e comunidade, as interções se tornam fáceis e diretas!* *

## Descrição

Este projeto tem como objetivo [descrição do que o projeto faz, o problema que resolve, etc.].

*Este projeto tem como objetivo promover a interação com os usuários, enquanto oferece um reprodutor de música, tudo centralizado num aplicativo só. ___tify não possibilita muita interação entre usuários, então decidimos criar este projeto.* *

## Tecnologias Usadas

- **Backend**: Django
- **Banco de Dados**: Oracle
- **Autenticação**: ?
- **DevOps**: ?

## Como rodar o projeto localmente

1. Clone o repositório com o comando:
   ```bash
   git clone <url-do-repositório>
   ```
2. Na pasta, crie um ambiente virutal, com o comando:
    ```bash
    python -m venv venv
    ``` 
    E ative. Windows:
    ```bash
    venv\Scripts\activate
    ```
    MacOS/Linux:
    ```bash
    source venv/bin/activate
    ```
3. Depois de ativar o ambiente virutal, vamos instalar as dependências do projeto:
   ```bash
   pip install django
   pip install -r requirements.txt
   ```
4. Rode comandos do Django para rodar localmente:
   ```bash
    python3 manage.py makemigrations
	python3 manage.py migrate
	python3 manage.py runserver
    ```
## Como Contribuir

1. 

Siga as **[boas práticas de contribuição](./docs/guia-contribuicao.md)**.

## Histórias de Usuário e Planejamento

As histórias de usuário e planejamento de sprints estão organizadas no [GitHub Projects](https://github.com/users/ermidapablo/projects/1).

## Documentação

Para mais detalhes sobre o projeto, arquitetura e decisões de design, consulte a [Wiki do Repositório](https://github.com/ermidapablo/engsw-2025-1/wiki), onde você pode encontrar informações detalhadas sobre o desenvolvimento e processos de cada sprint, retrospectivas, objetivos e mais.
