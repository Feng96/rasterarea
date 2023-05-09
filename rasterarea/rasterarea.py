"""Main module."""
# require GDAL 
# import localtileserver
import math
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import TwoSlopeNorm
import ipywidgets as widgets
from ipyfilechooser import FileChooser
import netCDF4 as nc
import os
from ipywidgets import TwoByTwoLayout
from ipyleaflet import WidgetControl
import traitlets
from IPython.display import display
from tkinter import Tk, filedialog
# from cartopy import config
# import cartopy.crs as ccrs
import geemap
import rasterio
from ipyleaflet import Marker
from datetime import datetime, timedelta

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


class SelectFilesButton(widgets.Button):
    """A file widget that leverages tkinter.filedialog."""

    def __init__(self):
        super(SelectFilesButton, self).__init__()
        # Add the selected_files trait
        self.add_traits(files=traitlets.traitlets.List())
        # Create the button.
        self.description = "Select Files"
        self.icon = "square-o"
        # Set on click behavior.
        self.on_click(self.select_files)

    @staticmethod
    def select_files(b):
        """Generate instance of tkinter.filedialog.

        Parameters
        ----------
        b : obj:
            An instance of ipywidgets.widgets.Button 
        """
        # Create Tk root
        root = Tk()
        # Hide the main window
        root.withdraw()
        # Raise the root to the top of all windows.
        root.call('wm', 'attributes', '.', '-topmost', True)
        # List of selected fileswill be set to b.value
        b.files = filedialog.askopenfilename(multiple=True)

        b.description = "Files Selected"
        b.icon = "check-square-o"
        b.style.button_color = "lightgreen"


