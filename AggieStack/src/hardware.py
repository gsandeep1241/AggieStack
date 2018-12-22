class Hardware:
    def __init__(self, name, ip, mem, num_disks, num_vcpus):
        self.name = name
        self.ip = ip
        self.mem = mem
        self.num_disks = num_disks
        self.num_vcpus = num_vcpus