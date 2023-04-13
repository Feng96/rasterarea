import folium


class Map(folium.Map):
    """_summary_

    Args:
        folium (_type_): _description_
    """
    def __init__(self, location=None, width="100%", height="100%", left="0%", top="0%", position="relative", tiles="OpenStreetMap", attr=None, min_zoom=0, max_zoom=18, zoom_start=10, min_lat=-90, max_lat=90, min_lon=-180, max_lon=180, max_bounds=False, crs="EPSG3857", control_scale=False, prefer_canvas=False, no_touch=False, disable_3d=False, png_enabled=False, zoom_control=True, **kwargs):
        super().__init__(location, width, height, left, top, position, tiles, attr, min_zoom, max_zoom, zoom_start, min_lat, max_lat, min_lon, max_lon, max_bounds, crs, control_scale, prefer_canvas, no_touch, disable_3d, png_enabled, zoom_control, **kwargs)
        
        