class Toolbar(widgets.VBox):
    def __init__(self,parent,**kwargs):
        super().__init__()
        self.create_widgets()
        self.output = widgets.Output()
        self.setup_interactive_plot()   
        self.parent = parent

        # Observe the changes in the fileuploader.files and call open_file
        self.fileuploader.observe(self.open_file, names='files')
        self.layerselector.observe(self.plot, 'value')  
    
    padding = "0px 0px 0px 5px"
    ## create buttons
    def create_widgets(self):
        self.fileuploader = SelectFilesButton()
        self.add_button = widgets.Button(description="Add")
        self.add_button.on_click(self.add)
        self.layerselector = widgets.Dropdown(
            options=["No file uploaded"],
            value=None,
            description="Layer:"
        )
        self.pick_button = widgets.Button(description="Pick", layout=widgets.Layout(padding="0px 0px 0px 5px"))  # Create a pick_button
        self.pick_button.on_click(self.pick_location)  # Add an event listener for the pick_button
        self.plot_button = widgets.Button(description="Plot", layout=widgets.Layout(padding="0px 0px 0px 5px"))  # Create a plot_button
        self.plot_button.on_click(self.plot_time_series)  # Add an event listener for the plot_button
        self.marker = None
        self.start_date_picker = widgets.DatePicker(description='Start Date', value=datetime(2018, 1, 1))
        self.end_date_picker = widgets.DatePicker(description='End Date', value=datetime(2018, 12, 31))
        self.time_resolution_dropdown = widgets.Dropdown(options=['Daily', 'Monthly', 'Yearly'], description='Resolution')
        self.save_button = widgets.Button(description="Save", layout=widgets.Layout(padding="0px 0px 0px 5px"))  # Create a save_button
        self.save_button.on_click(self.save_plot)  
        self.children = [self.fileuploader,
                        self.pick_button,
                        self.plot_button,
                        self.start_date_picker,
                        self.end_date_picker,
                        self.time_resolution_dropdown,
                        self.save_button]  # Add the plot_button to the children list
        self.fig = None 

    ## define toolbar layout
    def setup_interactive_plot(self):
        left_box = widgets.VBox([
            self.fileuploader,
            self.layerselector,
            self.add_button,
            self.pick_button,
            self.start_date_picker,
            self.end_date_picker,
            self.time_resolution_dropdown,
            self.plot_button,
            self.save_button
        ])

        toolbar = widgets.HBox([left_box, self.output])
        display(toolbar)
    ## define open file event
    def open_file(self, change):
        self.ds_list = self.fileuploader.files
        self.update_dropdown()

    def update_dropdown(self):
        if len(self.ds_list) > 0:
            file_names = [os.path.basename(file_path) for file_path in self.ds_list]
            self.layerselector.options = file_names
            self.layerselector.value = file_names[0]
        else:
            self.layerselector.options = ["No file uploaded"]
            self.layerselector.value = None

    def read_and_plot_file(self, file_path):
        with self.output:
            self.output.clear_output()
            if file_path.endswith(".tif"):
                self.parent.add_raster(source=file_path, bands=1, layer_name='GRACE', palette='Accent', vmin=None, vmax=None, nodata=-99999, attribute=None)
                with rasterio.open(file_path) as ds:
                    data = ds.read(1)
            else:
                print("File type not supported")
                return
        
            nodata = -99999
            data[data == nodata] = np.nan # Set nodata values to NaN

        # Setting up the color scale
            cmap = plt.cm.RdBu
            cmap.set_bad(color='white')
            norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)

            plt.imshow(data, cmap=cmap, norm=norm) # Plot the image with the new color scale
            plt.colorbar()
            plt.show()
            print(self.output.outputs)
    
    def plot(self, change):
        if change['name'] == 'value':
            selected_file_name = self.layerselector.value
            selected_file_index = self.layerselector.options.index(selected_file_name)
            selected_file_path = self.fileuploader.files[selected_file_index]
            self.read_and_plot_file(selected_file_path)

    def add(self, event=None):
        self.read_and_plot_file(file_path = self.fileuploader.files[0])

    def pick_location(self, button):
        if not self.parent.on_interaction(self.handle_click):  # Add a click event handler to the parent (Map)
            self.parent.on_interaction(self.handle_click)

    def handle_click(self, **kwargs):
        if kwargs.get('type') == 'click':  # Check if the event is a click event
            lat_lng = kwargs.get('coordinates')
            if lat_lng:
                if self.marker:  # If a marker already exists, remove it before adding a new one
                    self.parent.remove_layer(self.marker)

                self.marker = Marker(location=lat_lng, draggable=False)  # Create a marker at the clicked location
                self.parent.add_layer(self.marker)  # Add the marker to the map
                print(f'Clicked coordinates: {lat_lng}')  # Print the real-world coordinates

    @staticmethod
    def date_from_filename(filename):
        parts = filename.split('_')
        for part in parts:
            if part.isdigit():
                start_day_of_year = int(part[:7])
                end_day_of_year = int(part[7:])
                break
        else:
            raise ValueError("Date not found in file name")

        year = int(start_day_of_year / 1000)
        start_day_of_year %= 1000
        end_date = datetime(year, 1, 1) + timedelta(days=end_day_of_year - 1)
        return end_date

    def get_tiff_dates(self, file_list):
        dates = []
        for file_path in file_list:
            file_name = os.path.basename(file_path)
            date_obj = self.date_from_filename(file_name)
            dates.append(date_obj)
        return dates

    def get_pixel_values(self, file_list, lat_lng):
        lat, lng = lat_lng
        values = []
        for file_path in file_list:
            with rasterio.open(file_path) as src:
                row, col = src.index(lng, lat)
                value = src.read(1)[row, col]
                values.append(value)
        return values
    
    def check_number_of_files(self, start_date, end_date, time_resolution):
        if time_resolution == 'Daily':
            expected_files = (end_date - start_date).days + 1
        elif time_resolution == 'Monthly':
            expected_files = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1
        elif time_resolution == 'Yearly':
            expected_files = end_date.year - start_date.year + 1
        
        if len(self.fileuploader.files) != expected_files:
            return f"Error: {expected_files} files expected for the selected date range and time resolution, but {len(self.fileuploader.files)} files were uploaded."
        return ""

    def plot_time_series(self, button):
        if not hasattr(self, 'marker') or self.marker is None:
            return

        lat_lng = self.marker.location
        values = self.get_pixel_values(self.fileuploader.files, lat_lng)

        start_date = self.start_date_picker.value
        end_date = self.end_date_picker.value
        time_resolution = self.time_resolution_dropdown.value

        error_message = self.check_number_of_files(start_date, end_date, time_resolution)
        if error_message:
            print(error_message)
            return

        if time_resolution == 'Daily':
            date_range = pd.date_range(start_date, end_date, freq='D')
            x_axis_format = mdates.DayLocator()
            x_axis_date_format = mdates.DateFormatter('%Y-%m-%d')
        elif time_resolution == 'Monthly':
            date_range = pd.date_range(start_date, end_date, freq='M')
            x_axis_format = mdates.MonthLocator()
            x_axis_date_format = mdates.DateFormatter('%Y-%m')
        elif time_resolution == 'Yearly':
            date_range = pd.date_range(start_date, end_date, freq='Y')
            x_axis_format = mdates.YearLocator()
            x_axis_date_format = mdates.DateFormatter('%Y')

                # Resample the values to match the length of the date_range
        values = np.interp(
            np.linspace(0, len(values) - 1, len(date_range)),
            np.arange(len(values)),
            values
        )
        with self.output:
            self.output.clear_output() 
            self.fig, ax = plt.subplots()
            ax.plot(date_range, values)
            ax.xaxis.set_major_locator(x_axis_format)
            ax.xaxis.set_major_formatter(x_axis_date_format)
            plt.xticks(rotation=45)
            plt.show()
            
    def save_plot(self, button):
        with self.output:
            if self.fig:  # Check if there is a figure to save
                self.fig.savefig('plot.png')  # Save the figure to a file named 'plot.png'
                print('Plot saved as plot.png')  # Print a message to indicate the plot has been saved
            else:
                print('No plot to save')  # Print a message if there is no plot to save

