__author__ = 'shylander'
import pygeoj
import csv
import geojson
import shutil
import io
# open template
geoj_template = pygeoj.load(r"C:\Users\shylander\Desktop\ICE\app\ICE_Data\posts_Template.geojson")
#save copy
geoj_template.save(r"C:\Users\shylander\Desktop\ICE\app\ICE_Data\posts.geojson")
#open copy
geoj = pygeoj.load(r"C:\Users\shylander\Desktop\ICE\app\ICE_Data\posts.geojson")
#open copy
# open csv
csvfile = io.open(r"C:\Users\shylander\Desktop\ICE\app\ICE_Data\CSV\Posts.csv", 'r', encoding='utf-8', errors='ignore')
# intialize reader
reader = csv.DictReader(csvfile)
# dump the tabular data csv into a string of geojson objects
out = geojson.dumps([row for row in reader])
# convert to the geojson object into a dictionary
out_list = geojson.loads(out)
#close Tabular Data csv
csvfile.close()

sep = ","

for item in out_list:
    for key in item:
        if key =="Post7":
            item[key]=str(item[key])[:-1]
            print item[key]
        elif key =="Post1":
            item[key]=str((item["Post1"]).split(sep,1)[0])
        else:
            pass



print out_list
#print geoj.common_attributes
for feature in geoj:
    print feature.properties["Office"]
    for item in out_list:
        print "x"
        if item["Post1"]==feature.properties["Office"]:
            item["Post1"]=str(item["Post1"])+ " Office"
            #print feature.properties["Office"]
            #print item["Post7"]
            feature.properties.update(item)
        else:
            print "No"
    print feature.properties


geoj.save(r"C:\Users\shylander\Desktop\ICE\app\ICE_Data\posts.geojson")

js=r"C:\Users\shylander\Desktop\ICE\app\ICE_Data\posts_Buffer.js"
geoj.save(js)

with open(js, "r+")as js_update:
    body = js_update.read()
    js_update.seek(0)
    js_update.write("var cityPoints = \n"+ body)
js_update.close()

shutil.copy(js,r"C:\Users\shylander\Desktop\ICE\app\eroRP-master\data\posts.js")
del js