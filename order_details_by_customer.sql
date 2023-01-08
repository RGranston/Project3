-- each customer order details
use classicmodels;
select 
-- count(*) as 'total no. of orders',
c.customerNumber,
c.contactFirstName,
o.orderNumber,
od.quantityOrdered * priceEach as subtotal
from customers c
left join orders o
on c.customerNumber = o.customerNumber
left join orderdetails od
on o.orderNumber = od.orderNumber
-- group by c.contactFirstName
order by c.customerNumber
