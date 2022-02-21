create database estadistiques;
use estadistiques;

create table jornadas(
	jornada int primary key
) engine=Innodb;

create table jugadors(
	nomJugador varchar(20) primary key
) engine=Innodb;

create table jornadaJugador(
	jornada int,
    nomJugador varchar(20),
    goles int,
    minutos int,
    actitud int,
    primary key (jornada, nomJugador),
    FOREIGN KEY (jornada) REFERENCES jornadas (jornada),
    FOREIGN KEY (nomJugador) REFERENCES jugadors (nomJugador)
) engine=Innodb;

create table usuario(
	nomUser varchar(10) primary key,
    passwd varchar(20)
) engine=Innodb;

insert into jornadas values (1);
insert into jornadas values (2);
insert into jornadas values (3);
insert into jornadas values (4);
insert into jornadas values (5);

insert into jugadors values("Antonio Garica");
insert into jugadors values("Jose Martinez");
insert into jugadors values("Francisco Lopez");
insert into jugadors values("Juan Sanchez");
insert into jugadors values("Pedro Gomez");
insert into jugadors values("Jesus Fernandez");
insert into jugadors values("Andres Cano");
insert into jugadors values("Ramon Garrido");
insert into jugadors values("Enrique Gil");
insert into jugadors values("Alvaro Ortiz");
insert into jugadors values("Emilio Valero");
insert into jugadors values("Diego Rodenas");

insert into usuario values("carles", "1234");
insert into usuario values("ruben", "4321");