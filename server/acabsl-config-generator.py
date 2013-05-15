import acabsl_interface
import thread
import time
import sys
import os

config_file = open(sys.argv[1], 'w')

try:
    serials1 = set(os.listdir('/dev/serial/by-id'))
except:
    serials1 = set()

serials1 = set()

raw_input("Please attach the USB to RS485 bridges and press enter.")

serials2 = set(os.listdir('/dev/serial/by-id'))

serials = ['/dev/serial/by-id/'+serial for serial in serials2 - serials1]

if len(serials) == 0:
    print "Found no new devices. Aborting."
    sys.exit(1)

for serial in serials:
    print "Found device", serial

interfaces = range(len(serials))

config_file.write("UDP_PORT = 5004\n")
config_file.write("serials = %s\n"%(str(serials)))
config_file.write("interfaces = %s\n"%(str(interfaces)))

acabsl_interface.init(serials, interfaces, [])

def get_number(message, base=10, default=None):
    number = None
    
    while number == None:
        input = raw_input(message)
        if input == '' and default != None:
            return default
        try:
            number = int(input, base)
        except:
            pass
    return number

def get_tuple(message, default=None):
    tuple = None
    
    while tuple == None:
        input = raw_input(message)
        if input == '' and default != None:
            return default
        try:
            input = input.split(',')
            tuple = (int(input[0]), int(input[1]))
        except:
            pass
    return tuple

xsize = get_number("Please enter the horizontal dimension [16]: ", 10, 16)
ysize = get_number("Please enter the vertical dimension [6]: ",10, 6)
print "Your matrix is",xsize,"X",ysize,"big."

min_address = get_number("Please enter the smallest lamp address (in hexadecimal)[10]: ", 16, 0x10)
max_address = get_number("Please enter the smallest lamp address (in hexadecimal)[90]: ", 16, 0x90)
print "Tested address range: %02X - %02X"%(min_address, max_address)

addresses = range(min_address, max_address+1)

matrix = [[None for x in range(xsize)] for y in range(ysize)]

def get_matrix(matrix):
    m = '['
    for line in matrix:
        m+='['
        for entry in line:
            if entry != None:
                m+='(0x%02X,%d), '%(entry[0], entry[1])
            else:
                m+= 'None, '
        m = m[:-2] + '],\n'
    m = m[:-2] + ']\n'
    return m

def print_matrix(matrix):
    print "Currently known matrix:"
    print get_matrix(matrix)

def get_first_unknown_index(matrix):
    for x in range(len(matrix[0])):
        for y in range(len(matrix)):
            if matrix[y][x] == None:
                return (x,y)
    return None, None

for interface in interfaces:
    acabsl_interface.sendSetColor(0, 0, 0, 0, interface)

def half(l):
    return l[0:(len(l)+1)/2], l[(len(l)+1)/2:]

def set_interfaces(interfaces, r, g, b):
    for interface in interfaces:
        acabsl_interface.sendSetColor(0, r, g, b, interface)

def set_lamps(addresses, interface, r, g, b):
    for address in addresses:
        acabsl_interface.sendSetColor(address, r, g, b, interface)

def find_interface(interfaces):
    set_interfaces(interfaces, 0, 0, 255)
    red_interfaces, green_interfaces = half(interfaces)
    blue_interfaces = []
    
    abort = False
    while not abort:
        set_interfaces(red_interfaces, 255, 0, 0)
        set_interfaces(green_interfaces, 0, 255, 0)
        set_interfaces(blue_interfaces, 0, 0, 255)

        result = raw_input("Which color does the lamp have? (r,g,b): ")
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
            abort = True

    print "There was an error. Aborting."
    return None

def find_lamp_address(interface, addresses):
    acabsl_interface.sendSetColor(0, 0, 0, 255, interface)
    red_addresses, green_addresses = half(addresses)
    blue_addresses = []
    
    abort = False
    while not abort:
        set_lamps(red_addresses, interface, 255, 0, 0)
        set_lamps(green_addresses, interface, 0, 255, 0)
        set_lamps(blue_addresses, interface, 0, 0, 255)

        result = raw_input("Which color does the lamp have? (r,g,b): ")
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
            abort = True

    print "There was an error. Aborting."
    return None
    
while True:
    print_matrix(matrix)
    x,y = get_first_unknown_index(matrix)
    if x == None or y == None:
        break
    x,y = get_tuple("Coordinate to test: [%d,%d]: "%(x,y), (x,y))
    print "Searching lamp at coordinate (%d,%d):"%(x,y)
    interface = find_interface(interfaces)
    if interface == None:
        continue
    lamp_address = find_lamp_address(interface, addresses)

    if lamp_address == None:
        continue

    addresses.remove(lamp_address)
    
    matrix[y][x] = (lamp_address, interface)


config_file.write("matrix = ")
m = get_matrix(matrix)
m = m.split('\n')
config_file.write(m[0]+'\n')

for line in m[1:]:
    config_file.write("          " + line + '\n')
config_file.close()

