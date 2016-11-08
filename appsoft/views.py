# -*- coding: UTF-8 -*-

import urllib,urllib2,cookielib,httplib2
import attack
from bs4 import BeautifulSoup
from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse
from appsoft.models import tipo,ataque,aprobo








# Create your views here.



def inicio(request):
	pagina="index.html"
	return render(request,pagina)


	

def vistasqli(request):
	
	pagina="verificarsqli.html"
	creado=""
	resultado={}
	url=""

	if request.method == "POST": 
		url=request.POST['sqli']
		#me retorna un objeto

		urlsesion=request.POST['urlsession']
		user=request.POST['user']
		password=request.POST['password']
		
		if urlsesion == "":
			creado=sqliattack(url)
		else:
			
			resultado=sqlconsession(urlsesion,url,user,password)
			creado=resultado.get('vulnerable')
			errorhttp500=resultado.get("http500")

		
		request.session['vulnerable']=creado
		request.session['urlatacada']=url
		request.session['http500']=errorhttp500
			


	else:
		creado=""	
	return render(request, pagina,{"error":creado,"resultado":resultado, "url":url})



def infosqlinction(request):
	pagina="infosqli.html"
	vulnerable=""
	urlafectada=""
	error=""
	info=None

	try:
		vulnerable=request.session.get('vulnerable')
		urlafectada=request.session.get('urlatacada')
		info=ataque.objects.filter(id=1)
		error=request.session.get("http500")

		del request.session["vulnerable"]
		del request.session["urlatacada"]
		del request.session["http500"]

	except:
		return redirect('/sqli')


	return render(request,pagina,{"vulnerable":vulnerable, "url":urlafectada, "errorserver":error,"variable":info})






def  vistaxss(request):
	resultados={}
	pagina="verificaxss.html"
	if request.method == "POST": 
		url=request.POST['xss']
		#me retorna un objeto
		urlsesion=request.POST['urlsession']
		user=request.POST['user']
		password=request.POST['password']

		if urlsesion == "":
			resultados=attack.xssatack(url)
		else:
			
			resultados=xssconsession(urlsesion,url,user,password)
	
		creado=resultados.pop("vulnerable")	

		request.session["vulnerable"] = creado
		request.session["url"]=resultados["urlifectada"]
		if 'HTTP500' in resultados:	
			request.session["HTTP500"]=resultados["HTTP500"]

	else:
		creado=""

	

	return render(request, pagina,{"error":creado, "resultados":resultados})



def vistaserver(request):
	result={}
	creado="incializado"
	pagina="verificarserver.html"
	if request.method == "POST": 
		server=request.POST['server']
		#me retorna un objeto
		

		result=attack.conecctar(server)
		creado=result.pop("vulnerable")

		request.session["resultadoserver"]=result 
		request.session["vulnerable"]=creado
		request.session['ipescaneada']=result.get('ipes')
		del result['ipes']


	else:
		creado=""

	return render(request, pagina,{"error":creado, "resultado" :result})


def infoserver(request):
	pagina=""
	info=None
	resultado=None
	error=None
	creado=""

	try:

		resultado=request.session.get('resultadoserver')
		creado=request.session.get('vulnerable')
		pagina="infoserver.html"
		info=ataque.objects.filter(id=4)
		ip=request.session.get('ipescaneada')





	except:
		return redirect('/server')


	return render(request,pagina,{"vulnerable":creado, "resultado": resultado,"variable":info,"ip":ip } )





def vistainfosqli(request):
	try:
		url=request.session.get("url")
		vulnerable=request.session.get("vulnerable")
		errorserver=""
		if 'HTTP500' in request.session:
			errorserver=request.session.get("HTTP500")
			del request.session["HTTP500"]

		del request.session["vulnerable"]
		del request.session["url"]
		pagina="infoxss.html"


		sqli=ataque.objects.filter(id=2)
	except:
		 return redirect('/xss')

	return render(request,pagina,{"variable":sqli,"url":url,"vulnerable":vulnerable,"errorserver":errorserver})



def vistapivoting(request):
	objeto=None
	result=[]
	pagina="verificarpivoting.html"
	creado="iniciado"
	if request.method == "POST": 
		server=request.POST['server']
		#me retorna un objeto
		

		result=attack.pivoting(server)
		print str(len(result)) +'tamaño de la lista'
		if len(result)>1:
			creado="is vulnerable"
			#eliminamos el ultimo que es le porcentaje para que no se pinte
			objeto=result[len(result)-1]
			result.remove(objeto)
			print "el porcentaje es "+ str(objeto)
		else:
			creado="not vulnerable"


		request.session["iprevisada"]=result[0]
		request.session["vulpivoting"]=creado
		request.session["porcentaje"]=objeto
	else:
		creado=""


	return render(request,pagina,{"resultado":result,"error":creado})



