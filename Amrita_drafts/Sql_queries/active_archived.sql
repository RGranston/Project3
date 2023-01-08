-- Active/Archived status
use classicmodels;
SELECT 
orderNumber,
orderDate,
'Active' as Status
from orders
where orderDate >= '2005-01-01'
union
SELECT 
orderNumber,
orderDate,
'Archived' as Status
from orders
where orderDate < '2005-01-01'