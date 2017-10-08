import urllib.request as req

authed = req.urlopen('http://localhost:8080/auth?pass=SteveWTF')

while authed.status == 200:
    csrf = authed.read().decode('utf-8')
    authed = req.urlopen('http://localhost:8080/print?csrf={}&first_name=Mike&last_name=Swift&email=swift@mlh.io'.format(csrf))

print(authed.status)
print(authed.read())
