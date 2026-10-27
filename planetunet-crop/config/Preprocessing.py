
import os


# Configuration of the parameters for the 1-Preprocessing.ipynb notebook
class Configuration:
    '''
    Configuration for the first notebook.
    Copy the configTemplate folder and define the paths to input and output data. Variables such as raw_ndvi_image_prefix may also need to be corrected if you are use a different source.
    '''
    def __init__(self):
        # For reading the training areas and polygons
        self.training_base_dir = '/mnt/super/fallow'
        self.training_area_fn = 'training_areas_v1.shp'
        self.training_polygon_fn = 'training_polys_v1.shp'
        # For reading multichannel images
        self.raw_image_base_dir = '/mnt/warehouse/sahel/planet_medres_normalized_analytic_2019-06_2019-11_mosaic'
        self.input_image_pref = 'L15'
        self.raw_image_file_type = '.tif'
        self.prediction_pre = 'det'
        # Channel names in order
        self.raw_channel_prefixs = ['blue', 'green', 'red', 'infrared','ndvi']
        # All channel in one single raster file
        self.single_raster = True
        self.bands = list(range(len(self.raw_channel_prefixs)))

        # For writing the extracted images and their corresponding annotations and boundary file
        self.path_to_write = '/mnt/super/fallow/output_crop'
        self.show_boundaries_during_processing = False #False
        self.extracted_file_type = '.png'
        self.extracted_filenames = ['blue', 'green', 'red', 'infrared', 'ndvi']
        self.extracted_annotation_filename = 'annotation'
        self.extracted_boundary_filename = 'boundary'
        

        # Path to write should be a valid directory
        # assert os.path.exists(self.path_to_write)
        if not os.path.exists(self.path_to_write):
            os.makedirs(self.path_to_write)

        if not len(os.listdir(self.path_to_write)) == 0:
            print('Warning: path_to_write is not empty! The old files in the directory may not be overwritten!!')
