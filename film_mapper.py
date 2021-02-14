import random
import pandas
import folium
import geopy
from haversine import haversine

geolocator = geopy.Nominatim(user_agent="UCU OP Lab 2 Nefedov")

CLOSEST_FILENAME = "closest10.csv"

def gather_line_info(line):
    # print(line)
    try:
        movie_name = line.split("\"")[1]
    except IndexError:
        movie_name = line
    year = line[line.index("(")+1:line.index(")")]
    after_year = line[line.index(")") + 1:].strip()
    try:
        after_year = after_year.split("}")[1].strip()
    except IndexError:
        pass
    try:
        after_year = after_year.split("(")[0].strip()
    except IndexError:
        pass
    location = after_year
    location = location.replace(",", "_comma_")
    # location = geolocator.geocode(after_year)
    # print(location)
    # try:
    #     location = str(location.latitude) + " " + str(location.longitude)
    #     print(location)
    # except AttributeError:
    #     location = "ERROR"
    return movie_name, year, location

    # print("MOVIE NAME:", movie_name)
    # print("YEAR:", year)
    # print("LOCATION:", location)


def country_from_coordinates(coord_st):
    full_address = geolocator.reverse(coord_st, language="en").address
    # print("FULL ADDRESS:", full_address)
    return full_address.split(",")[-1].strip()


def filter_closest_movies(df: pandas.DataFrame, location: str, year, max_n=10):
    country = country_from_coordinates(location)
    if country == "United States":
        country = "USA"
    elif country == "United Kingdom":
        country = "UK"
    # print(year, country)

    df = df[(df["Year"] == str(year)) & (df["Location"].str.endswith(country))]
    # df = df[df["Year"] == str(year)]
    distances_to_input = []
    latitudes = []
    longitudes = []
    df = df.head(10)
    for item in df["Location"]:
        try:
            geocoded = geolocator.geocode(item)
            latitude, longitude = [float(x.strip()) for x in location.split(", ")]
            distances_to_input.append(haversine((geocoded.latitude, geocoded.longitude), (latitude, longitude)))
            latitudes.append(geocoded.latitude)
            longitudes.append(geocoded.longitude)
        except AttributeError:
            print("ERROR in", item)
            distances_to_input.append(None)
            latitudes.append(None)
            longitudes.append(None)
    df["Distance"] = distances_to_input
    df["Latitude"] = latitudes
    df["Longitude"] = longitudes
    df.dropna(inplace=True, how="any")

    movie_names = []
    movie_rows = []
    df = df.sort_values(by=["Distance"])
    for index, row in df.head(1000).iterrows():
        if not(any([movie_row["Movie"] == row["Movie"] for movie_row in movie_rows])) and row["Movie"] != "NaN" and row["Longitude"] != None:
            movie_rows.append(row)
            movie_names.append(row["Movie"])
        if len(movie_names) >= 10:
            break

    small_df = pandas.DataFrame(movie_rows)
    # print(small_df)
    small_df.head(10).to_csv(CLOSEST_FILENAME)


def read_data(filename):
    print("Reading CSV...")
    data = open(filename, "r", encoding="latin1")
    csv_data = open("locations.csv", "w")
    # csv_data.write("Name, Year, Location")
    for line in data.readlines()[14:-1]:
        line_st = ",".join(gather_line_info(line)) + "\n"
        csv_data.write(line_st)
    csv_data.close()
    df = pandas.read_csv("locations.csv", names=["Movie", "Year", "Location"], error_bad_lines=False,
                         warn_bad_lines=False)
    new_locations = []
    for item in df["Location"]:
        try:
            new_locations.append(item.replace("_comma_", ","))
        except AttributeError:
            new_locations.append(item)
    df["Location"] = new_locations
    return df


def change_coords_a_bit(coords, max_delta=0.05):
    new_x = coords[0] + random.random()*max_delta*random.choice([-1, 1])
    new_y = coords[1] + random.random() * max_delta * random.choice([-1, 1])
    return new_x, new_y


def build_map(closest_csv, aim_location):
    print("Building a map at", aim_location, "...")
    data = pandas.read_csv(closest_csv, error_bad_lines=False).head(100)
    lat = data['Latitude']
    lon = data['Longitude']
    map = folium.Map(location=aim_location, zoom_start=10)
    fg = folium.FeatureGroup(name="Map")
    for index, row in data.iterrows():
        # print("ROW:", row)
        lt, ln = row["Latitude"], row["Longitude"]
        # print("Lat Long Mov:", lt, ln, row["Movie"])
        try:
            fg.add_child(folium.Marker(location=change_coords_a_bit([lt, ln]),
                                       popup="{} ({})".format(row["Movie"], row["Year"]), icon=folium.Icon()))
        except ValueError:
            # print("NaN passed")
            pass

    fg.add_child(folium.Marker(location=aim_location,
                               popup="Selected Location", icon=folium.Icon(color="red")))

    map.add_child(fg)
    map.save('map.html')
    print("Map saved at map.html")


def main():
    df = read_data("locations.list")
    print(df.head(10))
    print("Read.\n_______")
    year = int(input("Year: "))
    location = input("Lat Long: ")
    filter_closest_movies(df, location, year)
    build_map(CLOSEST_FILENAME, [float(coord.strip()) for coord in location.split(",")])


if __name__ == "__main__":
    main()
    # from haversine import haversine
    # print(haversine((90.000, 90.000), (-90.000, -90.000)))
