import requests


class BadMapRequest(Exception):
    def __init__(self, request, response, params=None):
        self.request = request
        self.response = response
        self.params = params

    def __str__(self):
        if not self.params:
            print("Ошибка выполнения запроса:")
            print(self.request)
            print("Http статус:", self.response.status_code, "(", self.response.reason, ")")
        else:
            print("Ошибка выполнения запроса:")
            print(self.request, ' '.join(self.params.items()))
            print("Http статус:", self.response.status_code, "(", self.response.reason, ")")


class MapResponse:
    def __init__(self, json_response: dict):
        self.response = json_response
        self.toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        self.position = list(self.toponym["Point"]["pos"].split())
        self.lower_corner = list(self.toponym["boundedBy"]["Envelope"]["lowerCorner"].split())
        self.upper_corner = list(self.toponym["boundedBy"]["Envelope"]["upperCorner"].split())


def geocoder_request(toponym_to_find: str, *params) -> {}:

    '''
    Функция запроса геокодеру
    :param toponym_to_find: Строка с названием объекта, например, "Красная площадь"
    :param params: Параметры карты в формате "ключ=значение"
    :return: json найденного объекта или координаты на карте
    '''

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"
    }

    for i in params:
        k, v = i.split('=')
        geocoder_params[k] = v

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        raise BadMapRequest(geocoder_api_server, response, geocoder_params)

    return response.json()


def static_request(coords: list, *params):
    static_api_server = "https://static-maps.yandex.ru/1.x/"

    static_params = {
        "ll": ','.join(coords),
        'size': '450,450',
        'l': 'map'
    }

    for i in params:
        k, v = i.split('=')
        static_params[k] = v

    response = requests.get(static_api_server, params=static_params)

    if not response:
        raise BadMapRequest(static_api_server, response, static_params)

    return response


def get_mid(cords_1, cords_2):
    x1 = float(cords_1[0])
    y1 = float(cords_1[1])
    x2 = float(cords_2[0])
    y2 = float(cords_2[1])
    return [str((x1+x2) / 2), str((y1+y2) / 2)]


def get_map_with_route(point_a: str, point_b: str):
    point_a = MapResponse(geocoder_request(point_a))
    point_b = MapResponse(geocoder_request(point_b))
    map_coords = get_mid(point_a.position, point_b.position)
    param = f"pt=" + ','.join(point_a.position) + ",pmwtm1~" + ','.join(point_b.position) + ",pmwtm2"
    response = static_request(map_coords, param)
    return response.request.url

















