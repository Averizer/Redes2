from sys import argv

script, subred, netmask, rangem, rangeM, gateway = argv

path = "/etc/dhcp/dhcpd.conf"
options = "subnet "+subred+" netmask "+netmask+"{\n"
options = options + "\trange "+subred[0:len(subred)-1]+rangem
options = options + " " +subred[0:len(subred)-1]+rangeM+";\n"
options = options + "\toption routers " + gateway + ";\n"
options = options + "\tdefault-lease-time 600;\n"
options = options + "\tmax-lease-time 7200;\n}"

f = open(path, "a")
f.write(options)
f.close()