def infopivoting(request):
	pagina="infopivoting.html"
	try:
		ip=request.session.get("iprevisada")
		vulnerable=request.session.get("vulpivoting")
		porcentaje=request.session["porcentaje"]
		del request.session["iprevisada"]
		del request.session["vulpivoting"]
		del request.session["porcentaje"]
		sqli=ataque.objects.filter(id=3)

	except:
		 return redirect('/pivoting')

	return render(request,pagina,{"vulnerable":vulnerable, "ip":ip,"variable":sqli,"porcentaje":porcentaje})


def vistalinkscaidos(request):
	resultados={}
	creado=""
	pagina="verificarlinks.html"
	if request.method == "POST": 
		url=request.POST['links']

		request.session['urlson']=url
		#me retorna un objeto
		urlsesion=request.POST['urlsession']
		user=request.POST['user']
		password=request.POST['password']

		if urlsesion == "":
			#sin session
			resultados=attack.linkscaidossin(url)

		else:
			
			resultados=linksconse(urlsesion,url,user,password)

		request.session["afectacion"]=resultados.get('afectacion')
		del resultados['afectacion']
		
	
		if len(resultados)>0:
			creado="is vulnerable"
		else:
			creado="not vulnerable"


		request.session["vulnerable"] = creado
		request.session["url"]=url
		

	else:
		creado=""



	request.session['vulnerable']=creado

	

	return render(request, pagina,{"error":creado, "resultado":resultados})

def infolinks(request):
	pagina="infolinks.html"
	url=request.session.get('urlson')
	vulnerable=request.session.get('vulnerable')
	afectacion=request.session.get('afectacion')
	del request.session['vulnerable']
	del request.session['urlson']
	del request.session['afectacion']
	links=ataque.objects.filter(id=5)

	return render(request,pagina , {"pagina":url,"vulnerable":vulnerable,"variable":links,"afectacion":afectacion})














#pruebas

"""   
	UNION necesita algunos requisitos.
Necesitas meter la misma cantidad de valores que tiene la tabla.
Tener un informe de los errores que provocaremos en la instrucción 

' AND 0 UNION SELECT 1 AND 'l'='
al unir una columna con nada da error
error:
The used SELECT statements have a different number of column
"""

def sqliattack(fullurl):
	#fullurl url con el parametor al cual se quiere injectar
	resp = urllib.urlopen(fullurl + "=1\' or \'1\' = \'1\''") #variables que generan error en sql

	body = resp.read()#leo la respuesta de la web

	fullbody = body.decode("utf-8")#decodifico a utf-8

	if "You have an error in your SQL syntax" in fullbody:
		return 'is vulnerable' 
	else :
	#mas pruebas

		resp=urllib.urlopen(fullurl+"='AND 0 UNION SELECT 1 AND 'l'='")
		body=resp.read()
		fullbody=body.decode("utf-8")

		if "The used SELECT statements have a different number of column" in fullbody:
			return 'is vulnerable'
		else:
			return 'not vulnerable'	




#ataque sqli con inicio de sesion



resultado={}
def sqlconsession(urlsession,urlinjectar,user,password):
	

#es para iniciar sesion
	variables=nomvars(urlsession)
	

	http = httplib2.Http()

	
	body = {variables[0]: user, variables[1]: password}
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	response, content = http.request(urlsession, 'POST', headers=headers, body=urllib.urlencode(body))

	headers = {'Cookie': response['set-cookie']}

  	fullurl=urlinjectar+"='"
	response, content = http.request(fullurl, 'GET', headers=headers)
	fullbody= str(content)
	print "html :    "+fullbody
	if "500" in fullbody:

		resultado["vulnerable"]='is vulnerable'
		resultado["http500"]="error 500"

	if "You have an error in your SQL syntax" in fullbody:
		resultado["vulnerable"]='is vulnerable'
	else :
		http = httplib2.Http()

	
		body = {variables[0]: user, variables[1]: password}
		headers = {'Content-type': 'application/x-www-form-urlencoded'}
		response, content = http.request(urlsession, 'POST', headers=headers, body=urllib.urlencode(body))

		headers = {'Cookie': response['set-cookie']}
		fullurl=urlinjectar+"='AND 0 UNION SELECT 1 AND 'l'='"
		response, content = http.request(fullurl, 'GET', headers=headers)
		fullbody= str(content)
		if "The used SELECT statements have a different number of column" in fullbody:
			resultado["vulnerable"]='is vulnerable'

		elif "HTTP 500" in fullbody:
			resultado["vulnerable"]='is vulnerable'
			resultado["http500"]="error 500"
	
		vul=resultado.get('vulnerable')
		if vul:
			resultado["vulnerable"]='is vulnerable'
		else:

			resultado["vulnerable"]='notvulnerable'

		return resultado
	

