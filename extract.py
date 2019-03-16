import json

try:
    with open('sample.json', 'r') as fp:
        obj = json.load(fp)
        
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
