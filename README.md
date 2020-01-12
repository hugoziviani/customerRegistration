Configuracoes de rodar o projeto:
dúvidas: hugo_zivini@hotmail.com

Infraestrutura:
Este pequeno projeto foi pensado em mimetizar uma estrutura de produção.
Foi criado um container docker com um banco mysql que contém uma tabela simples
Este banco recebe requisições vindas da API via engine criada no código python
As respostas do banco são transladadas da API e levadas ao front-end (faltou implementar)

Para rodar a aplicaçao:
Parte A (Configurando o banco, container MYSQL)
1- Baixar e instalar o docker em sua máquina
2- clonar a imagem do mysql
3- subir um container com a imagem do mysql
4- entrar no container do mysql e criar a tabela dos dados com o script a seguir:
    use registers_db;
    CREATE TABLE customersTable (
        id integer AUTO_INCREMENT,
        name varchar(255) NOT NULL,
        birthDay date,
        generalRegistry varchar(200),
        address varchar(200),
        phoneNumber varchar(200),
        historic boolean,
        PRIMARY KEY (id)
    );

5- é opcional já inserir alguns dados, se quiser pode usar este modelo, já na interface com o banco:
OBS: não precisa passar o id, pois é autoincrementeado pelo banco
OBS2: Passar o historic = false, pois se não o registro não aparecerá na consulta pela API

    INSERT INTO customersTable (
        id, 
        name,
        birthDay, 
        generalRegistry, 
        address, 
        phoneNumber, 
        historic)
    VALUES (
        null, 
        "Natalia Josias de Oliveira",
        "2000-03-01",
        "MG-10.400.000",
        "Rua filé de merlusa, bairro SERRA",
        "31-9.9111-8888",
        false
    );
6 - como configurei o docker + mysql:
        A1- Rodando o mysql-docker
            $ docker run --name=customers_bd --env="MYSQL_ROOT_PASSWORD=adm.123" -p 3306:3306 -d mysql:latest
        A2-Acessar o mysql do docker pelo terminal (a senha será pedida)
            docker exec -it customers_bd mysql -uroot -p
        A3-Cria a base de dados
            mysql> CREATE DATABASE '..db...'
        A4-Cria a tabela dentro do BD
                use registers_db;
                CREATE TABLE customersTable (
                    id integer AUTO_INCREMENT,
                    name varchar(255) NOT NULL,
                    birthDay date,
                    generalRegistry varchar(200),
                    address varchar(200),
                    phoneNumber varchar(200),
                    historic boolean,
                    PRIMARY KEY (id)
                );
        A5-Cria um usuário para acessar o banco
            mysql> CREATE USER 'hugo'@'%' IDENTIFIED BY 'pwd.123'; (@% permite este usuário acessar de qq origem)

            GRANT ALL PRIVILEGES ON registers_db.* to 'hugo'@'%';

Parte B (Configurando API)
1-clonar o projeto no git
    link: https://github.com/hugoziviani/customerRegistration.git
2- instalar python3
3- instalar biblioteca virtualenv
    $ pip3 install virtualenv
4- Criar um ambiente virtual dentro do diretório do projeto
    $ virtualenv <.nomeDoAmbiente>
5- Ativar o ambiente virtual
    $ source ..nomeDoAmbiente/bin/activate
6- Instalar as dependencias listadas no 'requirement.txt', que está presente no diretório do projeto. Não consegui criar um script que rodasse isso automático

7- após tudo isso, rodar a API


Funcionamento da API: 
responde requisições em determinadas urls

Metodos (GET): Podem ser testados diretamente do navegador
1-Formulário de Cadastro
url: http://127.0.0.1:5000/index.html
exibe o formulário para cadastro de novos clientes
    OBS: por falta de tempo e domínio da tecnologia não consegui relacionar o front com o back, tive problema na serealização do objeto, o JSON enviado ao servidor da aplicação estava mal formatado. Isso fazia com que o servidor encarasse o objeto como nulo

2- Metodos (GET)
url: http://127.0.0.1:5000/allCustomers
lista todos os usuários já cadastrados em formato JSON. Estes registros poderiam ser utilizados em um dashboard para exibiçao.

3- Metodos (GET)
url: http://127.0.0.1:5000/allCustomers/<string:namePassed>
nesta url se passado um nome específico a API realiza a query e retorna somente um registro.

4- Metodo (POST)
url: http://127.0.0.1:5000/sendRegistry
salva registros com a formatação padrao do DB.
OBS: para teste desta funcionalidade utilizar postman e inserir um objeto no formato JSON como no exemplo abaixo:
OBS2: a data 'birthDay' deve ser inserida conforme o formato a seguir, tipo DATETIME.
    {
        "name":"Nome de Alguem",
        "birthDay":"2015-01-08",
        "generalRegistry":"07984462228",
        "address":"Rua do Alguem BH-MG-Brasil",
        "phoneNumber":"31-994223333"
    }

5-  Metodos (GET)
url: http://127.0.0.1:5000/<string:nameToDelete>
Deletar Registros:
optei pela deleção lógica de registros, o registro é reinserido no banco, com os mesmos dados, porém é setada a flag histórico. O nome para deleção pode ser aproximado, ele apagará a primeira ocorrencia do nome referente. Isso pode ser melhorado criando outras verificações.