resultxss={}
def xssconsession(urlsession,urlinjectar,user,password):
	#obtenemos variables que se enivan por post
	variables=nomvars(urlsession)
	
	#
	http = httplib2.Http()
	#creo el body de las variables que se envian
	
	body = {variables[0]: user, variables[1]: password}
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	#realizo peticion al servidor y recibo encabezado y el contenido en html
	response, content = http.request(urlsession, 'POST', headers=headers, body=urllib.urlencode(body))
	#cookies para usar session
	headers = {'Cookie': response['set-cookie']}
	#url completa para probar
  	fullurl=urlinjectar+"<marquee>Hack<marquee>"
  	#devuelve un contenido

  	resultxss["urlifectada"]=fullurl
	response, content = http.request(urlinjectar, 'GET', headers=headers)
	#parseo a string por si
	fullbody= str(content)
	#obtener la instanaci de beatifull con el hmtl devuelto y parseado
	bs=BeautifulSoup(fullbody,'html.parser')
	#busqueda de lo que se injecto
	var=bs.find_all('marquee')
	#si esta vacia verifica si hay control de errores 
	if not var:
		if "HTTP 500"  in fullbody:
			resultxss["HTTP500"]="HTTP 500"
			resultxss["vulnerable"]="is vulnerable"
		elif "403" in fullbody:
			resultxss["HTTP500"]="HTTP 403"
			resultxss["vulnerable"]="is vulnerable"
		elif "402" in fullbody:
			resultxss["HTTP500"]="HTTP 402"
			resultxss["vulnerable"]="is vulnerable"

		elif "404" in fullbody:
			resultxss["HTTP500"]="HTTP 404"
			resultxss["vulnerable"]="is vulnerable"

		elif "501" in fullbody:
			resultxss["HTTP500"]="HTTP 501"
			resultxss["vulnerable"]="is vulnerable"
		elif "502" in fullbody:
			resultxss["HTTP500"]="HTTP 502"
			resultxss["vulnerable"]="is vulnerable"
		elif "503" in fullbody:
			resultxss["HTTP500"]="HTTP 503"
			resultxss["vulnerable"]="is vulnerable"

	for r in var:
		if r.string=='Hack':
			resultxss["vulnerable"]="is vulnerable"
		else:
			resultxss["vulnerable"]="not vulnerable"


	return resultxss


resultlinks={}
def linksconse(urlsession,urlinjectar,user,password):

	
	#obtenemos variables que se enivan por post
	
	variables=nomvars(urlsession)

	
	#
	http = httplib2.Http()
	#creo el body de las variables que se envian
	
	body = {variables[0]: user, variables[1]: password}
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	#realizo peticion al servidor y recibo encabezado y el contenido en html
	response, content = http.request(urlsession, 'POST', headers=headers, body=urllib.urlencode(body))
	#cookies para usar session
	headers = {'Cookie': response['set-cookie']}
	#url completa para probar
  	fullurl=urlinjectar
  	#devuelve un contenido

  	#resultlinks["urverifi"]=fullurl
	response, content = http.request(urlinjectar, 'GET', headers=headers)
	#parseo a string por si
	fullbody= str(content)
	#obtener la instanaci de beatifull con el hmtl devuelto y parseado
	bs=BeautifulSoup(fullbody,'html.parser')
	#busqueda de lo que se injecto
	var=bs.find_all('a')
	#si esta vacia verifica si hay control de errores 
	
	con=1
	error=0

	for r in var:
		body = {variables[0]: user, variables[1]: password}
		headers = {'Content-type': 'application/x-www-form-urlencoded'}
		#realizo peticion al servidor y recibo encabezado y el contenido en html
		response, content = http.request(urlsession, 'POST', headers=headers, body=urllib.urlencode(body))
		#cookies para usar session
		headers = {'Cookie': response['set-cookie']}

		urltotal=reconstructorenlaces(urlinjectar,str(r['href']))
		response, content = http.request(urltotal, 'GET', headers=headers)
		#parseo a string por si
		fullbody= str(content)
		#print fullbody
		if "404" in fullbody:
			error=error+1
			print "entro"
			resultlinks[r]=r
			print "error"+ str(urltotal) + str(fullbody)


		if r['href']=="#":
			error=error+1
			print "entro "+str(r)
			resultlinks[r]=str(r)

		con=con+1


	total2=(float(error)/float(con))*float(100) 
	
	
	if error==0:
		total2=0

	resultlinks["afectacion"]=total2
		


	return resultlinks

	#darle  formato ala url


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






#retorna lista
def nomvars(fullurl):
	variables=[]
	
	content=urllib.urlopen(fullurl).read() #genera un contenido con todo el html

	#resive content , y el formato
	bs=BeautifulSoup(content,'html.parser')
	var=bs.find_all('input')
	variables.append(var[0]['name'])
	variables.append(var[1]['name'])

	return variables














