import subprocess
import random
import string
import re
import time
from progress import bar

class MacAddresSet():
    """
    This class uses kali linux functionality to work with interfaces
    of your device and their mac addresses. Goodluck using this class!
    """

    def __init__(self, interface: str, mac_address: str = None) -> str:
        self.interface = interface
        self.mac_address = mac_address

    def display_valid_interfaces(self) -> None:
        """This method displays and returns a list of all valid interfaces!"""
        ip_link_show = subprocess.check_output(['ip', 'link', 'show'])
        interfaces = re.findall(r'\d:\s\w{1,}', ip_link_show.decode('utf-8'))
        try:
            print('Valid interfaces:')
            for interface in interfaces:
                print(interface)
            return interfaces
        except AttributeError:
            print('There is no any valid interfaces!')
    
    def check_interface(self, interface: str) -> str:
        """
        This method checks valid interface or not with help of 'ip link show'
        Returns True if interface is valid else returns False
        """
        ip_link_show = subprocess.check_output(['ip', 'link', 'show'])
        return interface in ip_link_show.decode('utf-8')


    def shutdown_interface(self, interface: str) -> str:
        """
        This method can shutdown any valid interface you want!
        Returns True if interface was shutdowned successfuly or interface
        that was shutdowned before (It'll be shutdowned again)!
        """
        if self.check_interface(interface):
            ifconfig = subprocess.check_output('ifconfig').decode('utf-8')
            if interface in ifconfig:
                subprocess.call(f"sudo ifconfig {interface} down", shell=True)
                print(f'{interface} interface was shutdowned successfully!')
                return True
            else:
                subprocess.call(f"sudo ifconfig {interface} down", shell=True)
                print(f'{interface} interface was shutdowned before!')
                return True
        else:
            print("{interface} is invalid! Try again!")
            return False

    def wake_up_interface(self, interface: str) -> str:
        """
        This method can wake up any valid interface you want!
        Returns False if interface is invalid, else returns True
        """
        if self.check_interface(interface):
            subprocess.call(f'sudo ifconfig {interface} up', shell=True)
            print(f'{interface} interface is waked up!')
            return True
        else:
            print(f"{interface} is invalid! Try again!")
            return False

    def generate_mac_address(self) -> None:
        """This method generates valid mac address with help of python random module!"""
        mac_address_string = ''
        mac_address_symbols = list('0123456789ABCDF')
        for i in range(1, 7):
        #Typical example of mac address - 6A:02:8D:09:DA:62 
        # Six pairs of letters, which are splitted with :
            mac_address_string += f"{random.choice(mac_address_symbols)+random.choice(mac_address_symbols)}:"
        return mac_address_string[0:-1]

    def interface_info(self, interface: str) -> str:
        """This method returns status of interface you want"""
        if self.check_interface(interface):
            nmcli_device_status = subprocess.check_output(['nmcli', 'device', 'status']).decode('utf-8').split('\n')
            for interface_info in nmcli_device_status:
                if interface in interface_info:
                    return f"{nmcli_device_status[0]}\n{interface_info}"    
        else:
            return 'f{interface} interface is invalid'
            
    def check_mac_address(self, mac_address: str) -> str:
        """
        This method checks mac address with 'in' python method
        Returns True if mac address is valid else returns False!
        """
        mac_address_symbols = list('0123456789ABCDF:')
        correct_symbols_used = not False in [i in mac_address_symbols for i in mac_address]
        is_not_mess = re.match(('\w\w:'*6)[:-1], mac_address) is not None
        correct_len = len(mac_address) == 17
        if all([correct_symbols_used, is_not_mess, correct_len]):
            return True
        else:
            if not correct_symbols_used:
                print(f'Symbols of your mac address are incorrect. Use these symbols to create mac address: {"".join(mac_address_symbols)}')
            if not is_not_mess:
                print(f"Your mac address hasn't right format. Right example of mac address: {self.generate_mac_address()}")
            if not correct_len:
                print(f"Your mac address length is incorrect. Right example of mac address: {self.generate_mac_address()}, length should be 17")
            return False

    def __change_mac_address(self):
        """
        This method is private. It changes mac address of interface without any checks,
        using this method by calling it aint recommended!
        """
        try:
            subprocess.call(f"sudo ifconfig {self.interface} down", shell=True)
            subprocess.call(f"sudo ifconfig {self.interface} hw ether {self.mac_address}", shell=True)
            subprocess.call(f"sudo ifconfig {self.interface} up", shell=True)
            subprocess.call(f"sudo ifconfig")
        finally:
            print(f"\nTried to switch mac address of {self.interface} interface to {self.mac_address}\n")
                 
            subprocess.call(f"sudo ifconfig {self.interface} up", shell=True)

    def time_change_mac_address(self, time_: int = 0, per: int = 0, list_mac: list = []) -> int:
        """
        This method's a final product of this class methods.

        Type 'ctrl+d' shortcut to start proccess

        If you see 'Cannot assign requested address', mac address is invalid (it's ok)

        If arguments ain't changed, method'll change mac address once.

        'time_' argument should be setted in minutes
        'per' argument should be setted in seconds (every 'per' seconds mac address'll be changed)

        Also you can set 'list_mac' argument which'll tell this method that it should use
        your list of mac addresses.
   
        Warnings:
            [.] 'list_mac' argument is disabled without 'time_' and 'per' arguments else method'll return False
            [.] If your length of list_mac won't suit formula 'time_/per=len(list_mac)' (you'll be notified of needed col of mac_addresses if there'll be a need),
            you'll be notified about this and you should choose two ways:
                1. You agree that method'll append needed col of mac_addresses, which'll be generated with generate_mac_address method
                2. You drop method completing, so you should add needed col of mac addresses to use this method.
            [.] Be sure that your list contains only correct mac addresses else method'll return False.
            [.] You can always drop method completing by 'ctrl+c' shortcut.
        """
        if all([time_>=0, per>=0, type(time_) == int, type(per) == int, type(list_mac) == list, False not in [self.check_mac_address(i) for i in list_mac]]):
            if self.mac_address is None:
                self.mac_address = self.generate_mac_address()
            else:
                if not self.check_mac_address(self.mac_address):
                    return f"{self.mac_address} mac address is invalid!"
            if not self.check_interface(self.interface):
                return f"{self.interface} interface is invalid!"
            
            subprocess.call('sudo -s', shell=True)

            if any([time_==0, per==0]):
                self.__change_mac_address()
                return f"Mac address of {self.interface} interface was successfully switched to {self.mac_address}"
            else:
                time_ *= 60 
                progressbar = bar.IncrementalBar('Bar', max=time_)
                start = 0
                list_mac_index = 0
                len_list_mac = time_ / per
                while len(list_mac) < len_list_mac:
                    list_mac.append(self.generate_mac_address())
                try:
                    while start != time_:
                        start += 1
                        progressbar.next() 
                        time.sleep(1)
                        if (start % per) == 0:
                            self.mac_address = list_mac[list_mac_index]
                            list_mac_index += 1
                            self.__change_mac_address() 
                    progressbar.finish()
                    return True
                except KeyboardInterrupt:
                    return '\nSuccessfully finished'
        else:
            return False


if __name__ == "__main__":
    object = MacAddresSet(interface='eth0')
    print(object.time_change_mac_address(time_=1, per=10, list_mac=['AA:BB:CC:DD:FF:11']))
    # object.check_interface
    # object.interface_info
    # object.check_mac_address
    # object.display_valid_interfaces
    # object.generate_mac_address
    # object.shutdown_interface
    # object.wake_up_interface
    # object.time_change_mac_address
    