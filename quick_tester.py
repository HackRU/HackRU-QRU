#import urllib.request as req
import urllib2 as req

authed = req.urlopen('http://localhost:8080/auth?pass=SteveWTF')

if authed.getcode() == 200:
    csrf = authed.read().decode('utf-8')
    try:
        authed = req.urlopen('http://localhost:8080/print?csrf={}&first_name=Steve&last_name=Hsu&email=triangular.pyramid@gmail.com'.format(csrf))
    except e:
        print e

print(authed.getcode())
print(authed.read())
