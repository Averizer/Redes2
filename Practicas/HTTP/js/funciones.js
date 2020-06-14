function mostrarTFTP() {
    var tftp = document.getElementById("tftp");
    var dns = document.getElementById("dns");
    var dhcp = document.getElementById("dhcp");
    if (tftp.style.display === "none") {
        tftp.style.display = "block";
        dns.style.display = "none";
        dhcp.style.display = "none";
    } else {
        tftp.style.display = "block";
    }
}
function mostrarDNS() {
    var tftp = document.getElementById("dhcp");
    var dns = document.getElementById("dns");
    var dhcp = document.getElementById("tftp");
    if (dns.style.display === "none") {
        tftp.style.display = "block";
        dns.style.display = "none";
        dhcp.style.display = "none";
    } else {
        dns.style.display = "block";
    }
}
function mostrarDHCP() {
    var tftp = document.getElementById("dhcp");
    var dns = document.getElementById("dns");
    var dhcp = document.getElementById("tftp");
    if (dhcp.style.display === "none") {
        tftp.style.display = "none";
        dns.style.display = "none";
        dhcp.style.display = "block";
    } else {
        dhcp.style.display = "block";
    }
}

function tftpBackup(){
    var e = document.getElementById("routers");
    var seleccionado = e.options[e.selectedIndex].value;

    alert("Router seleccionado: " + seleccionado);
    
}