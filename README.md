
example_app/
├── app.py
├── requirements.txt
├── config.yaml
├── utils/
│   ├── db.py
│   └── helpers.py
├── tests/
│   ├── test_app.py
│   └── test_helpers.py
├── README.md


# To-Do List API

A simple To-Do List API built with Flask.

## Installation




# virtualenv

```sh
python3 -m venv .
source ./bin/activate

python3 -m pip install pytest

```



1. Clone the repository:
   ```bash
   git clone https://example.com/example_app.git
   cd example_app

pip install -r requirements.txt


python app.py

API Endpoints

GET /tasks - List all tasks
POST /tasks - Create a new task
PUT /tasks/<id> - Toggle task completion
DELETE /tasks/<id> - Delete task 

```


# Testing

```sh
python -m unittest discover tests

```


# TODO


## Parte 1 - Aplicação e Infra estrutura.

1. Adicionar o endpoint de DELETE
2. Criar testes usando CURL para testar todos os endpoints.
3. Fazer Dockerfile para buildar e rodar o container localmente.
4. Fazer arquivo de deployment do kubernetes para rodar localmente.
5. Portforward para expor o serviço e acessar as tasks.


## Parte 2 - Novas funcionalidades - Mais infraestrutura
6. Banco de dados NO-SQL para salvar persistir os dados
7. Adicionar tela de login e controle de usuários. 
8. Adicionar Testes unitários
9. ...
10. ...


## Sessão 3
Monitoramento do ambiente e aplicação
Implementação de Controle de Logs
Automação de monitoramento de Logs com GenAI - AIOps

