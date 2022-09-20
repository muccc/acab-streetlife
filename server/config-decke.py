server_ip = '0.0.0.0'
server_port = 7000
serials = ['/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400fvDr-if00-port0', '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A10044Xp-if00-port0']
interfaces = [0, 1]
matrix = [
          [(0x57,0), (0x47,1)],
          [(0x6d,0), (0x4a,1)],
          [(0x17,0), (0x41,1)],
          [(0x42,0), (0x3f,1)],
          [(0x67,0), (0x39,1)],
          [(0x20,0), (0x38,1)],
          [(0x5a,0), (0x43,1)],
          [(0x5c,0), (0x45,1)],
          [(0x4e,0), (0x4c,1)],
          [(0x22,0), (0x19,1)],
          [(0x28,0), (0x56,1)],
          [(0x26,0), (0x3e,1)],
         ]
simulation = False
router_base_port = 8000

walls = [
  { 'host': 'localhost', 'port': server_port,
    'simhost': '0.0.0.0', 'simport': server_port,
    'startx': 0, 'starty': 0},
]
