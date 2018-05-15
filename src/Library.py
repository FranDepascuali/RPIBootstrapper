#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import zipfile
from IOManager import *

def ask_user_for_disk():
    print_statement("Hello! The first step is to locate the partition in which the SD card is mounted")
    request_input("Press any key so I list the partitions")
    listPartitions()
    print_statement("Please, look for the partition where the SD card is mounted in the previous tables. In my case, it was /dev/disk0.")

    answer = False
    while answer == False:
        sd_partition = request_input("Enter partition of mounted SD card (example: /dev/disk0): ")
        if sd_partition == None:
            print_error("Partition cannot be None!")
        else:
            context = "It is important to check this because if partition is incorrect, you could erase your OS =("
            answer = yes_or_no(context, "Just for confirmation, is {} where your sd card is mounted? ".format(sd_partition))

    # We use r-disk because it is more efficient (instead of /dev/disk0, /dev/rdisk0)
    sd_partition_list = sd_partition.split('disk')
    sd_partition_list.insert(1, 'rdisk')

    return ''.join(sd_partition_list)

def list_local_network_ips():
    directive = "Listing network IPs..."
    command = "arp -a"
    success = "IP adresses listed"

    __call__(directive, command, success_message)

def activate_ssh_if_needed():
    context = "ssh is required to log from outside the RPI. For security reasons, it is initially turned off. It could be useful if you want to configure your raspberry pi and you don't have a monitor and keyboard."
    answer = yes_or_no(context, "Do you want to activate ssh?")

    if answer == True:
        create_file("/Volumes/boot/ssh")
        import stat
        os.chmod("/Volumes/boot/ssh", stat.S_IRWXO)

def yes_or_no_cycle(input_request_message, context, question):
    answer = False
    while answer == False:
        entered_input = request_input(input_request_message)
        answer = yes_or_no(context, question.format(entered_input))

    return entered_input

def yes_or_no(context, question):
    print_info(context)
    reply = str(request_input(question + ' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    elif reply[0] == 'n':
        return False
    else:
        return yes_or_no(question)

def runGPUMonitor():
    __call__("", "nvidia-smi -l 1", "")

def runCPUMonitor():
    __call__("", "top", "")

def create_file(file_path):
    directive = "Creating file {}".format(file_path)
    command = "touch {}".format(file_path)
    sucess = "File {} created".format(file_path)

    __call__(directive, command, sucess, requires_privileges = True)

def numberOfFiles(directory_path):
    number_of_files = len(os.listdir(directory_path))
    print_success("Directory {} contains {} files".format(os.path.abspath(directory_path), number_of_files))

def listPartitions():
    __call__("", "diskutil list", success_message = "Partitions listed via diskutil")

def listMountedDisks():
    __call__("", "df -h", success_message = "Mounted disks listed via df")

def unmount_disk_interactively():
    print_statement("Please, locate where the name under filesystem column that refers to your RPI (similar to /dev/diskXs1)")
    listMountedDisks()

    input_request_message = "Please, locate where the name under filesystem column that refers to your RPI (similar to /dev/diskXs1)"
    context = ""
    question = "Is {} where your disk is mounted?"
    disk_name = yes_or_no_cycle(input_request_message, context, question)
    unmountDisk(disk_name)

def unmountDisk(disk_name):
    directive = "Unmounting disk {}".format(disk_name)
    command = "diskutil unmount {}".format(disk_name)
    success = "Disk {} correctly unmounted".format(disk_name)

    __call__(directive, command, success, requires_privileges = True)

def mountDisk(disk_name):
    directive = "Mounting disk {}".format(disk_name)
    command = "diskutil mount {}".format(disk_name)
    success = "Disk {} correctly mounted".format(disk_name)

    __call__(directive, command, success, requires_privileges = True)

def eject_disk(disk_name):
    directive = "Ejecting disk {}".format(disk_name)
    cmd = "diskutil eject {}".format(disk_name)
    success = "Disk {} correctly ejected".format(disk_name)

    __call__(directive, cmd, success, requires_privileges = True)

def unzip(zip_file_path):
    print_statement("Unzipping file {}".format(zip_file_path))
    directory_path = os.path.dirname(os.path.realpath(zip_file_path))
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(directory_path)
        file_path = os.path.join(directory_path, zip_ref.namelist()[0])
        print_success(message = "File unzipped to {}".format(file_path))
        return file_path

def delete_file(file_path):
    print_statement("Deleting file {}".format(file_path))
    try:
        os.remove(file_path)
        print_success(message = "File {} deleted".format(file_path))
    except OSError as error:
        print_error(error.strerror)
        pass

def format_partition(disk_name):
    directive = "Formating {} partition".format(disk_name)
    cmd = "diskutil eraseDisk FAT32 RASPBIAN MBRFormat {}".format(disk_name)
    success = "Disk {} correctly formatted".format(disk_name)

    __call__(directive, cmd, success, requires_privileges = True)

def install_raspbian(raspian_image_path, disk_name):
    directive = "Installing {} to {} partition. This could take some minutes, please wait...".format(raspian_image_path, disk_name)
    cmd = "dd bs=1m if={} of={} conv=sync".format(raspian_image_path, disk_name)
    success = "Raspbian OS correctly installed to {}".format(disk_name)

    __call__(directive, cmd, success, requires_privileges = True)
