import os.path
from new_hardware import NewHardware
from new_image import NewImage
from rack import Rack
from flavor import Flavor
from instance import Instance
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

hardware_configs_fixed = {}
image_configs_fixed = {}
flavor_configs_fixed = {}

racks = {}
instances = {}
instance_on_server = {}

curr_command = ""


def handle_config(cmd_parts):
    global hardware, hardware_configs
    global images, image_configs
    global flavors, flavor_configs
    global curr_command
    if (len(cmd_parts) != 4):
        print("Invalid command. Refer to the documentation for the correct command.")
        logger.info(curr_command + ": Failure")
        return;

    if (cmd_parts[2] == "--hardware"):
        file = cmd_parts[3]
        my_file = "../p1_config/" + file

        if (os.path.exists(my_file)):

            hardware_configs = {}
            hardware = True

            with open(my_file) as f:
                lines = f.readlines()

            num_racks = int(lines[0])

            for x in range(1, num_racks+1):
                rack = lines[x].split(" ")
                r = Rack(rack[0], rack[1])
                racks[rack[0]] = r

            num_configs = int(lines[num_racks+1])

            for x in range(num_racks+2, num_racks+num_configs + 2):
                cfg = lines[x].split(" ")
                h = NewHardware(cfg[0], cfg[1], cfg[2], cfg[3], cfg[4], cfg[5])
                hf = NewHardware(cfg[0], cfg[1], cfg[2], cfg[3], cfg[4], cfg[5])
                hardware_configs[cfg[0]] = h
                hardware_configs_fixed[cfg[0]] = hf

            print len(hardware_configs), 'hardware configs loaded.'
            logger.info(curr_command + ": Success")

        else:
            print("File you specified does not exist!")
            logger.info(curr_command + ": Failure")

    elif (cmd_parts[2] == "--images"):
        file = cmd_parts[3]
        my_file = "../p1_config/" + file

        if (os.path.exists(my_file)):

            image_configs = {}
            images = True

            with open(my_file) as f:
                lines = f.readlines()

            num_configs = int(lines[0])

            for x in range(1, num_configs + 1):
                cfg = lines[x].split(" ")
                img = NewImage(cfg[0], cfg[1], cfg[2])
                imgf = NewImage(cfg[0], cfg[1], cfg[2])
                image_configs[cfg[0]] = img
                image_configs_fixed[cfg[0]] = imgf

            print len(image_configs), 'image configs loaded.'
            logger.info(curr_command + ": Success")

        else:
            print("File you specified does not exist!")
            logger.info(curr_command + ": Failure")

    elif (cmd_parts[2] == "--flavors"):
        file = cmd_parts[3]
        my_file = "../p1_config/" + file

        if (os.path.exists(my_file)):

            flavor_configs = {}
            flavors = True

            with open(my_file) as f:
                lines = f.readlines()

            num_configs = int(lines[0])

            for x in range(1, num_configs + 1):
                cfg = lines[x].split(' ')
                flv = Flavor(cfg[0], cfg[1], cfg[2], cfg[3])
                flvf = Flavor(cfg[0], cfg[1], cfg[2], cfg[3])
                flavor_configs[cfg[0]] = flv
                flavor_configs_fixed[cfg[0]] = flvf

            print len(flavor_configs), 'flavor configs loaded.'
            logger.info(curr_command + ": Success")
        else:
            print("File you specified does not exist!")
            logger.info(curr_command + ": Failure")

    else:
        print("Invalid command. Refer to the documentation for the correct command.")
        logger.info(curr_command + ": Failure")


def handle_display(cmd_parts, all=None):
    global hardware
    global images
    global flavors
    global curr_command
    if (len(cmd_parts) != 3):
        print("Invalid command. Refer to the documentation for the correct command.")
        logger.info(curr_command + ": Failure")
        return;

    if (cmd_parts[2] == "hardware"):
        if (hardware):
            print("Hardware configs available:")
            print("Name, Rack, IP, RAM, Num_Disks, Num_Vcpus")

            for key in hardware_configs_fixed:
                hw = hardware_configs_fixed[key]
                print hw.name, " ", hw.rack, " ", hw.ip, " ", hw.mem, " ", hw.num_disks, " ", hw.num_vcpus
            if (all == None):
                logger.info(curr_command + ": Success")
        else:
            print("Read hardware config first!")
            logger.info(curr_command + ": Failure")

    elif (cmd_parts[2] == "images"):
        if (images):
            print("Images available:")
            print("Name, Size, Path")

            for key in image_configs_fixed:
                img = image_configs_fixed[key]
                print img.name, " ", img.size, " ", img.path
            if (all == None):
                logger.info(curr_command + ": Success")
        else:
            print("Read images config first!")
            logger.info(curr_command + ": Failure")

    elif (cmd_parts[2] == "flavors"):
        if (flavors):
            print("Flavors available:")
            print("Type, Ram, Disks, VCPUs")

            for key in flavor_configs_fixed:
                flv = flavor_configs_fixed[key]
                print flv.type, " ", flv.ram, " ", flv.disks, " ", flv.vcpus
            if (all == None):
                logger.info(curr_command + ": Success")
        else:
            print("Read flavors config first!")
            logger.info(curr_command + ": Failure")

    elif (cmd_parts[2] == "all"):
        if (hardware and images and flavors):

            cmd_parts[2] = "hardware"
            handle_display(cmd_parts, "all")

            cmd_parts[2] = "images"
            handle_display(cmd_parts, "all")

            cmd_parts[2] = "flavors"
            handle_display(cmd_parts, "all")

            logger.info(curr_command + ": Success")
        else:
            print("Read hardware, image and flavor configs first.")
            logger.info(curr_command + ": Failure")

    else:
        print("Invalid command. Refer to the documentation for the correct command.")
        logger.info(curr_command + ": Failure")


