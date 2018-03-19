import os.path

def handle_config(cmd_parts):
    if(len(cmd_parts) != 4):
        print("Invalid command. Refer to the documentation for the correct command.")
        
    if(cmd_parts[2] == "--hardware"):
        file = cmd_parts[3]
        my_file = "../config/" + file
        
        if (os.path.exists(my_file)):
            print("File exists!")
        else:
            print("File you specified does not exist!")
            
    elif(cmd_parts[2] == "--images"):
        file = cmd_parts[3]
        my_file = "../config/" + file
        
        if (os.path.exists(my_file)):
            print("File exists!")
        else:
            print("File you specified does not exist!")
            
    elif(cmd_parts[2] == "--flavors"):
        file = cmd_parts[3]
        
        my_file = "../config/" + file
        
        if (os.path.exists(my_file)):
            print("File exists!")
        else:
            print("File you specified does not exist!")
            
    else:
        print("Invalid command. Refer to the documentation for the correct command.")
        

def handle_display(cmd_parts):
    if(len(cmd_parts) != 3):
        #error
        print("Goodbye!")
    if(cmd_parts[2] == "hardware"):
        #handle1
        print("Handle 1!")
    elif(cmd_parts[2] == "images"):
        #handle2
        print("Handle 2!")
    elif(cmd_parts[2] == "flavors"):
        #handle3
        print("Handle 3!")
    elif(cmd_parts[2] == "all"):
        #handle4
        print("Handle 4!")
    else:
        #handle_error
        print("Handle Error!")

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
    