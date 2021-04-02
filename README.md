# data-sharing-example

The sqlite3 database `Northwind_large.sqlite` contains the following tables:

```
Category              EmployeeTerritory     Region              
Customer              Order                 Shipper             
CustomerCustomerDemo  OrderDetail           Supplier            
CustomerDemographic   Product               Territory           
Employee              ProductDetails_V
```

## Tasks:

Please write in python ( or similar ) code which interacts with the provided sqlite database and generates a report to answer the following questions.  When done, make a pull request to this repository.

- For each country, what products are most popular?
- How many customers are return shoppers?
- Provide the number of sales for each year.
- What is the mean shipping time by `Shipper`?
- What 2 employees generate the most revenue?
- What supplier accounts for the most orders?
- (hard) What is the mean shipping distance from a `Supplier's` warehouse to the customer?
- ( open-ended ) What logistics improvements could help this company improve its operations; how does the data support this?
- ( open-ended ) What, if any, are some interesting findings within the data?

## Acknowledgements

Thank you to [jpwhite3/northwind-SQLite3](https://github.com/jpwhite3/northwind-SQLite3) for `Northwind_large.sqlite`.  See included MIT license.
