from keras.layers import BatchNormalization
from keras.layers import Layer
import keras.backend as K
from keras import initializers
from keras_contrib.layers import InstanceNormalization, GroupNormalization, Swish


# from transformer
class LayerNormalization(Layer):
    def __init__(self, eps=1e-6, **kwargs):
        self.eps = eps
        super(LayerNormalization, self).__init__(**kwargs)

    def build(self, input_shape):
        self.gamma = self.add_weight(name='gamma', shape=input_shape[-1:], initializer=initializers.Ones(), trainable=True)
        self.beta = self.add_weight(name='beta', shape=input_shape[-1:], initializer=initializers.Zeros(), trainable=True)
        super(LayerNormalization, self).build(input_shape)

    def call(self, inputs, **kwargs):
        mean = K.mean(inputs, axis=-1, keepdims=True)
        std = K.std(inputs, axis=-1, keepdims=True)
        return self.gamma * (inputs - mean) / (std + self.eps) + self.beta

    def compute_output_shape(self, input_shape):
        return input_shape


BN = BatchNormalization
LN = LayerNormalization
IN = InstanceNormalization
GN = GroupNormalization
Swish = Swish
