from q_db import *

# Panda query for supplier accounts for the most orders
most_supplier = pd.read_sql_query('''
                                  SELECT 
                                    supplier_id, 
                                    company_name,
                                    MAX(supplier_count) AS maximum_count
                                  FROM (
                                      SELECT 
                                        P.SupplierID AS supplier_id, 
                                        S.CompanyName AS company_name,
                                        COUNT(P.SupplierID) AS supplier_count
                                      FROM [OrderDetail] AS OD
                                      INNER JOIN [Product] AS P ON P.ID = OD.ProductID
                                      INNER JOIN [Supplier] AS S ON S.ID = P.SupplierID
                                      GROUP BY
                                        P.SupplierID
                                  )C
''', connection)

# Panda query for all order count on every supplier's account
supplier_list = pd.read_sql_query('''                           
                                  SELECT 
                                    P.SupplierID AS supplier_id, 
                                    S.CompanyName AS company_name,
                                    COUNT(P.SupplierID) AS supplier_count
                                  FROM [OrderDetail] AS OD
                                  INNER JOIN [Product] AS P ON P.ID = OD.ProductID
                                  INNER JOIN [Supplier] AS S ON S.ID = P.SupplierID
                                  GROUP BY
                                    P.SupplierID
''', connection)

# Convert dataframe to suitable html table report
most_supplier_html = HTML(most_supplier.to_html(classes='table-responsive table table-striped table-hover'))

supplier_list_html = HTML(supplier_list.to_html(classes='table-responsive table table-striped table-hover'))