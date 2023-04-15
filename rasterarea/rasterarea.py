"""Main module."""

import random
import string
import math
import ipyleaflet

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

    def add_basemap(self, basemap):
        """Adds a basemap to the map.

        Args:
            basemap (str): The name of the basemap to add.
        """
        import xyzservices.providers as xyz
        try:
            layer = eval(f"xyz.{basemap}")
            url = layer.build_url()
            attribution = layer.attribution
            self.add_tile_layer(url=url, attribution=attribution, name=basemap)

        except:
            raise ValueError(f"Invalid basemap name: {basemap}")
    

    def add_geojson(self, data, **kwargs):
        """Adds a GeoJSON layer to the map.

        Args:
            data (dict): The GeoJSON data.
            kwargs: Keyword arguments to pass to the GeoJSON layer.
        """
        import json

        if isinstance(data, str):
            with open(data, "r") as f:
                data = json.load(f)

        geojson = ipyleaflet.GeoJSON(data=data, **kwargs)
        self.add_layer(geojson)
    
    def add_shapefile(self, data, **kwargs):
        """Adds a shapefile layer to the map.

        Args:
            data (str): The path to the shapefile.
            kwargs: Keyword arguments to pass to the shapefile layer.
        """
        import geopandas as gpd

        if isinstance(data, str):
            data = gpd.read_file(data)

        geojson = ipyleaflet.GeoJSON(data=data.__geo_interface__, **kwargs)
        self.add_layer(geojson)
    
    def add_vector(self, data, **kwargs):
        """Adds a vector layer to the map.

        Args:
            data (str): The path to the vector file.
            kwargs: Keyword arguments to pass to the vector layer.
        """
        import geopandas as gpd

        if isinstance(data, str):
            data = gpd.read_file(data)

        geojson = ipyleaflet.GeoJSON(data=data.__geo_interface__, **kwargs)
        self.add_layer(geojson)

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


def area_of_pixel(center_lat,pixel_size=1, coordinatesp = 'WGS84', **kwargs):
    """_summary_

    Args:
        center_lat (_type_): _description_
        pixel_size (int, optional): _description_. Defaults to 1.
        coordinatesp (str, optional): _description_. Defaults to 'WGS84'.

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """ 
    if coordinatesp== 'WGS84':
        a = 6378137
        b = 6356752.3142
    elif coordinatesp== 'WGS72':
        a = 6378135
        b = 6356750.5
    elif coordinatesp== 'WGS66':
        a = 6378145
        b = 6356759.769356
    elif coordinatesp== 'WGS60':
        a = 6378165
        b = 6356783.286959
    elif coordinatesp== 'IERS':
        a = 6378136.6
        b = 6356751.9
    elif coordinatesp== 'GRS80':
        a = 6378137
        b = 6356752.3141
    elif coordinatesp== 'GRS67':
        a = 6378160
        b = 6356774.51609
    elif coordinatesp== 'Krassovsky':
        a = 6378245
        b = 6356863.019
    else:
        raise ValueError(f"Invalid coordinatesp name: {coordinatesp}")

    c = math.sqrt(1 - (b/a)**2)
    zm_a = 1 - c*math.sin(math.radians(center_lat+pixel_size/2))
    zp_a = 1 + c*math.sin(math.radians(center_lat+pixel_size/2))
    area_a = math.pi * b**2 * (math.log(zp_a/zm_a) / (2*c) + math.sin(math.radians(center_lat+pixel_size/2)) / (zp_a*zm_a))
    zm_b = 1 - c*math.sin(math.radians(center_lat-pixel_size/2))
    zp_b = 1 + c*math.sin(math.radians(center_lat-pixel_size/2))
    area_b = math.pi * b**2 * (math.log(zp_b/zm_b) / (2*c) + math.sin(math.radians(center_lat-pixel_size/2)) / (zp_b*zm_b))
    area = (1 / 360 * (area_a - area_b))
    return area

def get_geotiff_info(geotiff_path, **kwargs):
    """Get information about a GeoTIFF file.

    Args:
        geotiff_path (str): The path to the GeoTIFF file.

    Returns:
        dict: A dictionary containing information about the GeoTIFF file.
    """
    import rasterio

    with rasterio.open(geotiff_path) as src:
        info = {
            "crs": src.crs,
            "count": src.count,
            "driver": src.driver,
            "dtype": src.dtypes[0],
            "height": src.height,
            "indexes": src.indexes,
            "nodata": src.nodata,
            "shape": src.shape,
            "transform": src.transform,
            "width": src.width,
        }

    return info

def get_geotiff_array(geotiff_path, band=1, **kwargs):
    """Get a NumPy array from a GeoTIFF file.

    Args:
        geotiff_path (str): The path to the GeoTIFF file.
        band (int, optional): The band to read. Defaults to 1.

    Returns:
        numpy.ndarray: A NumPy array containing the data from the GeoTIFF file.
    """
    import rasterio

    with rasterio.open(geotiff_path) as src:
        array = src.read(band)

    return array

