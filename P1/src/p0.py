import os.path
import sys
from hardware import Hardware
from image import Image
from flavor import Flavor
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler("../logs/aggiestack-log.txt")
handler.setLevel(logging.INFO)

logger.addHandler(handler)

hardware = False
images = False
flavors = False

hardware_configs = {}
image_configs = {}
flavor_configs = {}

curr_command = ""

def handle_config(cmd_parts):
    global hardware, hardware_configs
    global images, image_configs
    global flavors, flavor_configs
    global curr_command
    if(len(cmd_parts) != 4):
        sys.stderr.write("ERROR: Invalid command." + "\n")
        logger.info(curr_command + ": Failure")
        return;
        
    if(cmd_parts[2] == "--hardware"):
        file = cmd_parts[3]
        my_file = "../p0_config/" + file
        
        if (os.path.exists(my_file)):

            hardware = True

            with open(my_file) as f:
                lines = f.readlines()

            num_configs = int(lines[0])

            for x in range(1, num_configs+1):
                cfg = lines[x].split(" ")
                h = Hardware(cfg[0], cfg[1], cfg[2], cfg[3], cfg[4])
                hardware_configs[cfg[0]] = h

            print len(hardware_configs), 'physical servers now available.'
            logger.info(curr_command + ": Success")

        else:
            sys.stderr.write("ERROR: File you specified does not exist." + "\n")
            logger.info(curr_command + ": Failure")
            
    elif(cmd_parts[2] == "--images"):
        file = cmd_parts[3]
        my_file = "../p0_config/" + file
        
        if (os.path.exists(my_file)):

            images = True

            with open(my_file) as f:
                lines = f.readlines()

            num_configs = int(lines[0])

            for x in range(1, num_configs+1):
                cfg = lines[x].split(" ")
                img = Image(cfg[0], cfg[1])
                image_configs[cfg[0]] = img

            print len(image_configs), 'images now available.'
            logger.info(curr_command + ": Success")

        else:
            sys.stderr.write("ERROR: File you specified does not exist." + "\n")
            logger.info(curr_command + ": Failure")
            
    elif(cmd_parts[2] == "--flavors"):
        file = cmd_parts[3]
        my_file = "../p0_config/" + file
        
        if (os.path.exists(my_file)):

            flavors = True

            with open(my_file) as f:
                lines = f.readlines()

            num_configs = int(lines[0])

            for x in range(1, num_configs+1):
                cfg = lines[x].split(' ')
                flv = Flavor(cfg[0], cfg[1], cfg[2], cfg[3])
                flavor_configs[cfg[0]] = flv

            print len(flavor_configs), 'VM flavors now available.'
            logger.info(curr_command + ": Success")
        else:
            sys.stderr.write("ERROR: File you specified does not exist." + "\n")
            logger.info(curr_command + ": Failure")
            
    else:
        sys.stderr.write("ERROR: Invalid command." + "\n")
        logger.info(curr_command + ": Failure")
        

        
def handle_display(cmd_parts, all=None):
    global hardware
    global images
    global flavors
    global curr_command
    if(len(cmd_parts) != 3):
        sys.stderr.write("ERROR: Invalid command." + "\n")
        logger.info(curr_command + ": Failure")
        return;
        
    if(cmd_parts[2] == "hardware"):
        if(hardware):
            print("Hardware configs available:")
            print("Name, IP, RAM, Num_Disks, Num_Vcpus")

            for key in hardware_configs:
                hw = hardware_configs[key]
                print hw.name, " ", hw.ip, " ", hw.mem, " ", hw.num_disks, " ", hw.num_vcpus
            if(all == None):
                logger.info(curr_command + ": Success")
        else:
            sys.stderr.write("ERROR: No physical servers available." + "\n")
            logger.info(curr_command + ": Failure")
            
    elif(cmd_parts[2] == "images"):
        if(images):
            print("Images available:")
            print("Name, Path")

            for key in image_configs:
                img = image_configs[key]
                print img.name, " : ", img.path
            if(all == None):
                logger.info(curr_command + ": Success")
        else:
            sys.stderr.write("ERROR: No images available." + "\n")
            logger.info(curr_command + ": Failure")
            
    elif(cmd_parts[2] == "flavors"):
        if(flavors):
            print("Flavors available:")
            print("Type, Ram, Disks, VCPUs")

            for key in flavor_configs:
                flv = flavor_configs[key]
                print flv.type, " ", flv.ram, " ", flv.disks, " ", flv.vcpus
            if(all == None):
                logger.info(curr_command + ": Success")
        else:
            sys.stderr.write("ERROR: No flavors available." + "\n")
            logger.info(curr_command + ": Failure")
            
    elif(cmd_parts[2] == "all"):
        if(hardware and images and flavors):

            cmd_parts[2] = "hardware"
            handle_display(cmd_parts, "all")

            cmd_parts[2] = "images"
            handle_display(cmd_parts, "all")

            cmd_parts[2] = "flavors"
            handle_display(cmd_parts, "all")

            logger.info(curr_command + ": Success")
        else:
            sys.stderr.write("ERROR: Hardware/Image/Flavor not available." + "\n")
            logger.info(curr_command + ": Failure")
            
    else:
        sys.stderr.write("ERROR: Invalid command." + "\n")
        logger.info(curr_command + ": Failure")
        
def handle_admin(cmd_parts):
    global curr_command
    if len(cmd_parts) == 4 and cmd_parts[2] == "show" and cmd_parts[3] == "hardware":
        handle_display([cmd_parts[0], cmd_parts[2], cmd_parts[3]])
    elif len(cmd_parts) == 5 and cmd_parts[2] == "can_host":
        mac_name = cmd_parts[3]
        flv = cmd_parts[4]

        if (hardware_configs.get(mac_name) == None or flavor_configs.get(flv) == None):
            sys.stderr.write("Hardware/Flavor not available" + "\n")
            logger.info(curr_command + ": Failure")
            return

        mac = hardware_configs[mac_name]
        vm = flavor_configs[flv]

        if(int(mac.mem) >= int(vm.ram) and int(mac.num_disks) >= int(vm.disks) and int(mac.num_vcpus) >= int(vm.vcpus)):
            print("Yes")
        else:
            print("No")
        logger.info(curr_command + ": Success")
    else:
        sys.stderr.write("ERROR: Invalid command." + "\n")
        logger.info(curr_command + ": Failure")

counter = 1
with open('../input-p0.txt', 'r') as f:
    for cmd in f:
        print ("Command# " + str(counter) + ":")
        counter += 1
        cmd = cmd.rstrip('\n')
        curr_command = cmd
        print cmd
        cmd_parts = cmd.split(" ")

        if(len(cmd_parts) <= 0 or len(cmd_parts) > 5):
            sys.stderr.write("ERROR: Invalid command." + "\n")
            logger.info(curr_command + ": Failure")
            print (
                "************************************************************************************************************")
            continue

        if(cmd_parts[0] != "aggiestack"):
            sys.stderr.write("ERROR: Invalid command." + "\n")
            logger.info(curr_command + ": Failure")
        elif(cmd_parts[1] == "config"):
            handle_config(cmd_parts)
        elif(cmd_parts[1] == "show"):
            handle_display(cmd_parts)
        elif(cmd_parts[1] == "admin"):
            handle_admin(cmd_parts)
        else:
            sys.stderr.write("ERROR: Invalid command." + "\n")
            logger.info(curr_command + ": Failure")
        print (
            "************************************************************************************************************")
