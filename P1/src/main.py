import os.path

hardware = False
images = False
flavors = False

def handle_config(cmd_parts):
    global hardware
    global images
    global flavors
    if(len(cmd_parts) != 4):
        print("Invalid command. Refer to the documentation for the correct command.")
        return;
        
    if(cmd_parts[2] == "--hardware"):
        file = cmd_parts[3]
        my_file = "../config/" + file
        
        if (os.path.exists(my_file)):
            print("Hardware file exists!")
            hardware = True
        else:
            print("File you specified does not exist!")
            
    elif(cmd_parts[2] == "--images"):
        file = cmd_parts[3]
        my_file = "../config/" + file
        
        if (os.path.exists(my_file)):
            print("File exists!")
            images = True
        else:
            print("File you specified does not exist!")
            
    elif(cmd_parts[2] == "--flavors"):
        file = cmd_parts[3]
        
        my_file = "../config/" + file
        
        if (os.path.exists(my_file)):
            print("File exists!")
            flavors = True
        else:
            print("File you specified does not exist!")
            
    else:
        print("Invalid command. Refer to the documentation for the correct command.")
        

        
def handle_display(cmd_parts):
    global hardware
    global images
    global flavors
    if(len(cmd_parts) != 3):
        print("Invalid command. Refer to the documentation for the correct command.")
        return;
        
    if(cmd_parts[2] == "hardware"):
        if(hardware):
            print("Show hardware")
        else:
            print("Read hardware config first!")
            
    elif(cmd_parts[2] == "images"):
        if(images):
            print("Show images")
        else:
            print("Read images config first!")
            
    elif(cmd_parts[2] == "flavors"):
        if(flavors):
            print("Show flavors")
        else:
            print("Read flavors config first!")
            
    elif(cmd_parts[2] == "all"):
        if(hardware and images and flavors):
            print("Show all")
        else:
            print("Read all hardware, images and flavors configs first!")
            
    else:
        print("Invalid command. Refer to the documentation for the correct command.")
        

while True:
    cmd = raw_input('Enter your command: ')
    cmd_parts = cmd.split(" ")
    
    if(len(cmd_parts) <= 0 or len(cmd_parts) > 4):
        print("Invalid command. Refer to the documentation for the correct command.")
    
    if(cmd_parts[0] == "quit"):
        print("Goodbye!")
        break;
    elif(cmd_parts[0] != "aggiestack"):
        print("Invalid command. Refer to the documentation for the correct command.")
    elif(cmd_parts[1] == "config"):
        handle_config(cmd_parts)
    elif(cmd_parts[1] == "show"):
        handle_display(cmd_parts)
    else:
        print("Invalid command. Refer to the documentation for the correct command.")
    