from requests import get

print(get('http://localhost:5000/api/routes').json())
print(get('http://localhost:5000/api/routes/1').json())
print(get('http://localhost:5000/api/routes/10').json())
print(get('http://localhost:5000/api/routes/qq').json())