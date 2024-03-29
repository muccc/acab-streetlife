#!/usr/bin/env python
import acabsl_interface
import time
import sys
import os

def get_matrix(matrix):
    m = '['
    for line in matrix:
        m+='['
        for entry in line:
            if entry == None:
                m += 'None, '
            elif entry == (None, None):
                m += '(None, None), '
            else:
                m += '(0x%02X,%d), '%(entry[0], entry[1])
        m = m[:-2] + '],\n'
    m = m[:-2] + ']\n'
    return m

def print_matrix(matrix):
    print("Currently known matrix:")
    print(get_matrix(matrix))

def write_config(serials, interfaces, matrix):
    config_file = open(sys.argv[1], 'w')
    
    config_file.write("server_ip = '0.0.0.0'\n")
    config_file.write("server_port = 5000\n")
    config_file.write("serials = %s\n"%str(serials))
    config_file.write("interfaces = %s\n"%str(interfaces))

    if len(matrix) > 0:
        config_file.write("matrix = ")
        m = get_matrix(matrix)
        m = m.split('\n')
        config_file.write(m[0]+'\n')

        for line in m[1:]:
            if line:
                config_file.write("          " + line)
            config_file.write('\n')

    config_file.write("simulation = False\n")
    config_file.write("router_base_port = 8000\n")
    config_file.write("""
walls = [
  { 'host': 'localhost', 'port': server_port,
    'simhost': '0.0.0.0', 'simport': server_port,
    'startx': 0, 'starty': 0},
]
""")

    config_file.close()

try:
    serials1 = set(os.listdir('/dev/serial/by-id'))
except:
    serials1 = set()

serials1 = set()
input("Please attach the USB to RS485 bridges and press enter.: ")

serials2 = set(os.listdir('/dev/serial/by-id'))
serials = ['/dev/serial/by-id/'+serial for serial in serials2 - serials1]

if len(serials) == 0:
    print("Found no new devices. Aborting.")
    sys.exit(1)

for serial in serials:
    print("Found device: ", serial)

interfaces = list(range(len(serials)))

matrix = []

write_config(serials, interfaces, matrix)

acabsl_interface.init(serials, interfaces, matrix)

def get_number(message, base=10, default=None):
    number = None
    
    while number == None:
        inp = input(message)
        if inp == '' and default != None:
            return default
        try:
            number = int(inp, base)
        except:
            pass
    return number

def get_tuple(message, default=None):
    tuple = None
    
    while tuple == None:
        inp = input(message)
        if inp == '' and default != None:
            return default
        try:
            inp = inp.split(',')
            tuple = (int(inp[0]), int(inp[1]))
        except:
            pass
    return tuple

xsize = get_number("Please enter the horizontal dimension [16]: ", 10, 16)
ysize = get_number("Please enter the vertical dimension [6]: ",10, 6)
print("Your matrix is",xsize,"X",ysize,"big.")

min_address = get_number("Please enter the smallest lamp address (in hexadecimal)[10]: ", 16, 0x10)
max_address = get_number("Please enter the biggest lamp address (in hexadecimal)[BF]: ", 16, 0xFF)
print("Tested address range: %02X - %02X (%d addresses)"%(min_address, max_address, max_address-min_address+1))

addresses = list(range(min_address, max_address+1))

matrix = [[None for x in range(xsize)] for y in range(ysize)]

def get_first_unknown_index(matrix):
    for x in range(len(matrix[0])):
        for y in range(len(matrix)):
            if matrix[y][x] == None:
                return (x,y)
    return None, None

def get_next_unknown_index(matrix):
    last_good = None

    for x in range(len(matrix[0])):
        for y in range(len(matrix)):
            if matrix[y][x] != None:
                last_good = (x,y)
    
    if last_good == None:
        return 0, 0
    
    next_bad = (last_good[0], last_good[1] + 1)
    
    if next_bad[1] == ysize:
        next_bad[0]+=1
        next_bad[1]=0
    return next_bad

for interface in interfaces:
    acabsl_interface.sendSetColor(0, 0, 0, 0, interface)

def half(l):
    return l[0:int((len(l)+1)/2)], l[int((len(l)+1)/2):]

def set_interfaces(interfaces, r, g, b):
    for interface in interfaces:
        acabsl_interface.sendSetColor(0, r, g, b, interface)

