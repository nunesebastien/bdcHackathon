import base64
import json
import os
import ssl
import sys

filename = sys.argv[1]
city_name = sys.argv[2]

try:
    import httplib  # Python 2
except:
    import http.client as httplib  # Python 3

headers = {"Content-type": "application/json",
           "X-Access-Token": "1pA3tbRowNsoFQTUW2r3RoRROOE7diux7E3S"}
conn = httplib.HTTPSConnection("dev.sighthoundapi.com", 
       context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))

# To use a hosted image uncomment the following line and update the URL
# image_data = "https://en.wikipedia.org/wiki/Category:Images_of_cars#/media/File:Red_2007_gtcs_front.jpg"

# To use a local file uncomment the following line and update the path
image_data = base64.b64encode(open(filename, "rb").read()).decode()

params = json.dumps({"image": image_data})
conn.request("POST", "/v1/recognition?objectType=vehicle", params, headers
            )
response = conn.getresponse()
result = response.read()
json_out = result.decode("utf-8")
    
# print(json_out)

try:
        obj = json.loads(json_out)
        
        #get make
        make = obj["objects"][0]["vehicleAnnotation"]["attributes"]["system"]["make"]["name"]
        
        #get model 
        model = obj["objects"][0]["vehicleAnnotation"]["attributes"]["system"]["model"]["name"]
        
        #get color
        color = obj["objects"][0]["vehicleAnnotation"]["attributes"]["system"]["color"]["name"]
        
        #print(obj)
        print(make)
        print(model)
        print(color)
except ValueError:
    print ("error loading JSON")


import pymysql.cursors
import pymysql

connection = pymysql.connect(host='hackathon-db.bdc.n360.io',
                             user='events',
                             password='Hack@th0n2019',
                             db='db',
                             charset='utf8mb4',
                             database='hackathon',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = """ SELECT car_ext_photo_url3 AS image,car_inventory.inventory_id, car_id, inventory_make, inventory_model, price, car_year, fuel, car_status, organization_name, address, phone
							FROM
							(
								(SELECT inventory_id, dealers.organization_unit_id, organization_name, address, phone
								FROM
									(SELECT * 
									FROM organization_unit
									WHERE city = %s) dealers
									INNER JOIN
									(SELECT *
									FROM organization_unit_inventory ) inventories
									ON dealers.organization_unit_id = inventories.organization_unit_id
									) local_dealers
							    INNER JOIN
									(SELECT * 
									FROM car_inventory) car_inventory
							    ON car_inventory.inventory_id = local_dealers.inventory_id
							)
							WHERE car_status = 'FOR_SALE' AND inventory_make = %s AND inventory_model = %s;
							"""
        
        cursor.execute(sql, (city_name, make, model))
        result = cursor.fetchall()
        print(result)

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

finally:
    connection.close()

