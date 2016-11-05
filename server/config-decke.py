server_ip = '0.0.0.0'
server_port = 7000
serials = ['/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A10044Xt-if00-port0', '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A10044Xu-if00-port0']
interfaces = [0, 1]
matrix = [[(0x57,0), (0x50,1)],
          [(0x14,0), (0x53,1)],
          [(0x10,0), (0x43,1)],
          [(0x6B,0), (0x66,1)],
          [(0x34,0), (0x23,1)],
          [(0x4F,0), (0x25,1)],
          [(0x71,0), (0x29,1)],
          [(0x22,0), (0x47,1)],
          [(0x31,0), (0x30,1)],
          [(0x32,0), (0x46,1)],
          [(0x3E,0), (0x19,1)],
          [(0x45,0), (0x24,1)]]

#matrix = [[(0x57,0), (0x50,1)],
#          [(0x14,0), (0x53,1)],
#          [(0x6B,0), (0x66,1)],
#          [(0x6B,0), (0x66,1)]]

simulation = False
router_base_port = 8000

walls = [
  { 'host': 'localhost', 'port': server_port,
    'simhost': '0.0.0.0', 'simport': server_port,
    'startx': 0, 'starty': 0},
]