def handle_admin(cmd_parts):
    global curr_command
    if len(cmd_parts) == 4 and cmd_parts[2] == "show" and cmd_parts[3] == "hardware":
        handle_display([cmd_parts[0], cmd_parts[2], cmd_parts[3]])
    elif len(cmd_parts) == 5 and cmd_parts[2] == "can_host":
        mac_name = cmd_parts[3]
        flv = cmd_parts[4]

        if (hardware_configs.get(mac_name) == None or flavor_configs.get(flv) == None):
            print("Specified Hardware or Flavor does not exist.")
            logger.info(curr_command + ": Failure")
            return

        mac = hardware_configs[mac_name]
        vm = flavor_configs[flv]

        if (int(mac.mem) >= int(vm.ram) and int(mac.num_disks) >= int(vm.disks) and int(mac.num_vcpus) >= int(
                vm.vcpus)):
            print("Yes")
        else:
            print("No")
        logger.info(curr_command + ": Success")
    else:
        print("Invalid command. Refer to the documentation for the correct command.")
        logger.info(curr_command + ": Failure")

def can_host(mac, vm):
    if (int(mac.mem) >= int(vm.ram) and int(mac.num_disks) >= int(vm.disks) and int(mac.num_vcpus) >= int(
            vm.vcpus)):
        return True
    else:
        return False

def handle_server(cmd_parts):
    global curr_command
    if(not (hardware and images and flavors)):
        print("First load hardware, images and flavors.")
        logger.info(curr_command + ": Failure")
        return

    if(len(cmd_parts) <= 2):
        print("Invalid command. Refer to the documentation for the correct command.")
        logger.info(curr_command + ": Failure")
        return

    if cmd_parts[2] == "list" and len(cmd_parts) == 3:
        print("Handle this.")

        if len(instances) == 0:
            print("No instances present!")
            logger.info(curr_command + ": Success")
            return

        print "Name", "Image", "Flavor"
        for key in instances:
            print instances[key].name, " ", instances[key].image, " ", instances[key].flavor

        logger.info(curr_command + ": Success")
        return

    elif cmd_parts[2] == "delete" and len(cmd_parts) == 4:

        if instances.get(cmd_parts[3]) == None:
            print("Instance does not exist")
            logger.info(curr_command + ": Failure")
            return

        flv = flavor_configs[instances[cmd_parts[3]].flavor]
        mac = hardware_configs[instance_on_server[cmd_parts[3]]]

        mac.mem = int(mac.mem) + int(flv.ram)
        mac.num_disks = int(mac.num_disks) + int(flv.disks)
        mac.num_vcpus = int(mac.num_vcpus) + int(flv.vcpus)

        del instances[cmd_parts[3]]
        del instance_on_server[cmd_parts[3]]

        print("Successfully deleted instance.")
        logger.info(curr_command + ": Success")
        return

    elif len(cmd_parts) == 8 and cmd_parts[2] == "create" and cmd_parts[3] == "--image" and cmd_parts[5] == "--flavor":

        img = cmd_parts[4]
        flv = cmd_parts[6]
        if image_configs.get(img) == None:
            print("Image specified is not available.")
            logger.info(curr_command + ": Failure")
            return

        if flavor_configs.get(flv) == None:
            print("Flavor specified is not available.")
            logger.info(curr_command + ": Failure")
            return

        if instances.get(cmd_parts[7]) != None:
            print("Use a different instance name.")
            logger.info(curr_command + ": Failure")
            return

        for key in hardware_configs:
            if (can_host(hardware_configs[key], flavor_configs[flv])):

                curr_mac = hardware_configs[key]
                curr_flv = flavor_configs[flv]

                curr_mac.mem = int(curr_mac.mem) - int(curr_flv.ram)
                curr_mac.num_disks = int(curr_mac.num_disks) - int(curr_flv.disks)
                curr_mac.num_vcpus = int(curr_mac.num_vcpus) - int(curr_flv.vcpus)

                inst = Instance(cmd_parts[7], cmd_parts[4], cmd_parts[6])
                instances[cmd_parts[7]] = inst

                instance_on_server[cmd_parts[7]] = key

                print("Successfully created an instance.")
                logger.info(curr_command + ": Success")
                return

        print("Resources unavailable!")
        logger.info(curr_command + ": Failure")
        return

    else:
        print("Invalid command. Refer to the documentation for the correct command.")
        logger.info(curr_command + " : Failure")


while True:
    cmd = raw_input('Enter your command: ')
    curr_command = cmd
    cmd_parts = cmd.split(" ")

    if (len(cmd_parts) <= 0):
        print("Invalid command. Refer to the documentation for the correct command.")
        logger.info(curr_command + ": Failure")

    if (cmd_parts[0] == "quit"):
        print("Goodbye!")
        logger.info(curr_command + ": Success")
        break;
    elif (cmd_parts[0] != "aggiestack"):
        print("Invalid command. Refer to the documentation for the correct command.")
        logger.info(curr_command + ": Failure")
    elif (cmd_parts[1] == "config"):
        handle_config(cmd_parts)
    elif (cmd_parts[1] == "show"):
        handle_display(cmd_parts)
    elif (cmd_parts[1] == "server"):
        handle_server(cmd_parts)
    elif (cmd_parts[1] == "admin"):
        handle_admin(cmd_parts)
    else:
        print("Invalid command. Refer to the documentation for the correct command.")
        logger.info(curr_command + ": Failure")