def get_geotiff_bounds(geotiff_path, **kwargs):
    """Get the bounds of a GeoTIFF file.

    Args:
        geotiff_path (str): The path to the GeoTIFF file.

    Returns:
        tuple: A tuple containing the bounds of the GeoTIFF file.
    """
    import rasterio

    with rasterio.open(geotiff_path) as src:
        bounds = src.bounds

    return bounds

def get_geotiff_crs(geotiff_path, **kwargs):
    """Get the CRS of a GeoTIFF file.

    Args:
        geotiff_path (str): The path to the GeoTIFF file.

    Returns:
        rasterio.crs.CRS: A CRS object containing the CRS of the GeoTIFF file.
    """
    import rasterio

    with rasterio.open(geotiff_path) as src:
        crs = src.crs

    return crs

def get_geotiff_transform(geotiff_path, **kwargs):
    """Get the transform of a GeoTIFF file.

    Args:
        geotiff_path (str): The path to the GeoTIFF file.

    Returns:
        Affine: An Affine object containing the transform of the GeoTIFF file.
    """
    import rasterio

    with rasterio.open(geotiff_path) as src:
        transform = src.transform

    return transform

def get_geotiff_resolution(geotiff_path, **kwargs):
    """Get the resolution of a GeoTIFF file.

    Args:
        geotiff_path (str): The path to the GeoTIFF file.

    Returns:
        tuple: A tuple containing the resolution of the GeoTIFF file.
    """
    import rasterio

    with rasterio.open(geotiff_path) as src:
        resolution = (src.res[0], src.res[1])

    return resolution

def get_geotiff_nodata(geotiff_path, **kwargs):
    """Get the nodata value of a GeoTIFF file.

    Args:
        geotiff_path (str): The path to the GeoTIFF file.

    Returns:
        float: The nodata value of the GeoTIFF file.
    """
    import rasterio

    with rasterio.open(geotiff_path) as src:
        nodata = src.nodata

    return nodata

def get_geotiff_shape(geotiff_path, **kwargs):
    """Get the shape of a GeoTIFF file.

    Args:
        geotiff_path (str): The path to the GeoTIFF file.

    Returns:
        tuple: A tuple containing the shape of the GeoTIFF file.
    """
    import rasterio

    with rasterio.open(geotiff_path) as src:
        shape = src.shape

    return shape

def point_cloud_arrary(filepath, no_data=0, band=1, **kwargs):
    """_summary_

    Args:
        filepath (_type_): _description_
        no_data (int, optional): _description_. Defaults to 0.
        band (int, optional): _description_. Defaults to 1.

    Returns:
        _type_: _description_
    """
    import lidario as lio
    translator = lio.Translator("geotiff", "np")
    point_cloud = translator.translate(input_values=filepath, no_data=no_data, band=band)
    return point_cloud
    
def pixel_area_array(point_cloud_arrary, pixel_size=1, coordinatesp = 'WGS84', **kwargs):
    """_summary_

    Args:
        filepath (_type_): _description_
        no_data (int, optional): _description_. Defaults to 0.
        band (int, optional): _description_. Defaults to 1.

    Returns:
        _type_: _description_
    """

    """_summary_

    Args:
        center_lat (_type_): _description_
        pixel_size (int, optional): _description_. Defaults to 1.
        coordinatesp (str, optional): _description_. Defaults to 'WGS84'.

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """ 
    if coordinatesp== 'WGS84':
        a = 6378137
        b = 6356752.3142
    elif coordinatesp== 'WGS72':
        a = 6378135
        b = 6356750.5
    elif coordinatesp== 'WGS66':
        a = 6378145
        b = 6356759.769356
    elif coordinatesp== 'WGS60':
        a = 6378165
        b = 6356783.286959
    elif coordinatesp== 'IERS':
        a = 6378136.6
        b = 6356751.9
    elif coordinatesp== 'GRS80':
        a = 6378137
        b = 6356752.3141
    elif coordinatesp== 'GRS67':
        a = 6378160
        b = 6356774.51609
    elif coordinatesp== 'Krassovsky':
        a = 6378245
        b = 6356863.019
    else:
        raise ValueError(f"Invalid coordinatesp name: {coordinatesp}")
    raster_area = point_cloud_arrary
    for i in range(len(point_cloud_arrary)):
        center_lat = point_cloud_arrary[i][1]
        c = math.sqrt(1 - (b/a)**2)
        zm_a = 1 - c*math.sin(math.radians(center_lat+pixel_size/2))
        zp_a = 1 + c*math.sin(math.radians(center_lat+pixel_size/2))
        area_a = math.pi * b**2 * (math.log(zp_a/zm_a) / (2*c) + math.sin(math.radians(center_lat+pixel_size/2)) / (zp_a*zm_a))
        zm_b = 1 - c*math.sin(math.radians(center_lat-pixel_size/2))
        zp_b = 1 + c*math.sin(math.radians(center_lat-pixel_size/2))
        area_b = math.pi * b**2 * (math.log(zp_b/zm_b) / (2*c) + math.sin(math.radians(center_lat-pixel_size/2)) / (zp_b*zm_b))
        area = (1 / 360 * (area_a - area_b))
        raster_area[i][2] = area
    return raster_area
