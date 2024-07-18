import csv
import json
import fiona
from shapely.geometry import shape, Point
from shapely.validation import make_valid
from collections import defaultdict, Counter

country_data = {}
with fiona.open('TM_WORLD_BORDERS-0.3.shp') as layer:
	for feature in layer:
		country_data[ feature["properties"]["NAME"] ] = make_valid( shape( feature['geometry'] ) )
				
def get_country(lat, lon):
	pt = Point(lon, lat)
	for c,p in country_data.items():
		if p.contains(pt):
			return c
	return None
	
city = {}
badcity = defaultdict(list)
badrow = 0
h = {"name":1, "asciiname":2, "alternatenames" : 3, "latitude" : 4, "longitude":5, "cc" : 8, "population":14};
with open('cities15000.txt', 'r', encoding = 'utf-8') as datafile:
	csvreader = csv.reader(datafile, delimiter="\t");
				
	for i,row in enumerate(csvreader):			
		pop = int(row[h["population"]])						
		if pop < 1: 
			badrow += 1
			continue;		
		name = row[h["name"]]				
		asciiname = row[h["asciiname"]]				
		alternatenames = row[h["alternatenames"]]				
		lon = float(row[h["longitude"]])
		lat = float(row[h["latitude"]])
		pop = int(row[h['population']])	
		f =  {"asciiname":asciiname,
		'alternatenames':alternatenames, 
		'lon':lon, 
		'lat':lat, 
		'pop':pop
		}		
		
		if name in city or name in badcity: 
			if name in city:
				oldf = city[name]
				del city[name]
				badcity[name].append( oldf )
			badcity[name].append( f )
		else:	
			city[name] = f
		

bc = 0
for name, data in badcity.items():
	#add country tag
	unique_names = Counter()
	
	for c in data:
		country = get_country( c['lat'], c['lon'] )
		namec = name + " ({})".format(country)
		
		num = ''
		if namec in unique_names: num = " " + str(unique_names[namec])
		unique_names[namec] += 1
		
		city[namec+num] = c
		
	bc += len(badcity[name])


print(len(city), "cities")
print(len(city) + badrow, "cities")
with open("cities15000.json", 'w') as outfile: outfile.write( json.dumps(city) )					
