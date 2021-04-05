from q_db import *

# Panda query for address for both suppliers and customers - limited only 20 becasue address caontained bad ascii characters and need to scrubbed [Will get back to data cleanup]
data_frame = pd.read_sql_query('''
                        SELECT 
                          O.ID AS order_id, 
                          P.SupplierID AS supplier_id, 
                          O.CustomerID AS customer_id, 
                          C.Address || ', ' || C.CIty || ', ' || C.Region || ', ' || C.PostalCode || ', ' || C.Country AS shipping_address, 
                          S.Address || ', ' || S.CIty || ', ' || S.Region || ', ' || S.PostalCode || ', ' || S.Country AS supplier_address, 
                          P.ProductName AS product_name, 
                          S.CompanyName AS company_name, 
                          S.ContactName AS contact_name 
                        FROM [Order] AS O
                        INNER JOIN [OrderDetail] AS OD ON OD.OrderID = O.ID 
                        INNER JOIN [Product] AS P ON P.ID = OD.ProductID
                        INNER JOIN [Supplier] AS S ON S.ID = P.SupplierID
                        LEFT JOIN [customer] AS C ON C.ID = O.CustomerID
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
                          S.Country IS NOT NULL) AND
                          O.CustomerID IS NOT NULL
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
key = 'eed6aa95e60548efa721ab515d3a98be'
geocoder = OpenCageGeocode(key)

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
shpping_mean_customer_html = HTML(shipping_mean.to_html(classes='table-responsive table table-striped table-hover'))

shpping_list_customer_html = HTML(data_frame.head().to_html(classes='table-responsive table table-striped table-hover'))