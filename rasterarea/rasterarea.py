"""Main module."""

import math
import pandas as pd

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

def point_cloud_arrary(filepath, no_data=-99999, band=1, **kwargs):
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
    
def pixel_area_array(point_cloud_arrary, pixel_size=1, coordinatesp = 'WGS84', toTable = False, **kwargs):
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
    
    if toTable == True:
        raster_area = pd.DataFrame(raster_area)
        raster_area.rename(columns={0:'center_lon',1:'center_lat',2:'pixel_area'},inplace=True)
    else:
        pass
    
    return raster_area