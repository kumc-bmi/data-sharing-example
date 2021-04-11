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

## Setup
- On Unix or Mac `python3 -m venv venv`
- On Windows: `py -3 -m venv venv` if you are using Python 2 `$ python2 -m virtualenv venv`
- Then `pip install Flask`
- Linux:
* Debian, Ubuntu
`$ sudo apt-get install python-virtualenv`
* CentOS, Fedora
`$ sudo yum install python-virtualenv`
* Arch
`$ sudo pacman -S python-virtualenv`

## Start app:
- Kindly look at the requirement.txt for all libraries need
- For Unix or Mac users run this command `source env/bin/activate` in your terminal to activate the corresponding enviroment
- For windows users run this command `$ . venv/bin/activate` in your DOS prompt to activate the corresponding enviroment
- Then run this command `python app.py` to start app

## Alternative
- You can kindly run the `all_questions.py` in python for hardcode results

## Acknowledgements

Thank you to [jpwhite3/northwind-SQLite3](https://github.com/jpwhite3/northwind-SQLite3) for `Northwind_large.sqlite`.  See included MIT license.
