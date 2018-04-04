import os.path
from hardware import Hardware
from image import Image
from flavor import Flavor

hardware = False
images = False
flavors = False

hardware_configs = []
image_configs = []
flavor_comfigs = []

def handle_config(cmd_parts):
    global hardware, hardware_configs
    global images, image_configs
    global flavors, flavor_comfigs
    if(len(cmd_parts) != 4):
        print("Invalid command. Refer to the documentation for the correct command.")
        return;
        
    if(cmd_parts[2] == "--hardware"):
        file = cmd_parts[3]
        my_file = "../config/" + file
        
        if (os.path.exists(my_file)):

            if hardware:
                print("Hardware config is already loaded.")
                return;

            hardware = True

            with open(my_file) as f:
                lines = f.readlines()

            num_configs = int(lines[0])

            for x in range(1, num_configs+1):
                cfg = lines[x].split(" ")
                h = Hardware(cfg[0], cfg[1], cfg[2], cfg[3], cfg[4])
                hardware_configs.append(h)

            print len(hardware_configs), 'hardware configs loaded.'

        else:
            print("File you specified does not exist!")
            
    elif(cmd_parts[2] == "--images"):
        file = cmd_parts[3]
        my_file = "../config/" + file
        
        if (os.path.exists(my_file)):

            if images:
                print("Images config already loaded.")
                return;

            images = True

            with open(my_file) as f:
                lines = f.readlines()

            num_configs = int(lines[0])

            for x in range(1, num_configs+1):
                cfg = lines[x].split(" ")
                img = Image(cfg[0], cfg[1])
                image_configs.append(img)

            print len(image_configs), 'image configs loaded.'

        else:
            print("File you specified does not exist!")
            
    elif(cmd_parts[2] == "--flavors"):
        file = cmd_parts[3]
        my_file = "../config/" + file
        
        if (os.path.exists(my_file)):

            if flavors:
                print("Flavors config already loaded.")
                return;

            flavors = True

            with open(my_file) as f:
                lines = f.readlines()

            num_configs = int(lines[0])

            for x in range(1, num_configs+1):
                cfg = lines[x].split(' ')
                flv = Flavor(cfg[0], cfg[1], cfg[2])
                flavor_comfigs.append(flv)

            print len(flavor_comfigs), 'flavor configs loaded.'
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
            print("Hardware configs available:")
            print("Name, IP, RAM, Num_Disks, Num_Vcpus")

            for hw in hardware_configs:
                print hw.name, " ", hw.ip, " ", hw.mem, " ", hw.num_disks, " ", hw.num_vcpus
        else:
            print("Read hardware config first!")
            
    elif(cmd_parts[2] == "images"):
        if(images):
            print("Images available:")
            print("Name, Path")

            for img in image_configs:
                print img.name, " : ", img.path
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
    