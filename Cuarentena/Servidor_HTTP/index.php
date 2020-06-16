<!-- #######  THIS IS A COMMENT - Visible only in the source editor #########-->
<html>
    <head>
    <link rel="stylesheet" href="css/styles.css"/>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Karma">
    <style>
        body,h1,h2,h3,h4,h5,h6 {font-family: "Karma", sans-serif}
    </style>
    </head>

    <body class="w3-black">
    <?php
	if(array_key_exists('tftpBtn',$_POST)){ tftp();}
	else if(array_key_exists('dnsBtn',$_POST)){ dns();}
	else if(array_key_exists('dhcpBtn',$_POST)){ dhcp();}
	function tftp(){
		$router = $_POST['routers'];
		shell_exec("python3 /var/www/html/Script/conectarTelnet.py");
		alert("Archivo de router $router recuperado");
	}
	function dns(){
		$dominio = $_POST['dominio'];
		$ip = $_POST['ip'];
		$zonei = $_POST['zonei'];
		shell_exec("python3 /var/www/html/Script/DNS.py");
		alert("Nuevo dominio agregado");
	}
	function dhcp(){
		shell_exec("python3 /var/www/html/Script/DHCP.py");
		alert("Nueva subred agregada");
	}
	function alert($msg){
		echo "<script type'text/javascript'>alert('$msg');</script>";
	}
	
    ?>        
        <header class="w3-container w3-center w3-padding-48 w3-white">
          <h1 class="w3-xxxlarge"><b>Gestor de protocolos</b></h1>
          <h6><span class="w3-tag"> TFTP, DNS, DHCP</span></h6>
        </header>
    <center>
        <script src="js/funciones.js"></script>
        
        <h2>
            Las configuraciones posibles serán:
        </h2>
        <p>
            &nbsp&nbsp&nbsp&nbsp&nbsp TFTP: Permite hacer la copia de seguridad de los routers.
        </p>
        <p>
            &nbsp&nbsp&nbsp&nbsp&nbsp DNS: Agregar una nueva entrada en la tabla de zona directa e inversa.
        </p>
        <p>
            &nbsp&nbsp&nbsp&nbsp&nbsp DHCP: Agregar una subred gestionando el rango de redes.
        </p>
    </center>
    <center>
        <table class="Table">
            <tbody>
                <tr>
                    <td><strong>Protocolo &nbsp&nbsp&nbsp&nbsp&nbsp   </strong></td>
                    <td><strong> &nbsp&nbsp&nbsp&nbsp&nbsp</strong></td>
                </tr>
                <tr>
                    <td>TFTP</td>
                    <td>
                        <button class="w3-button w3-light-grey w3-padding-large w3-section" onclick="mostrarTFTP()">Seleccionar</button>
                    </td>
                </tr>
                <tr>
                    <td>DNS</td>
                    <td>
                        <button class="w3-button w3-light-grey w3-padding-large w3-section" onclick="mostrarDNS()">Seleccionar</button>
                    </td>
                </tr>
                <tr>
                    <td>DHCP</td>
                    <td>
                        <button class="w3-button w3-light-grey w3-padding-large w3-section" onclick="mostrarDHCP()">Seleccionar</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </center>

    <center>
        <div id="tftp" style="display:none;">
	<form action="index.php" method="post" >
            <p>Selecciona un router al cual hacerle backup</p>
            <select id="routers" name="routers">
                <option value="1">Router 1</option>
                <option value="2" selected="selected">Router 2</option>
                <option value="3">Router 3</option>
            </select>
            <br>
            <br>
	    <input type="submit" id="tftpBtn" name="tftpBtn" value="Execute" />
	</form>
        </div>
    </center>

    <center>
        <div id="dns" style="display:none;">
	<form action="index.php" method="post" >
            <p></p>
            Has seleccionado DNS, aquí puedes agregar una entrada de red para Zona directa
            y zona inversa.
            <p></p>
            Ingresa el nombre de la ip (Ej. pcn.prueba.com): 
            <input type="text" name="dominio"><br>
            Ingresa la direccion ip a nombrar:
            <input type="text" name="ip"><br>
            Ingresa identificador para la Zona inversa:
            <input type="text" name="zonei">
            <br>
            <br>
	    <input type="submit" id="dnsBtn" name="dnsBtn" value="Execute" />
	</form>            
        </div>
    </center>
    
    <center>
        <div id="dhcp" style="display:none;">
	<form action="index.php" method="post" >
            <p></p>
            Has seleccionado DHCP, aquí podras agregar una subred a la configuracion
            <p></p>
            Ingresa la subred: 
            <input type="text" name="subred"><br>
            Ingresa la mascara de subred:
            <input type="text" name="mascara"><br>
            Ingresa la puerta de enlace predeterminada:
            <input type="text" name="gateway"><br>
            Ingresa el rango que quieres asignar: &nbsp;
            <input type="text" name="rangomin" value="Ingresa ip minima"/>
            <input type="text" name="rangomax" value="Ingresa ip maxima"/>
            <br>
            <br>
	    <input type="submit" id="dhcpBtn" name="dhcpBtn" value="Execute" />
	</form>
        </div>
    </center>        
    </body>
</html>
