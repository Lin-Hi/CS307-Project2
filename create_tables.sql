create table center
(
    name varchar
        constraint center_pk
            primary key
);

create table enterprise
(
    name          varchar
        constraint enterprise_pk
            primary key,
    country       varchar,
    city          varchar,
    supply_center varchar
        constraint enterprise_center_name_fk
            references center,
    industry      varchar
);

create table model
(
    number     varchar,
    model      varchar
        constraint model_pk
            primary key,
    name       varchar,
    unit_price int
);

create table staff
(
    name          varchar,
    age           int,
    gender        varchar,
    number        varchar
        constraint staff_pk
            primary key,
    supply_center varchar
        constraint staff_center_name_fk
            references center,
    mobile_number varchar,
    type          varchar
);

create table stock
(
    supply_center       varchar
        constraint stock_center_name_fk
            references center,
    product_model       varchar
        constraint stock_model_model_fk
            references model,
    supply_staff_number varchar
        constraint stock_staff_number_fk
            references staff,
    date                date,
    purchase_price      int,
    quantity            int
);

create table storage
(
    supply_center       varchar
        constraint storage_center_name_fk
            references center,
    product_model       varchar
        constraint storage_model_model_fk
            references model,
    supply_staff_number varchar
        constraint storage_staff_number_fk
            references staff,
    date                date,
    purchase_price      int,
    quantity            int,
    constraint storage_pk
        primary key (supply_center, product_model)
);

create table contract
(
    contract_number         varchar
        constraint contract_pk
            primary key,
    contract_manager_number varchar
        constraint contract_staff_number_fk
            references staff,
    enterprise_name         varchar
        constraint contract_enterprise_name_fk
            references enterprise,
    contract_type           varchar,
    contract_date           date
);

create table "order"
(
    contract_number         varchar
        constraint order_contract_contract_number_fk
            references contract (contract_number),
    product_model           varchar
        constraint order_model_model_fk
            references model,
    salesman_number         varchar
        constraint order_staff_number_fk
            references staff,
    quantity                int,
    estimated_delivery_date date,
    lodgement_date          date,
    constraint order_pk
        primary key (contract_number, product_model)
);

