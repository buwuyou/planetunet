import os

# Configuration of the parameters for the 2-UNetTraining.ipynb notebook
class Configuration:
    def __init__(self):
        # Initialize the data related variables used in the notebook
        # For reading the channels and annotated images generated in the Preprocessing step.
        # In most cases, they will take the same value as in the config/Preprocessing.py
        
        # dir where extrected images are
        self.base_dir = '/mnt/super/fallow/output_fallow'
        self.image_type = '.png'
        self.extracted_filenames = ['blue', 'green', 'red', 'infrared', 'ndvi', 'pred']
        self.annotation_fn = 'annotation'
        self.weight_fn = 'boundary'
        
        # Patch generation; from the training areas (extracted in the last notebook), we generate fixed size patches.
        # random: a random training area is selected and a patch in extracted from a random location inside that training area. Uses a lazy stratergy i.e. batch of patches are extracted on demand.
        # sequential: training areas are selected in the given order and patches extracted from these areas sequential with a given step size. All the possible patches are returned in one call.
        self.patch_generation_stratergy = 'random' # 'random' or 'sequential'
        # (Input + Output) channels
        self.image_channels = len(self.extracted_filenames)
        self.all_channels = self.image_channels + 2
        self.patch_size = (512,512,self.all_channels) # Height * Width * (Input + Output) channels
        # # When stratergy == sequential, then you need the step_size as well
        # step_size = (128,128)
        
        # The training areas are divided into training, validation and testing set. Note that training area can have different sizes, so it doesn't guarantee that the final generated patches (when using sequential stratergy) will be in the same ratio. 
        self.test_ratio = 0.2
        self.val_ratio = 0.2
        
        # Probability with which the generated patches should be normalized 0 -> don't normalize, 1 -> normalize all
        self.normalize = 1

        
        # The split of training areas into training, validation and testing set, is cached in patch_dir.
        self.patch_dir = './patches{}'.format(self.patch_size[0])
        self.frames_json = os.path.join(self.patch_dir,'frames_list.json')


        # Shape of the input data, height*width*channel
        self.input_shape = (512,512,self.image_channels)
        self.input_image_channel = list(range(self.image_channels))
        self.input_label_channel = [self.image_channels]
        self.input_weight_channel = [self.image_channels+1]
        self.label_weight_channel = [self.image_channels, self.image_channels+1]

        # CNN model related variables used in the notebook
        self.BATCH_SIZE = 8
        self.NB_EPOCHS = 100

        # number of validation images to use
        self.VALID_IMG_COUNT = 100 #200
        # maximum number of steps_per_epoch in training
        self.MAX_TRAIN_STEPS = 100 #1000
        self.model_path = './saved_models/UNet/'

