from q_db import *

# Panda query read for most popular product by country
product = pd.read_sql_query('''
                            SELECT 
                              country,
                              most_popular,
                              MAX(product_count) AS product_count
                            FROM (
                                SELECT 
                                  O.ShipCountry AS country, 
                                  P.ProductName AS most_popular, 
                                  COUNT(OD.ProductID) AS product_count
                                FROM [Order] AS O 
                                INNER JOIN [OrderDetail] AS OD ON OD.OrderID = O.ID
                                INNER JOIN [Product] AS P ON P.ID = OD.ProductID
                                GROUP BY 
                                  O.ShipCountry,
                                  OD.ProductID
                            ) C
                            GROUP BY 
                              country
''', connection)

# Convert dataframe to suitable html table report
most_popular_html = HTML(product.to_html(classes='table-responsive table table-striped table-hover'))