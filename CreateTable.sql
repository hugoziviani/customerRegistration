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
