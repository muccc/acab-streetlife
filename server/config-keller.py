server_ip = '0.0.0.0'
server_port = 5000
serials = ['/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A400fvDu-if00-port0']
interfaces = [0]
matrix = [[(0x8B,0)],
          [(0x82,0)],
          [(0x3F,0)],
          [(0x80,0)],
          [(0x84,0)],
          [(0x83,0)],
          [(0x87,0)],
          [(0x3E,0)],
          [(0x8D,0)],
          [(0x26,0)],
          [(0x1B,0)],
          [(0x89,0)],
          ]

simulation = False
router_base_port = 8000

walls = [
  { 'host': 'localhost', 'port': server_port,
    'simhost': '0.0.0.0', 'simport': server_port,
    'startx': 0, 'starty': 0},
]
