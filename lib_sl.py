import urllib2

HOST="127.1"
PORT=8080

def send(x,y,r,g,b,t=0):
  message = "/%s/%s/%i/%i/%i/%i" % (x, y, r, g, b, t*1000)
  urllib2.urlopen("http://%s:%i"% (HOST, PORT)+message)

def matrix(targetsize_x=8,targetsize_y=6):
  x=0
  y=0
  matrix = []
  while ( y < targetsize_y):
    while ( x < targetsize_x):
      p =  str(x) + str(y)
      matrix.append(p)
      x = x + 1

    y = y + 1
    x = 0
  return matrix
