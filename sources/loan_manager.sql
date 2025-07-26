create schema Loan_manager;

create table Clients
(
    id         int auto_increment
        primary key,
    nombre     Varchar(255) not null,
    correo     Varchar(255) not null,
    rfc        Varchar(255) not null,
    fecha_alta DATETIME     not null
);


create table Loans
(
    id                 int auto_increment
        primary key,
    client_id          int                                  not null,
    amount             FLOAT                                not null,
    fecha_otorgamiento DATETIME                             not null,
    status             ENUM ('activo', 'pagado', 'vencido') null,
    constraint Loans_Clients_id_fk
        foreign key (client_id) references Clients (id)
);

select * from Clients

select * from Loans