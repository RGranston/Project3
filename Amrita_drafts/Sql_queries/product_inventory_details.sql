use classicmodels;
-- Inventory status as per product lines
select
p.productName,
p.productVendor,
p.quantityInStock,
p.buyPrice,
pl.productLine

from products p
join productlines pl
on p.productLine = pl.productLine
order by pl.productLine
