from q_db import *

# Panda query for top two generatig employees 
top_two_employees = pd.read_sql_query('''
                                        SELECT
                                          *
                                        FROM (
                                          SELECT 
                                            O.ID AS id,
                                            O.EmployeeID AS employee_id,
                                            E.FirstName AS first_name, 
                                            E.LastName AS last_name,
                                            SUM((OD.UnitPrice - OD.Discount) * OD.quantity) AS total_dollar_sales
                                          FROM [OrderDetail] AS OD
                                          INNER JOIN [Order] AS O ON O.ID = OD.OrderID
                                          INNER JOIN [Employee] AS E ON E.ID = O.EmployeeID
                                          GROUP BY 
                                            O.EmployeeID) T
                                        ORDER BY total_dollar_sales DESC
                                        LIMIT 2
''', connection)

# Convert dataframe to suitable html table report
top_two_employees_html = HTML(top_two_employees.to_html(classes='table-responsive table table-striped table-hover'))

employees_count = pd.read_sql_query('''
                                      SELECT 
                                        O.ID AS id,
                                        O.EmployeeID AS employee_id,
                                        E.FirstName AS first_name, 
                                        E.LastName AS last_name,
                                        SUM((OD.UnitPrice - OD.Discount) * OD.quantity) AS total_dollar_sales
                                      FROM [OrderDetail] AS OD
                                      INNER JOIN [Order] AS O ON O.ID = OD.OrderID
                                      INNER JOIN [Employee] AS E ON E.ID = O.EmployeeID
                                      GROUP BY 
                                        O.EmployeeID
''', connection)