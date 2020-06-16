from sys import argv

#script, dominio = argv

def agregarSubred():
  f = open("/var/www/html/Script/confi.txt", "w")
  f.write("Hola")
  f.close()


agregarSubred()
