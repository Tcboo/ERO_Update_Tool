__author__ = 'shylander'

import csv
import geojson
import pygeoj
import shutil
import io

#open lookup table
csvfile = io.open(r"C:\Users\shylander\Desktop\ICE\app\ICE_Data\CSV\LookUp_Table.csv",'r', encoding='utf-8', errors='ignore')
#initialize reader
reader = csv.reader(csvfile)
#create dictionary from reader, includes all pairs, including matching key,pairs
lookup_dict_all = dict((rows[0],rows[1]) for rows in reader)
csvfile.close()
#create dict variable that will hold only replacement key,value pairs, remove matching key,pair values
#iterate through key,value pairs only select those with spelling variations
LookUp={}
for key,value in lookup_dict_all.iteritems():
    if key!=value:
       LookUp.update({key:value})
    else:
        pass
print "lookup table ="
print LookUp



# open template
geoj_template = pygeoj.load(r"C:\Users\shylander\Desktop\ICE\app\ICE_Data\Countries_Template.geojson")
# save copy
geoj_template.save(r"C:\Users\shylander\Desktop\ICE\app\ICE_Data\Countries.geojson")
# open copy
geoj = pygeoj.load(r"C:\Users\shylander\Desktop\ICE\app\ICE_Data\Countries.geojson")
# open csv
csvfile = io.open(r"C:\Users\shylander\Desktop\ICE\app\ICE_Data\CSV\Tabular_Data.csv",'r', encoding='utf-8', errors='ignore')
# intialize reader
reader = csv.DictReader(csvfile)
# dump the tabular data csv into a string of geojson objects
out = geojson.dumps([row for row in reader])
# convert to the geojson object into a list/array
out_list_tab = geojson.loads(out)
#close Tabular Data csv
csvfile.close()
print 'outlist ='
print out_list_tab
# convert strings to appropriate values in the out_list_tab schema
for item in out_list_tab:
    for key in item:
        if key == "Country":
            pass
        elif key=="Tab1" or key =="Tab13":
            item[key]= float(item[key])
        else:
            item[key] = int(item[key])
#switch country names in tabular data records with official spellings from lookup table
for item in out_list_tab:
    for key,value in LookUp.iteritems():
        if value ==item["Country"]:
            print "needs to switch: " + item["Country"]
            print "old value= "+item["Country"]
            item["Country"]=key
            print "new value = "+item["Country"]
        else:
            pass

#insert all tabular data records into feature properties, matches based on country names
for feature in geoj:
    print "FEATURE =" + feature.properties["COUNTRY_1"]  # each item in out_dict list[] is a small dictionary {}
    for item in out_list_tab:
        if item["Country"] == feature.properties["COUNTRY_1"]:
            # add the item entry to the feature properties
            feature.properties.update(item)
            print feature.properties
            del feature.properties["Country"]
            break
        else:
            pass
#always save changes
geoj.save(r"C:\Users\shylander\Desktop\ICE\app\ICE_Data\Countries.geojson")
print "tabular data updated"


#dump from transit data csv into a list
csvfile = io.open(r"C:\Users\shylander\Desktop\ICE\app\ICE_Data\CSV\csv1.csv",'r',encoding='utf-8', errors='ignore')
reader = csv.DictReader(csvfile)

out = geojson.dumps([row for row in reader])
out_list_from = geojson.loads(out)
csvfile.close()
print out_list_from

#switch country names in from transit data records with official spellings from lookup table
for item in out_list_from:
    for key,value in LookUp.iteritems():
        if value ==item["Country"]:
            print "needs to switch: "+ item["Country"]+ " to "+ key
            item["Country"]=key
            print "new value =" + item["Country"]
        elif value==item["from_country"]:
            print "needs to switch: "+item["from_country"]+" to "+ key
            item["from_country"]=key
            print "newvalue="+item["from_country"]
        else:
            pass

# from table into feature properties, matches based on country names
for feature in geoj:
    #create a dictionary for each feature that will hold any/all from transit data for that country; from country: from count
    transits = {}
    for item in out_list_from:
        #iterate through countries in out_dict_from and place any/all from data into properly formatted key:value pairs
        if item["Country"]==feature.properties["COUNTRY_1"]:
            transits.update({(item["from_country"].title()): int(item["from_count"])})

        else:
            pass
    #converts dictionary into list of tuplets that are arranged by descending from_count
    sorted_transits=  sorted(transits.items(), key = lambda x:x[1],reverse=True)
    #declare array/list for from country and from count data
    from_country_list=[]
    from_count_list =[]
    #iterate through ordered list of tuplets and stuff all from data into lists
    for (a,b) in sorted_transits:
        from_country_list.append(a)
        from_count_list.append(str(b))
    #convert lists to strings, insert commas between entries, no spaces
    from_country_s=','.join(from_country_list)
    from_count_s=','.join(from_count_list)
    #insert both from lists into each feature as properties
    feature.properties["from_country"]=from_country_s
    feature.properties["from_count"]=from_count_s
#save all changes
geoj.save(r"C:\Users\shylander\Desktop\ICE\app\ICE_Data\Countries.geojson")

#repeat previous step with the to transit data
csvfile = io.open(r"C:\Users\shylander\Desktop\ICE\app\ICE_Data\CSV\csv2.csv",'r',encoding='utf-8', errors='ignore')
reader = csv.DictReader(csvfile)
out = geojson.dumps([row for row in reader])
out_list_to = geojson.loads(out)
csvfile.close()

#switch country names in to transit data records with official spellings from lookup table
for item in out_list_to:
    for key,value in LookUp.iteritems():
        if value ==item["Country"]:
            print "needs to switch: "+ item["Country"]+ " to "+ key
            item["Country"]=key
            print "new value =" + item["Country"]
        elif value==item["to_country"]:
            print "needs to switch: "+item["to_country"]+" to "+ key
            item["to_country"]=key
            print "newvalue="+item["to_country"]
        else:
            pass


for feature in geoj:
    transits = {}
    for item in out_list_to:
        if item["Country"]==feature.properties["COUNTRY_1"]:
            transits.update({(item["to_country"].title()): int(item["to_count"])})
        else:
            pass
    sorted_transits=  sorted(transits.items(), key = lambda x:x[1],reverse=True)
    to_country_list=[]
    to_count_list =[]
    for (a,b) in sorted_transits:
        to_country_list.append(a)
        to_count_list.append(str(b))
    to_country_s=','.join(to_country_list)
    to_count_s=','.join(to_count_list)
    feature.properties["to_country"]=to_country_s
    feature.properties["to_count"]=to_count_s

geoj.save(r"C:\Users\shylander\Desktop\ICE\app\ICE_Data\Countries.geojson")



for feature in geoj:
    print feature.properties
#convert to javascript file extension
js=r"C:\Users\shylander\Desktop\ICE\app\ICE_DataCountries.js"
geoj.save(js)
#insert the declarative variable into the header of the js file
with open(js, "r+")as js_update:
    body = js_update.read()
    js_update.seek(0)
    js_update.write("var worldCountries = \n"+ body)
js_update.close()


#overwrite existing
shutil.copy(js,r"C:\Users\shylander\Desktop\ICE\app\eroRP-master\data\Countries.js")


