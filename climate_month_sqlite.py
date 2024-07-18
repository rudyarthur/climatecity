import xarray as xr
import json
import numpy as np
import sys
import sqlite3
import datetime
import sys
            
with open("cities15000.json", 'r') as infile: city = json.loads(infile.read())

year_min = 2030
year_max = 2101
year_step = 10


conn = sqlite3.connect("city_temp.db")
c = conn.cursor()

city_table = '''CREATE TABLE city_name (
			name TEXT COLLATE NOCASE,
			lat_id INTEGER,
			lon_id INTEGER,
			lat REAL,
			lon REAL,
			pop INTEGER
)'''
c.execute(city_table)
conn.commit()


lat_lon_pairs = set()	
for name in city:
	d = {"name":name, "lat_id":int( float( city[name]['lat'] ) )+90, "lon_id":int( float( city[name]['lon'] ) )+180, "lat":float(city[name]['lat']), "lon":float(city[name]['lon']), 'pop':int(city[name]['pop'])}
	c.execute("INSERT INTO city_name VALUES (:name, :lat_id, :lon_id, :lat, :lon, :pop)", d)
	lat_lon_pairs.add( (d["lat_id"], d["lon_id"]) )
conn.commit()


for ssp in ['ssp585', 'ssp370', 'ssp245', 'ssp126']: 

	block_table = "CREATE TABLE city_block_tx_CMIP6_{} (".format(ssp)
	for y in range(year_min,year_max,year_step):
		year = str(y)
		for m in ['01','02','03','04','05','06','07','08','09','10','11','12']:
			block_table += "median_{}_{} REAL,\n".format(y, m)
			block_table += "percentile_90_{}_{} REAL,\n".format(y, m)
			block_table += "percentile_10_{}_{} REAL,\n".format(y, m)


	block_table +=	 '''lat_id INTEGER,
	lon_id INTEGER)'''

	c.execute(block_table)
	conn.commit()



				
	#https://cds.climate.copernicus.eu/cdsapp#!/dataset/projections-climate-atlas?tab=form	
	dset = xr.open_dataset("tx_CMIP6_{}_mon_201501-210012.nc".format(ssp) )
	"""
	<xarray.DataArray 'tx' (member: 27, time: 1032, lat: 180, lon: 360)>
	[1805587200 values with dtype=float32]
	Coordinates:
	  * lat              (lat) float64 -89.5 -88.5 -87.5 -86.5 ... 87.5 88.5 89.5
	  * lon              (lon) float64 -179.5 -178.5 -177.5 ... 177.5 178.5 179.5
	  * time             (time) datetime64[ns] 2015-01-01 2015-02-01 ... 2100-12-01
	"""


	for lat in range(-90,90):
		for lon in range(-180,180):
			lat_id = lat+90
			lon_id = lon+180
			if (lat_id, lon_id) not in lat_lon_pairs: continue
			latc = lat + 0.5
			lonc = lon + 0.5
					
			data = dset['tx'].sel({'lat':latc, 'lon':lonc}).data
			#tdata = dset['tx'].sel(time="20300501").data[:, lon_id, lat_id]


			ins = "INSERT INTO city_block_tx_CMIP6_{} VALUES (".format(ssp)
			dummy = {}
			for y in range(year_min,year_max,year_step):
				year = str(y)
				for m,mon in enumerate(['01','02','03','04','05','06','07','08','09','10','11','12']):
					date = year + mon + '01'
					t = data[:,(y-2015)*12 + m]
											
					ins += ":median_{}_{}, ".format(y, mon)
					ins += ":percentile_90_{}_{}, ".format(y, mon)
					ins += ":percentile_10_{}_{}, ".format(y, mon)
					dummy["median_{}_{}".format(y, mon)] = float(np.median(t))
					dummy["percentile_90_{}_{}".format(y, mon)] = float(np.percentile(t,90))
					dummy["percentile_10_{}_{}".format(y, mon)] = float(np.percentile(t,10))
			ins += ":lat_id, :lon_id)"
			dummy["lat_id"] = lat_id
			dummy["lon_id"] = lon_id
			c.execute(ins, dummy)

			print(ssp, lat_id, lon_id)
			
		conn.commit()	
conn.close()
