import urllib, urllib2, cookielib

def main():
	username = 'myuser'
	password = 'mypassword'

	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	listica=metodo2()
	login_data = urllib.urlencode({listica[0] : 'gg@gmail.com', listica[1] : '1234567890'})
	opener.open('http://sandbox1.ufps.edu.co:8080/ufps_19-proyectoAn/login.jsp', login_data)
	resp = opener.open('http://sandbox1.ufps.edu.co:8080/ufps_19-proyectoAn/buscarReserva.jsp?cc=2')
	print resp.read()



def metodo2():
	variables=[]
	fullurl='http://sandbox1.ufps.edu.co:8080/ufps_19-proyectoAn/login.jsp'
	content=urllib.urlopen(fullurl).read() #genera un contenido con todo el html

	#resive content , y el formato
	bs=BeautifulSoup(content,'html.parser')
	var=bs.find_all('input')
	variables.append(var[0]['name'])
	variables.append(var[1]['name'])
	return variables
	

if __name__ == '__main__':
	main()