import folium
from geopy.geocoders import Bing
from geopy.exc import  GeocoderTimedOut
from geopy.exc import GeocoderServiceError


def main(year):
    """
    int -> dict

    Transorm file to a needed year and needed style.
    """
    file = open("docs/locations.list", "r", encoding = "UTF-8", errors = "ignore")
    films = file.readlines()[14:-2:]
    films1 = []
    for i in range(len(films)):
        if ("(" + str(year) + ")") in films[i]:
            films[i] = films[i].split("\t")
            a = films[i][-1][:-1:]
            if "(" in films[i][-1]:
                a = films[i][-2][:-1:]
            films[i] = films[i][0].split(" (")
            films[i].append(a)
            a = films[i][1].split(")")
            try:
                b = int(a[0])
                
            except ValueError as error:
                b = 0
                
            films[i][1] = b
            if len(films[i][-1].split(",")) > 2:
                a = films[i][-1].split(",")[-2::]
                r = str()
                for o in range(len(a) - 1):
                    r += a[o] + ","
                r += a[-1]
                r = r.strip(" ")
                films[i][-1] = r
                
            m = films[i][-1]
            films[i] = films[i][:2:]
            films[i].append(m)
            films1.append(films[i])
            
    places = {}
    
    for i in films1:
        if not i[2] in places:
            places[i[2]] = str(i[0]) + " || "
            
        elif not i[0] in places[i[2]]:
            a = places[i[2]]
            a += str(i[0]) + " || "
            places[i[2]] = a
            
    return places

def add_film(filminf):
    """
    list -> None

    Making markers about given info on map.
    """
    try:
        location = geolocator.geocode(filminf[0])
        map.add_child(folium.Marker(location = [location.latitude + filminf[-3], location.longitude + filminf[-3]],
                      popup=str(filminf[2]) + ":  " + filminf[1],
                      icon=folium.Icon(color=filminf[-1], icon_color=filminf[-2], icon= "cloud")))

    except IndexError as error:
        pass
    except AttributeError as error:
        pass
    except GeocoderTimedOut as error:
        pass
    except GeocoderServiceError as error:
        pass


def add_population():
    """
    None -> None

    Adding population of biggest cities to our HTML map.
    """
    try:
        file = open("docs/crowdedcitites.txt", "r", encoding="UTF-8")
        humans = file.readlines()[:-1:]
        for human in humans:
            human = human.split("\t")
            for info in range(len(human)):
                human[info] = human[info].strip(" ")
                
            human[0] = human[1] + ", " + human[2]
            location = geolocator.geocode(human[0])
            map.add_child(folium.CircleMarker(location=[location.latitude - 0.5, location.longitude - 0.5],
                                              popup = str("population of" + human[2] + "2018: " + human[3])
                                                      +"suburbs of city: " + str(human[3]),
                                              color = "red",
                                              fill_opacity = 0.3,
                                              radius=20,
                                              fill_color = "red"))
            
    except GeocoderTimedOut as error:
        pass
    except GeocoderServiceError as error:
        pass


if __name__ == "__main__":
    map = folium.Map()

    geolocator = Bing(api_key="Ag0zrFeOxLpmBE5EdTPEQp2laoQ8HoaXLEHObPUMdWhm1RF_QbCG5v64zk1eGJft ")

    year = int(input("Year of films u want to see on map(1890-2019): "))

    a = str(input("Do you want to see one more year of films on the map(Write Yes or No)? - "))
    if a == "Yes":
        year1 = int(input("Year of films u want to see on map(1890-2019): "))

    b = str(input("Do you want to see the most inhabited regions(write Yes or No)? - "))

    miss = 0
    places = main(year)
    for place in places:
        add_film([place, places[place], year, miss, "blue", "black"])
        
    if a == "Yes":
        places = main(year1)
        miss += 0.2
        for place in places:
            add_film([place, places[place], year1, miss, "yellow", "green"])
            
    if b == "Yes":
        add_population()
    map.save('Map_1.html')

