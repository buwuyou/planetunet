# Configuration of the parameters for the 3-FinalRasterAnalysis.ipynb notebook
import os
import time
class Configuration:
    '''
    Configuration for the notebook where objects are predicted in the image.
    Copy the configTemplate folder and define the paths to input and output data.
    '''
    def __init__(self):
        
        # Input related variables
        self.input_image_dir = '/mnt/warehouse/sahel/planet_medres_normalized_analytic_2019-06_2019-11_mosaic'
        self.input_image_type = '.jp2'
        self.input_image_pref = 'split'
        self.channel_prefixs = ['blue', 'green', 'red', 'infrared', 'ndvi']
        self.trained_model_path = './saved_models/UNet/crop_20211010-1531_AdaDelta_weightmap_tversky_01234_512.h5'

        # Output related variables
        self.output_dir = self.input_image_dir
        self.output_image_type = '.tif'
        self.output_prefix = 'crop_'
        self.output_shapefile_type = '.shp'
        self.overwrite_analysed_files = False
        self.output_dtype='uint8'

        # Variables related to batches and model
        self.BATCH_SIZE = 200 # Depends upon GPU memory and WIDTH and HEIGHT (Note: Batch_size for prediction can be different then for training.
        self.WIDTH=512 # Should be same as the WIDTH used for training the model
        self.HEIGHT=512 # Should be same as the HEIGHT used for training the model
        self.STRIDE=256 #224 or 196   # STRIDE = WIDTH means no overlap, STRIDE = WIDTH/2 means 50 % overlap in prediction
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.outputTime = f'{self.output_dir}_{self.timestr}'

#         if not os.path.exists(self.outputTime):
#             os.makedirs(self.outputTime)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

