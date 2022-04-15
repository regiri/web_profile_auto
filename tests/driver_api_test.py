from requests import get

print(get('http://localhost:5000/api/drivers').json())
print(get('http://localhost:5000/api/drivers/1').json())
print(get('http://localhost:5000/api/drivers/10').json())
print(get('http://localhost:5000/api/drivers/qq').json())
