-- Number of orders shipped by each salesrep.
select

(select 
e.firstName, 
e.lastName, 
count(*) as 'Number of shipped orders'
from employees e 
left join customers c on e.employeeNumber = c.salesRepEmployeeNumber
left join orders o on o.customerNumber = c.customerNumber
where o.status = 'Shipped'
group by e.firstName, e.lastName) shipped

order by count(*)desc

select 
e.firstName, 
e.lastName, 
count(*) as 'Number of shipped orders'
from employees e 
join orders o on o.customerNumber = c.customerNumber
join customers c on e.employeeNumber = c.salesRepEmployeeNumber
where o.status = 'Shipped'
group by e.firstName, e.lastName

select count(distinct salesRepEmployeeNumber) from customers