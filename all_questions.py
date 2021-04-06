from q_db import *

# method to make sure unit test is functional
def cuboid(args):
  if type(args) not in [int, float]:
    raise TypeError("The length of cuboid can only be a valid integer or a float")
  return (args * args * args)

# Question 1
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
HTML(product.to_html(classes='table-responsive table table-striped table-hover'))

# Question 2
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
HTML(return_customer.to_html(classes='table-responsive table table-striped table-hover'))

HTML(return_customer_count.to_html(classes='table-responsive table table-striped table-hover'))


# Question 3
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
HTML(sales_by_order_id.to_html(classes='table-responsive table table-striped table-hover'))

HTML(sales_by_dollar.to_html(classes='table-responsive table table-striped table-hover'))

# Question 4
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
HTML(shipper_mean_orders.to_html(classes='table-responsive table table-striped table-hover'))

HTML(shipper_mean_order_details.to_html(classes='table-responsive table table-striped table-hover'))

# Question 5
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
HTML(top_two_employees.to_html(classes='table-responsive table table-striped table-hover'))

# Question 6
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
HTML(most_supplier.to_html(classes='table-responsive table table-striped table-hover'))

HTML(supplier_list.to_html(classes='table-responsive table table-striped table-hover'))


# Question 7
# Panda query for address for both suppliers and customers - limited only 20 becasue address caontained bad ascii characters and need to scrubbed [Will get back to data cleanup]
data_frame = pd.read_sql_query('''
                        SELECT 
                          O.ID AS order_id, 
                          P.SupplierID AS supplier_id, 
                          O.CustomerID AS customer_id, 
                          O.ShipAddress || ', ' || O.ShipCIty || ', ' || O.ShipRegion || ', ' || O.ShipPostalCode || ', ' || O.ShipCountry AS shipping_address, 
                          S.Address || ', ' || S.CIty || ', ' || S.Region || ', ' || S.PostalCode || ', ' || S.Country AS supplier_address, 
                          P.ProductName AS product_name, 
                          S.CompanyName AS company_name, 
                          S.ContactName AS contact_name 
                        FROM [Order] AS O
                        INNER JOIN [OrderDetail] AS OD ON OD.OrderID = O.ID 
                        INNER JOIN [Product] AS P ON P.ID = OD.ProductID
                        INNER JOIN [Supplier] AS S ON S.ID = P.SupplierID
                        WHERE
                          (O.ShipAddress IS NOT NULL AND 
                          O.ShipCIty IS NOT NULL AND 
                          O.ShipRegion IS NOT NULL AND
                          O.ShipPostalCode IS NOT NULL AND
                          O.ShipCountry IS NOT NULL) AND
                          (S.Address IS NOT NULL AND
                          S.CIty IS NOT NULL AND
                          S.Region IS NOT NULL AND
                          S.PostalCode IS NOT NULL AND
                          S.Country IS NOT NULL)
                        GROUP BY 
                          O.ID, 
                          P.SupplierID
                        LIMIT 10
''', connection)

# convert customer shipping address to list
data_frame_shipping_list = data_frame['shipping_address'].tolist()

# convert supplier shipping address to list
data_frame_supplier_list = data_frame['supplier_address'].tolist()

# create empty list for customer and supplier latitude shipping addresses
shipping_lat = []
supplier_lat = []


# create empty list for customer and supplier longitutude shipping addresses
supplier_long = []
shipping_long = []

# create empty list for distance calculation
distance_lat = []

# OpenCage API key - Great company with great expertise on location mapping
geocoder = OpenCageGeocode(opencage_api_key)

# for loop to iterate over customer list of addresses
for shipping_address in data_frame_shipping_list:
    results = geocoder.geocode(shipping_address)
    ship_lat = results[0]['geometry']['lat']
    ship_long = results[0]['geometry']['lng']

    shipping_lat.append(ship_lat)
    shipping_long.append(ship_long)

# for loop to iterate over supplier list of addresses
for supplier_address in data_frame_supplier_list:
    results = geocoder.geocode(supplier_address)
    supply_lat = results[0]['geometry']['lat']
    supply_long = results[0]['geometry']['lng']

    supplier_lat.append(supply_lat)
    supplier_long.append(supply_long)

# create new columns for latitude and longitude in dataframe
data_frame['ship_lat'] = shipping_lat
data_frame['ship_long'] = shipping_long
data_frame['supply_lat'] = supplier_lat
data_frame['supply_long'] = supplier_long


# create list of array for corresponding latitude and logitude coordinates 
supplier_location = data_frame[['supply_lat', 'supply_long']]
shipping_location = data_frame[['ship_lat', 'ship_long']]


# use numpy to make sure array list are values
supplier_array = supplier_location.to_numpy()
shipping_arrary = shipping_location.to_numpy()

# create tuple and calculate the distance of latitude and longitude of corresponding customer and supplier shipping address in dataframe
for supplier_address in data_frame_supplier_list:
  for lat, long  in zip(supplier_array, shipping_arrary):
      distance = math.sqrt( ((lat[0]-long[0])**2)+((lat[1]-long[1])**2) )
      # create a column for distance and append to dataframe
      distance_lat.append(distance)

# use panda series to make sure distance value is right datatype
data_frame['distance'] = pd.Series(distance_lat)

# calculate the mean for distance and groupby supplier address
shipping_mean = data_frame.groupby(['supplier_id', 'supplier_address'], as_index=False)['distance'].mean()

# Convert dataframe to suitable html table report
HTML(shipping_mean.to_html(classes='table-responsive table table-striped table-hover'))

shpping_list_html = HTML(data_frame.head().to_html(classes='table-responsive table table-striped table-hover'))

