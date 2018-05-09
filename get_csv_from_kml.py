#!/usr/bin/env python
#info: 
#  read best_track kml file (download from www.nhc.noaa/gis/archive_besttrack.php
#  adn write to csv file (datetime, storm_type, lon, lat, mslp, intensity)

from datetime import datetime
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import csv


tree=ET.parse('doc.kml')
root=tree.getroot()
out_csv='doc.csv'
with open(out_csv,"w") as csvf:
    fieldnames=["datetime", "storm_type", "lon", "lat", "mslp", "intensity"]
    writer = csv.DictWriter(csvf, fieldnames=fieldnames)
    writer.writeheader()
    dct={}

    xmlns='{http://www.opengis.net/kml/2.2}'
    for folder in root.iter(xmlns+"Folder"):
        if(folder.get("id") == "FeatureLayer1"):
            for node in folder.iter(xmlns+'Placemark'):
                dt_str_pre=node.find(xmlns+'name').text
                text=node.find(xmlns+'description').text
                soup=BeautifulSoup(text, "html5lib")
                stormid=soup.find("td", text="STORM_ID").next_sibling.next_sibling.string
                year=int(stormid[-4:])
                stormtype=soup.find("td", text="STORMTYPE").next_sibling.next_sibling.string
                lat=float(soup.find("td", text="LAT").next_sibling.next_sibling.string)
                lon=float(soup.find("td", text="LON").next_sibling.next_sibling.string)
                mlsp=float(soup.find("td", text="MSLP_mb").next_sibling.next_sibling.string[0:-3])
                kt=float(soup.find("td", text="INTENSITY_kt").next_sibling.next_sibling.string[0:-3])
                dt_str=dt_str_pre+" %d"%year #e.g. 1800 UTC 26 SEP 2015
                #print(dt_str)
                dt_reformat=datetime.strptime(dt_str, "%H00 UTC %d %b %Y").strftime("%Y%m%d%H00")
                print(dt_reformat)
                dct["datetime"]=dt_reformat
                dct["storm_type"]=stormtype
                dct["lon"]=lon
                dct["lat"]=lat
                dct["mslp"]=mlsp
                dct["intensity"]=kt
                writer.writerow(dct)
            else:
                exit(0)
