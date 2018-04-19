import os.path
import sys
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

racks = {}
instances = {}
instance_on_server = {}
server_instances = {}
machines_on_racks = {}

curr_command = ""


def handle_config(cmd_parts):
    global hardware, hardware_configs
    global images, image_configs
    global flavors, flavor_configs
    global curr_command,racks,instances,instance_on_server,server_instances,machines_on_racks
    global hardware_configs_fixed
    if (len(cmd_parts) != 4):
        sys.stderr.write("ERROR: Invalid command.")
        logger.info(curr_command + ": Failure")
        return;

    if (cmd_parts[2] == "--hardware"):
        file = cmd_parts[3]
        my_file = "../p1_config/" + file

        if (os.path.exists(my_file)):

            if hardware:
                hardware_configs = {}
                racks = {}
                instances = {}
                instance_on_server = {}
                server_instances = {}
                machines_on_racks = {}
                racks = {}
                instances = {}
                instance_on_server = {}
                server_instances = {}
                machines_on_racks = {}
                hardware_configs_fixed = {}

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

                if machines_on_racks.get(cfg[1]) == None:
                    machines_on_racks[cfg[1]] = []
                machines_on_racks[cfg[1]].append(cfg[0])

            print len(hardware_configs), 'physical servers now available.'
            logger.info(curr_command + ": Success")

        else:
            sys.stderr.write("ERROR: File you specified does not exist." + "\n")
            logger.info(curr_command + ": Failure")

    elif (cmd_parts[2] == "--images"):
        file = cmd_parts[3]
        my_file = "../p1_config/" + file

        if (os.path.exists(my_file)):

            images = True

            with open(my_file) as f:
                lines = f.readlines()

            num_configs = int(lines[0])

            for x in range(1, num_configs + 1):
                cfg = lines[x].split(" ")
                img = NewImage(cfg[0], cfg[1], cfg[2])
                image_configs[cfg[0]] = img

            print len(image_configs), 'images now available.'
            logger.info(curr_command + ": Success")

        else:
            sys.stderr.write("ERROR: File you specified does not exist." + "\n")
            logger.info(curr_command + ": Failure")

    elif (cmd_parts[2] == "--flavors"):
        file = cmd_parts[3]
        my_file = "../p1_config/" + file

        if (os.path.exists(my_file)):

            flavors = True

            with open(my_file) as f:
                lines = f.readlines()

            num_configs = int(lines[0])

            for x in range(1, num_configs + 1):
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
    global hardware, hardware_configs
    global images, image_configs
    global flavors, flavor_configs
    global curr_command, racks, instances, instance_on_server, server_instances, machines_on_racks
    global hardware_configs_fixed
    if (len(cmd_parts) != 3):
        sys.stderr.write("ERROR: Invalid command." + "\n")
        logger.info(curr_command + ": Failure")
        return;

    if (cmd_parts[2] == "hardware"):
        if (hardware):
            print("Physical servers available:")
            print("Name, Rack, IP, RAM, Num_Disks, Num_Vcpus")

            for key in hardware_configs_fixed:
                hw = hardware_configs_fixed[key]
                print hw.name, " ", hw.rack, " ", hw.ip, " ", hw.mem, " ", hw.num_disks, " ", hw.num_vcpus
            if (all == None):
                logger.info(curr_command + ": Success")
        else:
            sys.stderr.write("ERROR: No physical servers available." + "\n")
            logger.info(curr_command + ": Failure")

    elif (cmd_parts[2] == "images"):
        if (images):
            print("Images available:")
            print("Name, Size, Path")

            for key in image_configs:
                img = image_configs[key]
                print img.name, " ", img.size, " ", img.path
            if (all == None):
                logger.info(curr_command + ": Success")
        else:
            sys.stderr.write("ERROR: No images available." + "\n")
            logger.info(curr_command + ": Failure")

    elif (cmd_parts[2] == "flavors"):
        if (flavors):
            print("Flavors available:")
            print("Type, Ram, Disks, VCPUs")

            for key in flavor_configs:
                flv = flavor_configs[key]
                print flv.type, " ", flv.ram, " ", flv.disks, " ", flv.vcpus
            if (all == None):
                logger.info(curr_command + ": Success")
        else:
            sys.stderr.write("ERROR: No flavors available." + "\n")
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
            sys.stderr.write("ERROR: Hardware/Image/Flavor not available." + "\n")
            logger.info(curr_command + ": Failure")

    else:
        sys.stderr.write("ERROR: Invalid command." + "\n")
        logger.info(curr_command + ": Failure")


