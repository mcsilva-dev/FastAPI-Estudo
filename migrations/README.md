# Generic single-database configuration.

## Criando banco com alembic

para trabalhar com a criacao de modelos automatica do alembic, de inicio e necessario instalar a dependencia
`pip install alembic` e realizar o comando `alembic init <nome diretorio>` 

no arquivo `env.py` faca o importe do modelo de metadados sql que ira utilizar e atribua a variavel `target_metadata`
OBS:(pode ser necessario alterar tambem o `config` indicando onde esta a variavel de ambiente apontando para o caminho do banco,
     porem nao e necessario, pois pode ser inserida em `alembic.ini` em `sqlalchemy.uri`)

apos criar um modelo com sqlalchemy para o banco de dados e hora de criar um modelo automatico com alembic 
para isso utilize o comando\:
> `alembic revision --autogenerate -m "<comentario>"`
