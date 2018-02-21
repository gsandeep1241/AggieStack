import redis
import time
from mongo_connect import connectMongo
import constants
import pymongo
import pprint
import sys

collection = connectMongo()
r = redis.StrictRedis(host='localhost', port=6379, db=0)

board_name = ""
subscribing = False

while True:
    try:
        
        if subscribing:
            while True:
                message = p.get_message()
                if message:
                    print "New Message: %s" % message['data']
                time.sleep(1)
        
        cmd = raw_input('Enter your command: ')
        print(cmd)
        cmd_parts = cmd.split(" ")

        if cmd_parts[0] == "select":
            if len(cmd_parts) == 1:
                print "Give a board to select!"
                continue;
            board_name = ' '.join(cmd_parts[1:])
            
        elif cmd_parts[0] == "read":
            if board_name:
                RQ0 = collection.find({"name": board_name})
                for data in RQ0:
                    pprint.pprint(data)
            else:
                print "No board selected!"
                
        elif cmd_parts[0] == "write":
            if board_name:
                if len(cmd_parts) == 1:
                    print "Write message missing."
                    continue;
                data_message = ' '.join(cmd_parts[1:])
                data = {
                    "name": board_name,
                    "message": data_message
                }
                
                r.publish(board_name, data_message)
                collection.insert(data)
            else:
                print "No board selected!" 
                
        elif cmd_parts[0] == "listen":
            if board_name:
                p = r.pubsub()
                p.subscribe(board_name)
                subscribing = True
            else:
                print "No board selected!"
            
        elif cmd_parts[0] == "quit":
            break;
            
        else:
            print "Input format wrong!"
            
    except KeyboardInterrupt:
        subscribing = False