class Map(geemap.Map):
    
    def __init__(self, center=[20, 0], zoom=2, **kwargs) -> None:

        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        super().__init__(center=center, zoom=zoom, **kwargs)
        self.toolbar = Toolbar(parent=self)

    
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

    def add_raster(
        self,
        source,
        bands=1,
        layer_name=None,
        palette=None,
        vmin=None,
        vmax=None,
        nodata=None,
        attribute=None
    ):
        """Add a local raster dataset to the map.

            If you are using this function in JupyterHub on a remote server and the raster does not render properly, try
            running the following two lines before calling this function:

            import os
            os.environ['LOCALTILESERVER_CLIENT_PREFIX'] = 'proxy/{port}'

        Args:
            source (str): The path to the GeoTIFF file or the URL of the Cloud Optimized GeoTIFF.
            band (int, optional): The band to use. Band indexing starts at 1. Defaults to None.
            palette (str, optional): The name of the color palette from `palettable` to use when plotting a single band. See https://jiffyclub.github.io/palettable. Default is greyscale
            vmin (float, optional): The minimum value to use when colormapping the palette when plotting a single band. Defaults to None.
            vmax (float, optional): The maximum value to use when colormapping the palette when plotting a single band. Defaults to None.
            nodata (float, optional): The value from the band to use to interpret as not valid data. Defaults to None.
            attribution (str, optional): Attribution for the source raster. This defaults to a message about it being a local file.. Defaults to None.
            layer_name (str, optional): The layer name to use. Defaults to None.
        """
        super().add_raster(source=source, bands=bands, layer_name=layer_name, palette=palette, vmin=vmin, vmax=vmax, nodata=nodata, attribute=attribute)

 
    def add_toolbar(self, position='topright', **kwargs):
        """Adds a toolbar to the map.

        Args:
            toolbar (str, optional): The toolbar to add. Defaults to 'draw'.
            position (str, optional): The position of the toolbar. Defaults to 'topright'.
        """
        widget_width = "250px"
        padding = "0px 0px 0px 5px"  # upper, right, bottom, left

        toolbar_button = widgets.ToggleButton(
            value=False,
            tooltip="Toolbar",
            icon="wrench",
            layout=widgets.Layout(width="28px", height="28px", padding=padding),
        )

        close_button = widgets.ToggleButton(
            value=False,
            tooltip="Close the tool",
            icon="times",
            button_style="primary",
            layout=widgets.Layout(height="28px", width="28px", padding=padding),
        )
        toolbar = widgets.HBox([toolbar_button])

        def toolbar_click(change):
            if change["new"]:
                toolbar.children = [toolbar_button, close_button]
            else:
                toolbar.children = [toolbar_button]
        
        toolbar_button.observe(toolbar_click, "value")

        def close_click(change):
            if change["new"]:
                toolbar_button.close()
                close_button.close()
                toolbar.close()
        
        close_button.observe(close_click, "value")
        rows = 2
        cols = 2
        grid = widgets.GridspecLayout(rows, cols, grid_gap="0px", layout=widgets.Layout(width="65px"))
        icons = ["folder-open", "map", "info", "question"]

        for i in range(rows):
            for j in range(cols):
                grid[i, j] = widgets.Button(description="", button_style="primary", icon=icons[i*rows+j], 
                                            layout=widgets.Layout(width="28px", padding="0px"))
        toolbar = widgets.VBox([toolbar_button])
        def toolbar_click(change):
            if change["new"]:
                toolbar.children = [widgets.HBox([close_button, toolbar_button]), grid]
            else:
                toolbar.children = [toolbar_button]
        
        toolbar_button.observe(toolbar_click, "value")

        toolbar_ctrl = WidgetControl(widget=toolbar, position=position)

        output = widgets.Output()
        output_ctrl = WidgetControl(widget=output, position="bottomright")
        def tool_click(b):    
            with output:
                output.clear_output()
                print(f"You clicked the {b.icon} button")

        for i in range(rows):
            for j in range(cols):
                tool = grid[i, j]
                tool.on_click(tool_click)

        with output:
            output.clear_output()
            print("Click on a button to see the output")

        basemap = widgets.Dropdown(
            options=["roadmap", "satellite"],
            value=None,
            description="Basemap:",
            style={"description_width": "initial"},
            layout=widgets.Layout(width="200px"),
        )
        basemap_ctrl = WidgetControl(widget=basemap, position="topright")

        def tool_click(b):    
            with output:
                output.clear_output()
                print(f"You clicked the {b.icon} button")

                if b.icon == "map":
                    self.add_control(basemap_ctrl)
                if b.icon == "folder-open":
                    self.toolbar.setup_interactive_plot()

        for i in range(rows):
            for j in range(cols):
                tool = grid[i, j]
                tool.on_click(tool_click)

        def change_basemap(change):
            if change["new"]:
                self.add_basemap(basemap.value)

        basemap.observe(change_basemap, names='value')
        self.add_control(toolbar_ctrl)