def handle_admin(cmd_parts):
    global hardware, hardware_configs
    global images, image_configs
    global flavors, flavor_configs
    global curr_command, racks, instances, instance_on_server, server_instances, machines_on_racks
    global hardware_configs_fixed
    if len(cmd_parts) == 4 and cmd_parts[2] == "show" and cmd_parts[3] == "hardware":

        if (hardware):
            print("Physical servers available:")
            print("Name, Rack, IP, RAM, Num_Disks, Num_Vcpus")

            if len(hardware_configs) == 0:
                print("No physical servers available.")
                logger.info(curr_command + ": Success")
                return

            for key in hardware_configs:
                hw = hardware_configs[key]
                print hw.name, " ", hw.rack, " ", hw.ip, " ", hw.mem, " ", hw.num_disks, " ", hw.num_vcpus

            logger.info(curr_command + ": Success")
        else:
            sys.stderr.write("ERROR: No physical servers available." + "\n")
            logger.info(curr_command + ": Failure")

    elif len(cmd_parts) == 4 and cmd_parts[2] == "show" and cmd_parts[3] == "instances":

        if len(instance_on_server) == 0:
            print("No instances present.")
            logger.info(curr_command + " :Success")
            return

        print "Instance", "Physical Server"
        for key in instance_on_server:
            print key, " ", instance_on_server[key]

        logger.info(curr_command + ": Success")
        return

    elif len(cmd_parts) == 4 and cmd_parts[2] == "evacuate":
        rack_name = cmd_parts[3]
        if racks.get(rack_name) == None:
            sys.stderr.write("ERROR: Rack does not exist." + "\n")
            logger.info(curr_command + ": Failure")
            return

        all_machines_on_rack = machines_on_racks[rack_name]
        for machine in all_machines_on_rack:
            if server_instances.get(machine) == None:
                del hardware_configs[machine]
                print(machine + " deleted")
                continue
            all_instances = server_instances[machine]
            for each_instance in all_instances:
                done = False
                for key in hardware_configs:
                    if hardware_configs[key].rack == rack_name:
                        continue
                    if(can_host(hardware_configs[key], flavor_configs[instances[each_instance].flavor])):
                        done = True
                        curr_mac = hardware_configs[key]
                        curr_flv = flavor_configs[instances[each_instance].flavor]

                        curr_mac.mem = int(curr_mac.mem) - int(curr_flv.ram)
                        curr_mac.num_disks = int(curr_mac.num_disks) - int(curr_flv.disks)
                        curr_mac.num_vcpus = int(curr_mac.num_vcpus) - int(curr_flv.vcpus)

                        inst = instances[each_instance]
                        instances[each_instance] = inst

                        instance_on_server[each_instance] = key

                        if server_instances.get(key) == None:
                            server_instances[key] = []
                        server_instances[key].append(each_instance)
                        break
                if done:
                    print(each_instance + " successfully migrated.")
                else:
                    del instances[each_instance]
                    del instance_on_server[each_instance]
                    print(each_instance + " could not be migrated.")
            del hardware_configs[machine]
            print(machine + " removed.")
            del server_instances[machine]
        machines_on_racks[rack_name] = []

        print("Rack evacuation done.")
        logger.info(curr_command + ": Success")

    elif len(cmd_parts) == 4 and cmd_parts[2] == "remove":

        if hardware_configs.get(cmd_parts[3]) == None:
            sys.stderr.write("ERROR: Server does not exist" + "\n")
            logger.info(curr_command + ": Failure")
            return

        if server_instances.get(cmd_parts[3]) != None:
            all_instances = server_instances[cmd_parts[3]]
            for ins in all_instances:
                del instance_on_server[ins]
                del instances[ins]
            del server_instances[cmd_parts[3]]

        del hardware_configs[cmd_parts[3]]

        print("Machine successfully removed.")
        logger.info(curr_command + ": Success")
        return

    elif len(cmd_parts) == 14 and cmd_parts[2] == "add" and cmd_parts[3] == "--mem" and cmd_parts[5] == "--disk" and cmd_parts[7] == "--vcpus" and cmd_parts[9] == "--ip" and cmd_parts[11] == "--rack":

        if(hardware_configs.get(cmd_parts[13]) != None):
            sys.stderr.write("ERROR: Machine with the name already exists." + "\n")
            logger.info(curr_command + ": Failure")
            return

        if(racks.get(cmd_parts[12]) == None):
            sys.stderr.write("ERROR: Rack does not exist." + "\n")
            logger.info(curr_command + ": Failure")
            return

        hw = NewHardware(cmd_parts[13], cmd_parts[12], cmd_parts[10], cmd_parts[4], cmd_parts[6], cmd_parts[8])
        hw1 = NewHardware(cmd_parts[13], cmd_parts[12], cmd_parts[10], cmd_parts[4], cmd_parts[6], cmd_parts[8])
        hardware_configs[cmd_parts[13]] = hw

        print("Machine successfully added.")
        logger.info(curr_command + ": Success")
        return

    else:
        sys.stderr.write("ERROR: Invalid command." + "\n")
        logger.info(curr_command + ": Failure")

