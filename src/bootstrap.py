# import Library
# import Network

# Initial setup
# def configure_sd_disk():
#     raspian_zip_image_path = "/Users/FranDepascuali/Documents/Projects/Coding/IOT/RPI/OS/2017-08-16-raspbian-stretch.zip"
#     disk_name = Library.ask_user_for_disk()
#     Library.format_partition(disk_name)
#     Library.unmount_disk_interactively()
#     raspbian_image_path = Library.unzip(raspian_zip_image_path)
#     Library.install_raspbian(raspbian_image_path, disk_name)
#     Library.delete_file(raspbian_image_path)
#     Library.activate_ssh_if_needed()
#     Library.eject_disk(disk_name)


# Network.print_hosts_in_network("192.168.2.11", "24")
# Network.establish_ssh_connection("192.168.2.11", "pi", "raspberry")
import sys
sys.path.append("/Users/FranDepascuali/Documents/Projects/Coding/IOT/RPI/src/programs")
import TwitterBot
