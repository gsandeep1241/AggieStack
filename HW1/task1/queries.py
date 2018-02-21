from mongo_connect import connectMongo
import constants
import pymongo
import json
import pprint


collection = connectMongo()

##### FIND ALL ENTRIES IN THE DATABASE #####
# Assuming RQ0 is the query to find all entries in the database
RQ0 = collection.find()
for data in RQ0:
	pprint.pprint(data)
print("\n\n\n\n")   
    
    
############################ WQ1
load_data = []
with open('dummy-fitness.json') as json_data:
    load_data = json.load(json_data)

for entry in load_data:
    collection.insert(entry)
    
RQ0 = collection.find()
print "WQ1: Data upload: "
for data in RQ0:
    pprint.pprint(data)
print("\n\n\n\n")    
    
    
############################ WQ2
with open('user1001-new.json') as json_data:
    update_data = json.load(json_data)

WQ2 = collection.update({"uid" : 1001}, {"$set" : update_data})
RQ0 = collection.find({"uid" : 1001})
print "WQ2: Updated user 1001:"
for data in RQ0:    
    pprint.pprint(data)
print("\n\n\n\n") 



############################# RQ1
RQ1 = collection.count()
print "RQ1: Count: "
pprint.pprint(RQ1)
print("\n\n\n\n")




############################ RQ2
RQ2 = collection.find({"tags" : {"$in": ["active"]}})
print "RQ2: Active users: "
for data in RQ2:
    pprint.pprint(data)
    

print("\n\n\n\n")




############################ RQ3
RQ3 = collection.find({"goal.stepGoal" : {"$gt": 5000}})
print "RQ3: Users with step goal > 5000: "
for data in RQ3:
    pprint.pprint(data)

print("\n\n\n\n") 



############################ RQ4
RQ4 = collection.aggregate([
        {
            "$project": {
                "uid": "$uid",
                "totalDuration": {"$sum": "$activityDuration"}
            }
        }
    ])

print "RQ4: Aggregate Activity duration for the users: "
for data in RQ4:
    pprint.pprint(data)

    
    
    
#############################END    



######## FIND ENTRIES WITH CONDITION #######
######## collection.find(CONDITION) #######
######## E.g., collection.find({"Name" : "Alice"}) #######

######## UPDATE ENTRIES WITH CONDITION ########
######## collection.update_one(CONDITION, _update_) #######
######## collection.update_many(CONDITION, _update_)
######## E.g., collection.find({"Name" : "Alice"}, {"$inc" : {"age" : 1} })

######## DELETE ENTRIES WITH CONDITION ########
######## collection.delete_one(CONDITION) #######
######## collection.delete_many(CONDITION)
######## E.g., collection.find({"Name" : "Alice"})

######## AGGREGATE ENTRIES WITH PIPELINE ########
######## collection.aggregate(PIPELINE) ########

