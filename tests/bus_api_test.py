from requests import get

print(get('http://localhost:5000/api/buses').json())
print(get('http://localhost:5000/api/buses/1').json())
print(get('http://localhost:5000/api/buses/10').json())
print(get('http://localhost:5000/api/buses/qq').json())
