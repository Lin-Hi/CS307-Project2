select *
from cs307_3.pg_catalog.pg_user;

select *
from cs307_3.pg_catalog.pg_roles;;

-- this is an example for top user
create user t123123 superuser password '123456';

-- this is an example for salesman
create user s12110429;
alter user s12110429 password '123456';
grant select on "order" to s12110429;
create policy salesman_order on "order" for select to s12110429 using (salesman_number = '12110429');
alter table "order"
    enable row level security;

-- this is an example for contract manager
create user c12011529;
alter user c12011529 password '123456';

grant select on "order" to c12011529;
grant select on contract to c12011529;

create policy manager_order
    on "order"
    for select to c12011529
    using (contract_number in (select contract.contract_number
                               from contract
                               where contract_manager_number = '12011529'));
alter table "order"
    enable row level security;

create policy manager_contract
    on contract
    for select to c12011529
    using (contract_manager_number = '12011529');
alter table contract
    enable row level security;


-- check whether a user is already exist
select count(*)
from pg_catalog.pg_user
where usename = 's12110429';



drop owned by salesman;
drop role salesman;
drop owned by s12110429;
drop user s12110429;

select *
from center;

select *
from contract;

select *
from "order";
