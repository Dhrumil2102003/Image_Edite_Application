import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K


smooth = 1e-15 # Smoothing

def iou(y_true, y_pred): # Intersection over Union
    def f(y_true, y_pred): # Function
        intersection = (y_true * y_pred).sum() # Intersection
        union = y_true.sum() + y_pred.sum() - intersection # Union
        x = (intersection + 1e-15) / (union + 1e-15) # Intersection over Union
        x = x.astype(np.float32) # Convert to float32
        return x 
    return tf.numpy_function(f, [y_true, y_pred], tf.float32) # Return float32


def dice_coef(y_true, y_pred): # Dice Coefficient 
    y_true = tf.keras.layers.Flatten()(y_true)  # Flatten
    y_pred = tf.keras.layers.Flatten()(y_pred)  # Flatten
    intersection = tf.reduce_sum(y_true * y_pred) # Intersection
    return (2. * intersection + smooth) / (tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) + smooth) # Dice Coefficient

def dice_loss(y_true, y_pred): # Dice Loss
    return 1.0 - dice_coef(y_true, y_pred) # Dice Loss

def debug_shapes(y_true, y_pred):
    tf.print("y_true shape:", tf.shape(y_true))
    tf.print("y_pred shape:", tf.shape(y_pred))
    return y_true, y_pred




# import numpy as np
# import tensorflow as tf
# from tensorflow.keras import backend as K

# smooth = 1e-15  # Smoothing

# def iou(y_true, y_pred):
#     """TensorFlow implementation of Intersection over Union."""
#     intersection = tf.reduce_sum(y_true * y_pred)
#     union = tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) - intersection
#     return (intersection + smooth) / (union + smooth)

# def dice_coef(y_true, y_pred):
#     """Dice Coefficient metric."""
#     y_true = tf.keras.layers.Flatten()(y_true)
#     y_pred = tf.keras.layers.Flatten()(y_pred)
#     intersection = tf.reduce_sum(y_true * y_pred)
#     return (2. * intersection + smooth) / (tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) + smooth)

# def dice_loss(y_true, y_pred):
#     """Dice loss function."""
#     return 1.0 - dice_coef(y_true, y_pred)

