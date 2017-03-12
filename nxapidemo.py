#!/usr/bin/python env
'''
This is just a demo script I created to get started with using hte NXAPI and pycsco module.
'''
import getpass

import json

import xmltodict

from pycsco.nxos.device import Device

from prettytable import PrettyTable

print chr(0x1b) + '[2J'
# clear the screen

print "Enter your credentials:"

username = raw_input('Username: ')
# prompt for the username to use

password = getpass.getpass("Password: ")
# prompt for the password to use

device_ip = raw_input("Switch Hostname or IP: ")
# prompt for the hostname or IP of the switch

nxapi_connect = Device(ip=device_ip, username=username, password=password)
# setup an object to include ip and creds for the pyscsco

loop = 1

while loop == 1:

    '''
    Ask the user which function they want to launch.
    '''
    print chr(0x1b) + '[2J'
    # clear the screen
    print "\
    Make a selection:\n \
     [1] Device Info\n \
     [2] IP Arp Table\n \
     [3] Change Device\n \
     [4] Exit\n \
     "
    selection = raw_input('Selection [1]: ') or "1"
    selection = int(selection)


    if selection == 1:
        get_sh_ver = nxapi_connect.show('show version')
        # this returns a tuple of 2 xml objects.  the first is headers, etc. and the second is the data we want

        sh_ver_dict = xmltodict.parse(get_sh_ver[1])
        # converting the second element to a python dictionary

        sh_ver_simple = sh_ver_dict['ins_api']['outputs']['output']['body']
        # trim down headers and wrapers

        hostname = sh_ver_simple['host_name']
        # creat object of parsed data for the hostname of device

        version = sh_ver_simple['rr_sys_ver']
        # creat object of parsed data for the version of device

        chassis_type = sh_ver_simple['chassis_id']
        # creat object of parsed data for the model of device

        '''
        Print device informtion
        '''
        print "Hostname: {}" .format(hostname)
        print "Version: {}" .format(version)
        print "Model: {}" .format(chassis_type)

        raw_input('Press any key to continue...')

    elif selection == 2:
        get_sh_arp = nxapi_connect.show('show ip arp vrf all')
        # TBD

        sh_arp_dict = xmltodict.parse(get_sh_arp[1])
        # TBD

        sh_arp_simple = sh_arp_dict['ins_api']['outputs']['output']['body']['TABLE_vrf']['ROW_vrf']

        arp_entries = sh_arp_simple['cnt-total']
        # Total number of arp entries

        t = PrettyTable(['Interface', 'IP', 'Age', 'MAC'])
        # Create a disable table to add data to.

        for entry in sh_arp_simple['TABLE_adj']['ROW_adj']:

            row = [str(entry['intf-out']), str(entry['ip-addr-out']), str(entry['time-stamp']), str(entry['mac'])]
            # Make a list from the data in each dictrionary entry

            t.add_row(row)
            # add a row to the PrettyTable

        '''
        Print device information
        '''
        print t
        print "{} arp entries retrieved." .format(arp_entries)

        raw_input('Press any key to continue...')

    elif selection == 3:

        device_ip = raw_input("Switch Hostname or IP: ")
        # prompt for the hostname or IP of the switch

    elif selection == 4:

        loop = 0

        print "Exiting..."
