
from bs4 import BeautifulSoup
import urllib
import socket


resultxss={}
def xssatack(url):
	param='<marquee>Hack</marquee>' #paramatro para probar

	fullurl=url+param
	content=urllib.urlopen(fullurl).read() #genera un contenido con todo el html
	resultxss["urlifectada"]=fullurl

	#resive content , y el formato
	fullbody=BeautifulSoup(content,'html.parser')
	var=fullbody.find_all('marquee')

	if not var:
		if "HTTP 500" in fullbody:
			resultxss["HTTP500"]="HTTP 500"

		resultxss["vulnerable"]="not vulnerable"

	for r in var:
		if r.string=='Hack':
			resultxss["vulnerable"]="is vulnerable"
		else:
			resultxss["vulnerable"]="not vulnerable"





	return resultxss

resultlinks={}
def  linkscaidossin(url):
	fullurl=url
	content=urllib.urlopen(fullurl).read() #genera un contenido con todo el html
	fullbody= str(content)
	#obtener la instanaci de beatifull con el hmtl devuelto y parseado
	bs=BeautifulSoup(fullbody,'html.parser')
	#busqueda de lo que se injecto
	var=bs.find_all('a')
	con=1
	error=0

	for r in var:

		fullurl=reconstructorenlaces(url,str(r.get('href')))
		content=urllib.urlopen(fullurl).read() #genera un contenido con todo el html
		fullbody=BeautifulSoup(content,'html.parser')
		
		#print fullbody
		if "404" in fullbody:
			print "entro"
			resultlinks[r]=r
			print "error"+ str(urltotal) + str(fullbody)
			error=error+1



		if r.get('href')=="#":
			print "entro "+str(r)
			resultlinks[r]=str(r)
			error=error+1

		con=con+1

	total2=(float(error)/float(con))*float(100) 
	
	if error==100:
		total2=0

	resultlinks["afectacion"]=total2

	print "afeto en "+ str(total2)

	return resultlinks



def reconstructorenlaces(enlace,href):
	listan=enlace.split('/')

	listan[len(listan)-1]=href
	caracter=""
	contador=1
	for n in listan:
		if contador<len(listan):
			caracter=caracter+n+'/'

		else:
			caracter=caracter+n

		contador=contador+1


	return caracter


#diccionario
result={}
portopen=[]
def checkvulnner(banner,port):
	banners=open('vulnerables.txt','r')
	result
	for line in banners.readline():
		portopen.append(port)
		result[port]=banner
		if line.strip('\n') == banner:
			result["vulnerable"]="is vulnerable"
			print  line.strip('\n') 



	return 'not vulnerable'

		


def conecctar(dominio):
	#darle formato al dominio
	real=dominio.split('http://')
	realdomain=real[1].split('/')

	domainfull= realdomain[0].split(':')
	
	ipadd=socket.gethostbyname(domainfull[0])

	#tiempo de conexion de espera

	socket.setdefaulttimeout(2)

	ports=open('ports.txt','r')

	for line in ports:
		try:
			s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.connect((ipadd,int(line)))
			s.send("GET / HTTP/1.0\r\n\r\n")
			banner=s.recv(1024)
			if banner :
				checkvulnner(banner,line)

			
		except:
			print 'port '+line+' closed'



	if result.get("vulnerable") is None:
		result["vulnerable"]="not vulnerable"

	result['ipes']=ipadd



	return result



resultado=[]
def pivoting(dominio):
	socket.setdefaulttimeout(2)
	real=dominio.split('http://')
	realdomain=real[1].split('/')

	domainfull= realdomain[0].split(':')

	
	addr=socket.gethostbyname(domainfull[0])#obtenemos ip la del domini

	listaips=addr.split(".")# para poder serpar ip
	#obtener el ip sin el segmento de red
	ipnueva=listaips[0]+'.'
	ipnueva=ipnueva+listaips[1]+'.'
	ipnueva=ipnueva+listaips[2]
	resultado.append(addr)

	print 'la ip sin segmento de red es ' +ipnueva
	con=1
	error=0

	for host in range(50,60):
		ipcompleta=ipnueva+'.'+str(host)
		try:
			s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.connect((ipcompleta,80))

			s.send("GET / HTTP/1.0\r\n\r\n")#se le eniva al servidor una cabezera
			ans=s.recv(1024)
			if not ans:# si esta funcionando algo 
				print 'no hubo respuesta'

			else:
				print 'hubo respuesta de '+str(ipcompleta)
				resultado.append(ipcompleta)
				error=error+1

		except Exception as e:
			print  'no hay respuesta de '+ipcompleta

		con=con+1

	total=(float(error)/float(con))*100

	resultado.append(total)
	return resultado
