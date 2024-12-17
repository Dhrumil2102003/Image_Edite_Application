
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, MaxPool2D, Conv2DTranspose, Concatenate, Input
from tensorflow.keras.layers import AveragePooling2D, GlobalAveragePooling2D, UpSampling2D, Reshape, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.applications import ResNet50
import tensorflow as tf

def SqueezeAndExcite(inputs, ratio=8): # Squeeze and Excite
    init = inputs # initial input
    filters = init.shape[-1] # filters
    se_shape = (1, 1, filters) # shape of se
    
    se = GlobalAveragePooling2D()(init)  # Global Average Pooling
    se = Reshape(se_shape)(se) # Reshape
    se = Dense(filters // ratio, activation='relu', kernel_initializer='he_normal', use_bias=False)(se) # Dense
    se = Dense(filters, activation='sigmoid', kernel_initializer='he_normal', use_bias=False)(se) # Dense
    x = init * se # Multiply
    
    return x 

def ASPP(inputs): # Atrous Spatial Pyramid Pooling
    """ Image Pooling """
    shape = inputs.shape # shape of input
    y1 = AveragePooling2D(pool_size=(shape[1], shape[2]))(inputs) # 1x1 conv
    y1 = Conv2D(256, 1, padding="same", use_bias=False)(y1) # 1x1 conv
    y1 = BatchNormalization()(y1) # Batch Normalization
    y1 = Activation("relu")(y1) # ReLU
    y1 = UpSampling2D((shape[1], shape[2]), interpolation="bilinear")(y1) # Upsampling

    
    """ 1x1 conv """
    y2 = Conv2D(256, 1, padding="same", use_bias=False)(inputs) # 1x1 conv
    y2 = BatchNormalization()(y2) # Batch Normalization
    y2 = Activation("relu")(y2) # ReLU  
    
    """ 3x3 conv rate=6 """ # 3x3 conv rate=6
    y3 = Conv2D(256, 3, padding="same", use_bias=False, dilation_rate=6)(inputs) # 3x3 conv
    y3 = BatchNormalization()(y3) # Batch Normalization
    y3 = Activation("relu")(y3) # ReLU
    
    """ 3x3 conv rate=12 """ # 3x3 conv rate=12
    y4 = Conv2D(256, 3, padding="same", use_bias=False, dilation_rate=12)(inputs) # 3x3 conv
    y4 = BatchNormalization()(y4) # Batch Normalization
    y4 = Activation("relu")(y4) # ReLU
    
    """ 3x3 conv rate=18 """ # 3x3 conv rate=18
    y5 = Conv2D(256, 3, padding="same", use_bias=False, dilation_rate=18)(inputs) # 3x3 conv
    y5 = BatchNormalization()(y5) # Batch Normalization
    y5 = Activation("relu")(y5) # ReLU
    
    y = Concatenate()([y1, y2, y3, y4, y5]) # Concatenate
    y = Conv2D(256, 1, padding="same", use_bias=False)(y) # 1x1 conv
    y = BatchNormalization()(y) # Batch Normalization
    y = Activation("relu")(y) # ReLU
    
    return y # return output
def deeplabv3_plus(shape):
    """ Input """
    inputs = Input(shape)

    """ Encoder """
    encoder = ResNet50(weights="imagenet", include_top=False, input_tensor=inputs) # ResNet50
    image_features = encoder.get_layer("conv4_block6_out").output # get layer
    x_a = ASPP(image_features)
    x_a = UpSampling2D((4, 4), interpolation="bilinear")(x_a) # Upsampling

    x_b = encoder.get_layer("conv2_block2_out").output # get layer
    x_b = Conv2D(filters=48, kernel_size=1, padding='same', use_bias=False)(x_b) # 1x1 conv
    x_b = BatchNormalization()(x_b) # Batch Normalization
    
    
    x = Concatenate()([x_a, x_b]) # Concatenate
    x = SqueezeAndExcite(x) # Squeeze and Excite    
    
    x = Conv2D(filters=256, kernel_size=3, padding='same', use_bias=False)(x) # 3x3 conv
    x = BatchNormalization()(x) # Batch Normalization
    x = Activation('relu')(x) # ReLU
    
    x = Conv2D(filters=256, kernel_size=3, padding='same', use_bias=False)(x) # 3x3 conv
    x = BatchNormalization()(x) # Batch Normalization    
    x = Activation('relu')(x) # ReLU

    x = SqueezeAndExcite(x) # Squeeze and Excite
    
    x = UpSampling2D((4, 4), interpolation="bilinear")(x) # Upsampling
    x = Conv2D(1, 1)(x) # 1x1 conv
    x = Activation("sigmoid")(x) # Sigmoid
    model = Model(inputs, x) # Model
    
    return model # return model


if __name__ == "__main__":
    model = deeplabv3_plus((512, 512, 3))
    model.summary()