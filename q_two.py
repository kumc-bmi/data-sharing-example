from q_db import *

# Panda query read for first date of customer purchase and count of subsequent purchases
return_customer = pd.read_sql_query('''
                                    SELECT
                                      CustomerID AS customer_id,
                                      COUNT(CustomerID) AS return_customer
                                    FROM (
                                        SELECT DISTINCT
                                          CustomerID, 
                                          OrderDate,
                                          MIN(OrderDate) OVER (PARTITION BY CustomerID) AS first_purchase_date
                                        FROM [Order]) C
                                      GROUP BY 
                                        CustomerID
''', connection)

# Panda query read for total count for returning customers
return_customer_count = pd.read_sql_query('''
                                          SELECT
                                            COUNT(*) AS returning_customer_count
                                          FROM (SELECT
                                              CustomerID,
                                              COUNT(CustomerID) AS return_customer
                                            FROM (SELECT DISTINCT
                                                CustomerID, 
                                                OrderDate,
                                                MIN(OrderDate) OVER (PARTITION BY CustomerID) AS first_purchase_date
                                              FROM [Order]) C
                                            GROUP BY 
                                              CustomerID) R 
                                            WHERE return_customer > 1
''', connection)

# Convert dataframe to suitable html table report
return_customer_html = HTML(return_customer.to_html(classes='table-responsive table table-striped table-hover'))

return_customer_count_html = HTML(return_customer_count.to_html(classes='table-responsive table table-striped table-hover'))