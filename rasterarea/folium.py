import folium

class Map(folium.Map):
    """Create a folium map object.

    Args:
        folium (_type_): _description_
    """    
    def __init__(self, center=[20, 0], zoom=2, **kwargs) -> None:
        """Initializes the map object.

        Args:
            center (list, optional): The map center. Defaults to [20, 0].
            zoom (int, optional): The zoom level. Defaults to 2.
        """
        super().__init__(location=center, zoom_start=zoom, **kwargs)


    def add_tile_layer(self, url, name, attribution="", **kwargs):
        """Adds a tile layer to the map.

        Args:
            url (str): The URL of the tile layer.
            name (str): The name of the tile layer.
            attribution (str, optional): The attribution of the tile layer. Defaults to "".
        """
        tile_layer = folium.TileLayer(
            tiles=url,
            name=name,
            attr=attribution,
            **kwargs
        )
        self.add_child(tile_layer)
    
    def add_geojson_layer(self, data, name, **kwargs):
        """Adds a geojson layer to the map.

        Args:
            data (dict): The geojson data.
            name (str): The name of the layer.
        """
        geojson_layer = folium.GeoJson(
            data=data,
            name=name,
            **kwargs
        )
        self.add_child(geojson_layer)
    
    def add_base_layer(self, layer, name):
        """Adds a layer to the map.

        Args:
            layer (folium.Layer): The layer to add.
            name (str): The name of the layer.
        """
        self.add_child(layer)
        self.add_child(folium.LayerControl())
    
    def add_shp_layer(self, path, name, **kwargs):
        """Adds a shapefile layer to the map.

        Args:
            path (str): The path to the shapefile.
            name (str): The name of the layer.
        """
        shp_layer = folium.features.GeoJson(
            data=path,
            name=name,
            **kwargs
        )
        self.add_child(shp_layer)