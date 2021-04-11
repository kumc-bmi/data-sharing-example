from q_db import *

# Panda query for mean shipping time by Shipper from the orders table
shipper_mean_orders = pd.read_sql_query('''
                                        SELECT 
                                          O.ShipVia AS ship_id,
                                          S.CompanyName AS company_name,
                                          AVG(O.ShippedDate - O.OrderDate) AS shipping_time
                                        FROM [Order] AS O
                                        INNER JOIN [Shipper] AS S ON S.ID = O.ShipVia 
                                        GROUP BY 
                                          ShipVia
''', connection)

# Panda query for mean shipping time by Shipper from the orders details table which might be more logical
shipper_mean_order_details = pd.read_sql_query('''
                                              SELECT 
                                                O.ShipVia AS ship_id,
                                                S.CompanyName AS company_name,
                                                AVG(O.ShippedDate - O.OrderDate) AS shipping_time
                                              FROM [OrderDetail] AS OD
                                              INNER JOIN [Order] AS O ON O.ID = OD.OrderID
                                              INNER JOIN [Shipper] AS S ON S.ID = O.ShipVia 
                                              GROUP BY 
                                                ShipVia
''', connection)

# Convert dataframe to suitable html table report
shipper_mean_orders_html = HTML(shipper_mean_orders.to_html(classes='table-responsive table table-striped table-hover'))

shipper_mean_order_details_html = HTML(shipper_mean_order_details.to_html(classes='table-responsive table table-striped table-hover'))

smod = pd.read_sql_query('''
                        SELECT 
                          O.ShipVia AS ship_id,
                          S.CompanyName AS company_name,
                          AVG(O.ShippedDate - O.OrderDate) AS shipping_time
                        FROM [Order] AS O
                        INNER JOIN [Shipper] AS S ON S.ID = O.ShipVia
                        GROUP BY 
                          O.ShipAddress || ', ' || O.ShipCIty || ', ' || O.ShipRegion || ', ' || O.ShipPostalCode || ', ' || O.ShipCountry
                                        
''', connection)

smod_count = pd.read_sql_query('''
                        SELECT COUNT(*) AS count
                        FROM( SELECT 
                            O.ShipVia AS ship_id,
                            S.CompanyName AS company_name,
                            AVG(O.ShippedDate - O.OrderDate) AS shipping_time
                          FROM [Order] AS O
                          INNER JOIN [Shipper] AS S ON S.ID = O.ShipVia
                          GROUP BY 
                            O.ShipAddress || ', ' || O.ShipCIty || ', ' || O.ShipRegion || ', ' || O.ShipPostalCode || ', ' || O.ShipCountry)C
                                        
''', connection)
