"""
    pass
"""

from cores.core_NOAA.change_weather import get_response_aiohttp


# Устанавливаем адрес запроса
async def decode_address(address: str):
    """
        pass
    """


# rer = [{'place_id': 342000301, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright',
#         'osm_type': 'way', 'osm_id': 1096999543, 'lat': '40.4385875', 'lon': '-86.91665347584745', 'class': 'building',
#         'type': 'house', 'place_rank': 30, 'importance': 0.3852629434778953, 'addresstype': 'building',
#         'name': 'Samara',
#         'display_name': 'Samara, Northwestern Avenue, West Lafayette, Tippecanoe County, Indiana, 46906, United States',
#         'boundingbox': ['40.4384700', '40.4387020', '-86.9167990', '-86.9164710']},
#        {'place_id': 89404154, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright',
#         'osm_type': 'way', 'osm_id': 179669434, 'lat': '49.9465464', 'lon': '2.178295983584313', 'class': 'tourism',
#         'type': 'theme_park', 'place_rank': 30, 'importance': 0.25960299066529513, 'addresstype': 'tourism',
#         'name': 'Samara',
#         'display_name': "Samara, Route d'Amiens, La Chaussée-Tirancourt, Amiens, Somme, Hauts-de-France, France métropolitaine, 80310, France",
#         'boundingbox': ['49.9437970', '49.9494225', '2.1670131', '2.1820668']},
#        {'place_id': 187449878, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright',
#         'osm_type': 'relation', 'osm_id': 3368701, 'lat': '53.2194648', 'lon': '50.2039316', 'class': 'place',
#         'type': 'city', 'place_rank': 16, 'importance': 0.6449450061537874, 'addresstype': 'city', 'name': 'Самара',
#         'display_name': 'Самара, городской округ Самара, Самарская область, Приволжский федеральный округ, 443028, Россия',
#         'boundingbox': ['53.0919014', '53.5509321', '49.7313889', '50.3903893']},
#        {'place_id': 54598559, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright',
#         'osm_type': 'way', 'osm_id': 74728345, 'lat': '44.8257406', 'lon': '24.714095', 'class': 'place',
#         'type': 'village', 'place_rank': 19, 'importance': 0.4164100037473589, 'addresstype': 'village',
#         'name': 'Sămara',
#         'display_name': 'Sămara, Poiana Lacului, Argeș, 117569, România',
#         'boundingbox': ['44.8224790', '44.8318520', '24.7112744', '24.7170210']},
#        {'place_id': 195024672, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright',
#         'osm_type': 'node', 'osm_id': 2480261764, 'lat': '34.2', 'lon': '43.9', 'class': 'place', 'type': 'city',
#         'place_rank': 16, 'importance': 0.5609307816610702, 'addresstype': 'city', 'name': 'سامراء',
#         'display_name': 'سامراء, ناحية مرکز قضاء سامراء, قضاء سامراء, محافظة صلاح الدين, 04002, العراق',
#         'boundingbox': ['34.0400000', '34.3600000', '43.7400000', '44.0600000']},
#        {'place_id': 218195655, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright',
#         'osm_type': 'node', 'osm_id': 5063856318, 'lat': '16.4066851', 'lon': '120.3327898', 'class': 'place',
#         'type': 'village', 'place_rank': 19, 'importance': 0.14672166857404437, 'addresstype': 'village',
#         'name': 'Samara', 'display_name': 'Samara, Aringay, La Union, Ilocos Region, 2503, Pilipinas',
#         'boundingbox': ['16.3866851', '16.4266851', '120.3127898', '120.3527898']},
#        {'place_id': 284975786, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright',
#         'osm_type': 'relation', 'osm_id': 6413424, 'lat': '9.8834197', 'lon': '-85.5288998', 'class': 'boundary',
#         'type': 'administrative', 'place_rank': 16, 'importance': 0.33973472073036687, 'addresstype': 'village',
#         'name': 'Sámara', 'display_name': 'Sámara, Cantón de Nicoya, Guanacaste, 50205, Costa Rica',
#         'boundingbox': ['9.8597185', '9.9634885', '-85.6369160', '-85.4627008']},
#        {'place_id': 187265215, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright',
#         'osm_type': 'relation', 'osm_id': 377931, 'lat': '52.6664095', 'lon': '52.3978605', 'class': 'waterway',
#         'type': 'river', 'place_rank': 18, 'importance': 0.4758467396969812, 'addresstype': 'river', 'name': 'Самара',
#         'display_name': 'Самара, Приволжский федеральный округ, Россия',
#         'boundingbox': ['51.8717949', '53.2426759', '50.0315666', '54.5019218']},
#        {'place_id': 178822367, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright',
#         'osm_type': 'relation', 'osm_id': 3278272, 'lat': '48.5354317', 'lon': '36.0283512', 'class': 'waterway',
#         'type': 'river', 'place_rank': 18, 'importance': 0.473842069505934, 'addresstype': 'river', 'name': 'Самара',
#         'display_name': 'Самара, Україна', 'boundingbox': ['48.3884322', '48.7747046', '35.1005992', '37.1869064']},
#        {'place_id': 191346124, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright',
#         'osm_type': 'node', 'osm_id': 8051251790, 'lat': '40.8863071', 'lon': '39.8573871', 'class': 'place',
#         'type': 'village', 'place_rank': 19, 'importance': 0.2535713079130456, 'addresstype': 'village',
#         'name': 'Gülyurdu', 'display_name': 'Gülyurdu, Yomra, Trabzon, Karadeniz Bölgesi, Türkiye',
#         'boundingbox': ['40.8663071', '40.9063071', '39.8373871', '39.8773871']}]

    url = f"https://nominatim.openstreetmap.org/search?format=json&q={address}"
    data = await get_response_aiohttp(url)  # Делаем GET запрос к API Nominatim
    print(data)

    # if data:
    #     latitude = str(data[0]['lat'])      # Преобразование широты в строку
    #     longitude = str(data[0]['lon'])     # Преобразование долготы в строку
    #
    #     print(f'Адрес декодирован, координаты: latitude - {latitude}, longitude - {longitude}')
    #
    # return latitude, longitude
