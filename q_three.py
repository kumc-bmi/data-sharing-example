from q_db import *

# multiple sales based on order (an orderid can have multiple sales in it)
sales_by_order_id = pd.read_sql_query('''
                                    SELECT 
                                      strftime('%Y', O.OrderDate) AS year, 
                                      SUM(OD.quantity) AS total_sales  
                                    FROM [Order]  AS O
                                    INNER JOIN [OrderDetail] AS OD ON OD.OrderID = O.ID  
                                    GROUP BY 
                                      strftime('%Y', O.OrderDate)
                                    ORDER BY 
                                      OrderDate ASC
''', connection)

#sales by dollar
sales_by_dollar = pd.read_sql_query('''
                                          SELECT 
                                            strftime('%Y', O.OrderDate) AS year, 
                                            SUM((OD.UnitPrice - OD.Discount) * OD.quantity) AS total_dollar_sales  
                                          FROM [Order] AS O
                                          INNER JOIN [OrderDetail] AS OD ON OD.OrderID = O.ID 
                                          GROUP BY 
                                            strftime('%Y', O.OrderDate)
                                          ORDER BY 
                                            O.OrderDate ASC
''', connection)

# Convert dataframe to suitable html table report
sales_by_order_id_html = HTML(sales_by_order_id.to_html(classes='table-responsive table table-striped table-hover'))

sales_by_dollar_html = HTML(sales_by_dollar.to_html(classes='table-responsive table table-striped table-hover'))