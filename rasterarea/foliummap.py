import folium
class Map(folium.Map):
    """ Create a folium map object.

    Args:
        folium: Creates a map in Folium 
    """
    def __init__(self, center=[20,0], zoom=2, **kwargs) -> None:
        """

        Args:
            center (list, optional): The Map Center. Defaults to [20,0].
            zoom (int, optional): Sets the zoom level of the map. Defaults to 2.
        """
        super().__init__(location=center, zoom_start=zoom, **kwargs)

    def add_tile_layer(self, url, name, attribution = "", **kwargs):
        """Adds a tile layer to the map.

        Args:
            url (str): The URL of the tile layer.
            name (str): The name of the tile layer
            attribution (str, optional): The attribution of the tile layer. Defaults to **
            """
        tile_layer = folium.TileLayer(
            tiles= url,
            name = name,
            attr = attribution,
            **kwargs
        )
        self.add_child(tile_layer)

    def add_basemap(self, basemap, **kwargs):   
        """Adds a basemap to the map

        Args:
            basemap: The basemap to add

        Raises:
            ValueError: Incorrect Basemap
        """
        import xyzservices.providers as xyz

        if basemap.lower() == 'roadmap':
            url = 'http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs ) 
        elif basemap.lower() == 'satellite':
            url = 'http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs)
        else:
            try:
                basemap = eval(f"xyz.{basemap}")
                url = basemap.build_url()
                attribution = basemap.attribution 
                self.add_tile_layer(url, name =basemap.name, attribution=attribution, **kwargs)
            except:
                raise ValueError(f"Basemap '{basemap}' not found")

    def add_geojson(self, data, name="GeoJSON", **kwargs):
        """Adds a GeoJSON layer to the map.

        Args:
            data (dict): The GeoJSON data.
            """

        if isinstance(data, str):
            import json
            with open(data, "r") as f:
                data = json.load(f)

        geojson = folium.GeoJson(data=data, name=name,**kwargs)
        geojson.add_to(self)

    def add_shp(self, data, name='Shapefile', **kwargs):
        """Adds a Shapefile layer to the map.

        Args:
            data (str): the path to the Shapefile.
        """
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name=name, **kwargs)

    def add_vector(self, data, name = 'Vector Data', **kwargs):
        """Adds Vector Data to the map.

        Args:
            data (str): the path to the Vector Data
            """
        import geopandas as gdp
        gdf = gdp.read_file(data)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name = name, **kwargs)