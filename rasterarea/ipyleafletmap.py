import ipyleaflet
from ipyleaflet import WidgetControl
import ipywidgets as widgets
class Map(ipyleaflet.Map):
    
    def __init__(self, center=[20, 0], zoom=2, **kwargs) -> None:

        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        super().__init__(center=center, zoom=zoom, **kwargs)

        if "height" not in kwargs:
            self.layout.height = "500px"
        else:
            self.layout.height = kwargs["height"]

        if "fullscreen_control" not in kwargs:
            kwargs["fullscreen_control"] = True
        if kwargs["fullscreen_control"]:
            self.add_fullscreen_control()
        
        if "layers_control" not in kwargs:
            kwargs["layers_control"] = True
        if kwargs["layers_control"]:
            self.add_layers_control()

    def add_search_control(self, position="topleft", **kwargs):
        """Adds a search control to the map.

        Args:
            kwargs: Keyword arguments to pass to the search control.
        """
        if "url" not in kwargs:
            kwargs["url"] = 'https://nominatim.openstreetmap.org/search?format=json&q={s}'
    

        search_control = ipyleaflet.SearchControl(position=position, **kwargs)
        self.add_control(search_control)

    def add_draw_control(self, **kwargs):
        """Adds a draw control to the map.

        Args:
            kwargs: Keyword arguments to pass to the draw control.
        """
        draw_control = ipyleaflet.DrawControl(**kwargs)

        draw_control.polyline =  {
            "shapeOptions": {
                "color": "#6bc2e5",
                "weight": 8,
                "opacity": 1.0
            }
        }
        draw_control.polygon = {
            "shapeOptions": {
                "fillColor": "#6be5c3",
                "color": "#6be5c3",
                "fillOpacity": 1.0
            },
            "drawError": {
                "color": "#dd253b",
                "message": "Oups!"
            },
            "allowIntersection": False
        }
        draw_control.circle = {
            "shapeOptions": {
                "fillColor": "#efed69",
                "color": "#efed69",
                "fillOpacity": 1.0
            }
        }
        draw_control.rectangle = {
            "shapeOptions": {
                "fillColor": "#fca45d",
                "color": "#fca45d",
                "fillOpacity": 1.0
            }
        }

        self.add_control(draw_control)

    def add_layers_control(self, position="topright"):
        """Adds a layers control to the map.

        Args:
            kwargs: Keyword arguments to pass to the layers control.
        """
        layers_control = ipyleaflet.LayersControl(position=position)
        self.add_control(layers_control)

    def add_fullscreen_control(self, position="topleft"):
        """Adds a fullscreen control to the map.

        Args:
            kwargs: Keyword arguments to pass to the fullscreen control.
        """
        fullscreen_control = ipyleaflet.FullScreenControl(position=position)
        self.add_control(fullscreen_control)

    def add_tile_layer(self, url, name, attribution="", **kwargs):
        """Adds a tile layer to the map.

        Args:
            url (str): The URL template of the tile layer.
            attribution (str): The attribution of the tile layer.
            name (str, optional): The name of the tile layer. Defaults to "OpenStreetMap".
            kwargs: Keyword arguments to pass to the tile layer.
        """
        tile_layer = ipyleaflet.TileLayer(url=url, attribution=attribution, name=name, **kwargs)
        self.add_layer(tile_layer)

    def add_basemap(self, basemap, **kwargs):

        import xyzservices.providers as xyz

        if basemap.lower() == "roadmap":
            url = 'http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs)
        elif basemap.lower() == "satellite":
            url = 'http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs)
        else:
            try:
                basemap = eval(f"xyz.{basemap}")
                url = basemap.build_url()
                attribution = basemap.attribution
                self.add_tile_layer(url, name=basemap.name, attribution=attribution, **kwargs)
            except:
                raise ValueError(f"Basemap '{basemap}' not found.")

    def add_geojson(self, data, name='GeoJSON', **kwargs):
        """Adds a GeoJSON layer to the map.

        Args:
            data (dict): The GeoJSON data.
        """
        if isinstance(data, str):
            import json
            with open(data, "r") as f:
                data = json.load(f)
        geojson = ipyleaflet.GeoJSON(data=data,name=name, **kwargs)
        self.add_layer(geojson)

    
    def add_shp(self, data, name='Shapefile', **kwargs):
        """Adds a Shapefile layer to the map.

        Args:
            data (str): The path to the Shapefile.
        """
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name=name, **kwargs)

    def add_vector(self, data, name='Vector', **kwargs):
        """Adds a vector layer to the map.

        Args:
            data (str): The path to the vector file.
        """
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name=name, **kwargs)

    def add_raster(self, url, name='Raster', fit_bounds=True, **kwargs):
        """Adds a raster layer to the map.

        Args:
            url (str): The URL of the raster layer.
            name (str, optional): The name of the raster layer. Defaults to 'Raster'.
            fit_bounds (bool, optional): Whether to fit the map bounds to the raster layer. Defaults to True.
        """
        import httpx

        titiler_endpoint = "https://titiler.xyz"

        r = httpx.get(
            f"{titiler_endpoint}/cog/info",
            params = {
                "url": url,
            }
        ).json()

        bounds = r["bounds"]

        r = httpx.get(
            f"{titiler_endpoint}/cog/tilejson.json",
            params = {
                "url": url,
            }
        ).json()

        tile = r["tiles"][0]

        self.add_tile_layer(url=tile, name=name, **kwargs)

        if fit_bounds:
            bbox = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]
            self.fit_bounds(bbox)

    def add_image(self, url, width, height, position = 'bottomright',**kwargs):
        """Add an image to the map.

        Args:
            url (str): The URL of the image.
            width (int): The width of the image.
            height (int): The height of the image.
            position (str, optional): The position of the image. Defaults to 'bottomright'.
        """
        widget = widgets.HTML(value = f'<img src="{url}" width="{width}" height="{height}">')
        control = WidgetControl(widget=widget, position=position)
        self.add(control)