def can_host(mac, vm):
    if (int(mac.mem) >= int(vm.ram) and int(mac.num_disks) >= int(vm.disks) and int(mac.num_vcpus) >= int(
            vm.vcpus)):
        return True
    else:
        return False

def handle_server(cmd_parts):
    global hardware, hardware_configs
    global images, image_configs
    global flavors, flavor_configs
    global curr_command, racks, instances, instance_on_server, server_instances, machines_on_racks
    global hardware_configs_fixed
    if(not (hardware and images and flavors)):
        sys.stderr.write("ERROR: Load all hardware, images and flavors." + "\n")
        logger.info(curr_command + ": Failure")
        return

    if(len(cmd_parts) <= 2):
        sys.stderr.write("ERROR: Invalid command." + "\n")
        logger.info(curr_command + ": Failure")
        return

    if cmd_parts[2] == "list" and len(cmd_parts) == 3:

        if len(instances) == 0:
            print("No instances present.")
            logger.info(curr_command + ": Success")
            return

        print "Name", "Image", "Flavor"
        for key in instances:
            print instances[key].name, " ", instances[key].image, " ", instances[key].flavor

        logger.info(curr_command + ": Success")
        return

    elif cmd_parts[2] == "delete" and len(cmd_parts) == 4:

        if instances.get(cmd_parts[3]) == None:
            sys.stderr.write("ERROR: Instance does not exist" + "\n")
            logger.info(curr_command + ": Failure")
            return

        flv = flavor_configs[instances[cmd_parts[3]].flavor]
        mac = hardware_configs[instance_on_server[cmd_parts[3]]]

        mac.mem = int(mac.mem) + int(flv.ram)
        mac.num_disks = int(mac.num_disks) + int(flv.disks)
        mac.num_vcpus = int(mac.num_vcpus) + int(flv.vcpus)

        del instances[cmd_parts[3]]
        del instance_on_server[cmd_parts[3]]

        server_instances[mac.name].remove(cmd_parts[3])

        print("Successfully deleted instance.")
        logger.info(curr_command + ": Success")
        return

    elif len(cmd_parts) == 8 and cmd_parts[2] == "create" and cmd_parts[3] == "--image" and cmd_parts[5] == "--flavor":

        img = cmd_parts[4]
        flv = cmd_parts[6]
        if image_configs.get(img) == None:
            sys.stderr.write("ERROR: Image not available." + "\n")
            logger.info(curr_command + ": Failure")
            return

        if flavor_configs.get(flv) == None:
            sys.stderr.write("ERROR: Flavor not available." + "\n")
            logger.info(curr_command + ": Failure")
            return

        if instances.get(cmd_parts[7]) != None:
            sys.stderr.write("ERROR: Instance with the name already exists." + "\n")
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

                if server_instances.get(key) == None:
                    server_instances[key] = []
                server_instances[key].append(cmd_parts[7])

                print("Successfully created an instance.")
                logger.info(curr_command + ": Success")
                return

        sys.stderr.write("ERROR: Resources unavailable." + "\n")
        logger.info(curr_command + ": Failure")
        return

    else:
        sys.stderr.write("ERROR: Invalid command." + "\n")
        logger.info(curr_command + " : Failure")

counter = 1
with open('../input.txt', 'r') as f:
    for cmd in f:
        print ("Command# " + str(counter) + ":")
        counter += 1
        cmd = cmd.rstrip('\n')
        curr_command = cmd
        print cmd
        cmd_parts = cmd.split(" ")

        if (len(cmd_parts) <= 1):
            sys.stderr.write("ERROR: Invalid command." + "\n")
            logger.info(curr_command + ": Failure")
            continue

        if (cmd_parts[0] != "aggiestack"):
            sys.stderr.write("ERROR: Invalid command." + "\n")
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
            sys.stderr.write("ERROR: Invalid command." + "\n")
            logger.info(curr_command + ": Failure")
        print ("************************************************************************************************************")
