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
        self.input_image_dir = '/mnt/warehouse/sahel/sahel_fallow_pred'
        self.input_image_type = '.tif'
        self.input_image_pref = 'pred_L15'
        self.channel_prefixs = ['blue', 'green', 'red', 'infrared', 'ndvi','pred']
        self.trained_model_path = './saved_models/UNet/fallow_20210419-1602_AdaDelta_weightmap_tversky_012345_512.h5'

        # Output related variables
        self.output_dir = self.input_image_dir
        self.output_image_type = '.tif'
        self.output_prefix = 'fallow_'
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

