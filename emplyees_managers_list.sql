
-- Employee report to and managers using self join
use classicmodels;
select e.employeeNumber,
e.firstName,
m.firstName as Managers
from employees e 
left join employees m 
on e.reportsTo = m.employeeNumber

