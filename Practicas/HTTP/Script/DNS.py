from sys import argv

script, dominio, ip, zonei = argv
path1 = "/etc/bind/db.jovanny.local"
path2 = "/etc/bind/db.192.168"

#configuraión local
def archivoLocal(path, dominio, ip):
  options = dominio + ".\tIN\tA\t" + ip + "\n"
  f = open(str(path), 'a')
  f.write(options)
  f.close()

#configuracion inversa
def archivoInv(path, zonei, dominio, ip):
  pal = reverse(ip)
  options = pal[1:4] + "\tIN\tPTR\t" + dominio + ".\n"
  f = open(str(path), 'a')
  f.write(options)
  f.close()

#extra
def reverse(palabra):
  aux = palabra.split(".")
  p = ""
  for i in aux:
    p = i + p
    if(i != ""):
      p = "." + p
  return p

archivoLocal(str(path1),str(dominio),str(ip))
archivoInv(str(path2), str(zonei), str(dominio), str(ip))
