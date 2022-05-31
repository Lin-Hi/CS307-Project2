-- getBestSalesman(type: str) amount
select *
from (select t1.salesman_number, s.name, rank() over (order by t1.s desc ) as rank, t1.s as sale_amount
      from (select o.salesman_number, sum(o.quantity * m.unit_price) as s
            from "order" o
                     join model m on o.product_model = m.model
            group by o.salesman_number) t1
               join staff s on t1.salesman_number = s.number) t2
where t2.rank <= 10;

-- getBestSalesman(type: str) model
select *
from (select t1.salesman_number                           as staff_number,
             s.name                                       as staff_name,
             rank() over (order by t1.model_amount desc ) as rank,
             t1.model_amount
      from (select o.salesman_number, sum(o.quantity) as model_amount
            from "order" o
            group by o.salesman_number) t1
               join staff s on t1.salesman_number = s.number) t2
where rank <= 10;

-- getBestSalesman(type: str) order
select t2.staff_number,
       t2.staff_name,
       t2.rank,
       t2.order_count
from (select t1.salesman_number                       as staff_number,
             s.name                                   as staff_name,
             t1.order_count,
             rank() over (order by order_count desc ) as rank
      from (select o.salesman_number,
                   count((o.salesman_number, o.product_model, o.contract_number)) as order_count
            from "order" o
            group by o.salesman_number) t1
               join staff s on t1.salesman_number = s.number) t2
where t2.rank <= 10;


-- getBestProfitProductModel()
select t4.product_model, t4.total_profit, t4.quantity
from (select t3.*, rank() over (order by total_profit desc ) as rank
      from (select t1.product_model, (total_sale_price - total_purchase_price) as total_profit, t2.quantity
            from (select s1.product_model, sum(s1.quantity * s1.purchase_price) as total_purchase_price
                  from stock s1
                  group by s1.product_model) t1
                     join
                 (select t.product_model, (t.sum * m.unit_price) as total_sale_price, t.sum as quantity
                  from (select s.product_model, sum(s.quantity) as sum
                        from stock s
                        group by s.product_model) t
                           join model m on t.product_model = m.model) t2
                 on t1.product_model = t2.product_model) t3) t4
where t4.rank <= 10;

-- getOrderBetweenDates(date1: str, date2: str, enterprise: str, contract_num: str)
select c.contract_date, o.*
from "order" o
         join contract c on o.contract_number = c.contract_number
where c.contract_date between '2000-1-1' and '2022-1-2'
  and c.enterprise_name = 'Nippon Life Insurance'
  and o.contract_number = 'CSE0000102';


-- getMostModelEnterpriseRecent()
select *
from (select t1.*, rank() over (order by deals desc ) as rank
from (select sum(o.quantity) as deals, c.enterprise_name
      from "order" o
               join contract c on o.contract_number = c.contract_number
      where c.contract_type = 'Finished'
        and c.contract_date >= date(now() - interval '1' year)
      group by c.enterprise_name) t1) t2
where t2.rank <= 10;


-- getLossProductModel()
(select product_model
 from (select distinct s.product_model, sum(s.quantity * s.purchase_price) as total_purchase_money
       from stock s
       where s.product_model in (select distinct product_model
                                 from stock
                                 except
                                 select distinct product_model
                                 from storage)
       group by s.product_model) t2
          join
      (select distinct m.model, sum(o.quantity * m.unit_price) as total_sale_money
       from "order" o
                join model m on o.product_model = m.model
       where m.model in (select distinct product_model
                         from stock
                         except
                         select distinct product_model
                         from storage)
       group by m.model) t3
      on t2.product_model = t3.model
 where total_purchase_money > total_sale_money)
union
select s3.product_model
from stock s3
where s3.product_model in (select distinct s1.product_model
                           from stock s1
                           except
                           select distinct s2.product_model
                           from storage s2)
  and s3.date < date(now() - interval '1' year);


-- getOrderEachMonth(center: str)
with t1 as (select to_char(c.contract_date, 'mm')                                          as month,
                   count(distinct (o.contract_number, o.product_model, o.salesman_number)) as order_cnt,
                   s.supply_center
            from "order" o
                     join contract c on o.contract_number = c.contract_number
                     join staff s on o.salesman_number = s.number
            group by to_char(c.contract_date, 'mm'), s.supply_center)
select t1.month, sum(t1.order_cnt) as order_count
from t1
where t1.supply_center = 'America'
group by t1.month;

