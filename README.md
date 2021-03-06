# Film Mapper

Film Mapper is a python module that maps movies with given parameters on a world map.


## Usage

```python
>>> import film_mapper as fm
>>> fm.main()
Reading CSV...
Read.
_______
Year: 2015
Location: 50.4420416584236, 30.518646242096857
Building a map at [50.4420416584236, 30.518646242096857] ...
Map saved at map.html
```

![alt text](screenshot.png)

## HTML Structure

Map generation taken care of automatically by [folium](https://python-visualization.github.io/folium/).

HTML map consists of 3 layers (main, selected location pin, movie pins). Updates with each run of the script at map.html.


## Goals and opportunities

Use this module to pinpoint the nearest movie filming spots for any given location around the globe.
It helps not only browse through the movies filmed in any country and period of time, but also visualise the moviemaking history both geographically and chronologically. Film Mapper can also provide high-quality HTML data for by-hand analysis of movies in their relation to countries, continents and time periods.


## License
[MIT](https://choosealicense.com/licenses/mit/)
