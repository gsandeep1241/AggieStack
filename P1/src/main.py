while True:
    cmd = raw_input('Enter your command: ')
    cmd_parts = cmd.split(" ")
    
    if cmd_parts[0] == "quit":
        print("Goodbye!")
        break;
        
        
def handle_config(cmd_parts):
    if(len(cmd_parts) != 4):
        #error
        print("Goodbye!")
    if(cmd_parts[2] == "--hardware"):
        #handle1
        print("Handle 1!")
    elif(cmd_parts[2] == "--images"):
        #handle2
        print("Handle 2!")
    elif(cmd_parts[2] == "--flavors"):
        #handle3
        print("Handle 3!")
    else:
        #handle_error
        print("Handle Error!")
        

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