def set_lamps(addresses, interface, r, g, b):
    for address in addresses:
        acabsl_interface.sendSetColor(address, r, g, b, interface)

def set_known_addresses(r, g, b):
    for x in range(len(matrix[0])):
        for y in range(len(matrix)):
            if matrix[y][x] != None and matrix[y][x] != (None, None):
                acabsl_interface.sendSetColor(matrix[y][x][0], r, g, b, matrix[y][x][1])


def find_interface(interfaces):
    set_interfaces(interfaces, 0, 0, 255)
    red_interfaces, green_interfaces = half(interfaces)
    blue_interfaces = []
    
    print("Looking for the correct interface. Press 'Q' to abort. Press 'N' if the lamp does not exist.")
    
    abort = False
    skip = False
    while (not abort) and (not skip):
        set_interfaces(red_interfaces, 255, 0, 0)
        set_interfaces(green_interfaces, 0, 255, 0)
        set_interfaces(blue_interfaces, 0, 0, 0)
	
        set_known_addresses(0, 0, 0)	

        result = input("Which color does the lamp have? (r,g,b): ")
        if result == 'r' and len(red_interfaces) == 1:
            return red_interfaces[0]
        if result == 'r' and len(red_interfaces) > 0:
            blue_interfaces += green_interfaces
            red_interfaces, green_interfaces = half(red_interfaces)
            continue

        if result == 'g' and len(green_interfaces) == 1:
            return green_interfaces[0]
        if result == 'g' and len(green_interfaces) > 0:
            blue_interfaces += red_interfaces
            red_interfaces, green_interfaces = half(green_interfaces)
            continue

        if result != '' and result in  'rgb':
            print("There was an error: The lamp ahould not have this color")
            abort = True
        
        if result == 'Q':
            abort = True

        if result == 'N':
            skip = True

    if abort: 
        print("Aborting.")
        return None
    
    if skip:
        print("Skipping this lamp")
        return 'skip'
    
def find_lamp_address(interface, addresses):
    acabsl_interface.sendSetColor(0, 0, 0, 0, interface)
    red_addresses, green_addresses = half(addresses)
    blue_addresses = []
    
    print('Looking for the lamp\'s address. Press Q to abort.')
    abort = False

    while not abort:
        set_lamps(red_addresses, interface, 255, 0, 0)
        set_lamps(green_addresses, interface, 0, 255, 0)
        set_lamps(blue_addresses, interface, 0, 0, 0)

        result = input("Which color does the lamp have? (r,g,b): ")
        if result == 'r' and len(red_addresses) == 1:
            return red_addresses[0]
        if result == 'r' and len(red_addresses) > 0:
            blue_addresses += green_addresses
            red_addresses, green_addresses = half(red_addresses)
            continue

        if result == 'g' and len(green_addresses) == 1:
            return green_addresses[0]
        if result == 'g' and len(green_addresses) > 0:
            blue_addresses += red_addresses
            red_addresses, green_addresses = half(green_addresses)
            continue
    
        if result != '' and result in  'rgb':
            print("There was an error: The lamp should not have this color")
            abort = True
        
        if result == 'Q':
            abort = True

    print("Aborting.")
    return None

write_config(serials, interfaces, matrix)

while True:
    print_matrix(matrix)
    x,y = get_first_unknown_index(matrix)
    #x,y = get_next_unknown_index(matrix)
    if x == None or y == None:
        break
    x,y = get_tuple("Coordinate to test (-1,-1 to quit): [%d,%d]: "%(x,y), (x,y))

    if x==-1 and y==-1:
        print("Aborting.")
        break

    print("Starting to search for lamp at coordinate (%d,%d):"%(x,y))

    if matrix[y][x] != None:
        addresses.append(matrix[y][x][0])

    interface = find_interface(interfaces)
    set_interfaces(interfaces, 0, 0, 0)

    if interface == None:
        continue

    if interface != 'skip':

        lamp_address = find_lamp_address(interface, addresses)

        if lamp_address == None:
            continue

        for i in range(3):
            acabsl_interface.sendSetColor(lamp_address, 255, 255, 255, interface)
            time.sleep(.2)
            acabsl_interface.sendSetColor(lamp_address, 0, 0, 0, interface)
            time.sleep(.2)

        addresses.remove(lamp_address)
    
    else:
        lamp_address = None
        interface = None
        
    matrix[y][x] = (lamp_address, interface)
    write_config(serials, interfaces, matrix)

