import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.models import load_model

# load the word encoder
dataset, info = tfds.load('imdb_reviews/subwords8k', with_info=True, as_supervised=True)
encoder= info.features['text'].encoder

# load the model
model = load_model("./model2")

# apply padding to sentence
def pad_to_size(vec, size):
    zeros = [0]*(size-len(vec))
    vec.extend(zeros)
    return vec

# predict the sentiment of a sentence
def sample_predict(sentence, pad):
    encoded_sample_pred_text = encoder.encode(sentence)
    if pad:
        encoded_sample_pred_text = pad_to_size(encoded_sample_pred_text, 64)
    encoded_sample_pred_text = tf.cast(encoded_sample_pred_text, tf.float32)
    predictions = model.predict(tf.expand_dims(encoded_sample_pred_text, 0))
    return predictions