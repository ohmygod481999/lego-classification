import tensorflow as tf
import os

def getClassNames():
    dataset_path = 'croped_lego'
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(os.path.join(dataset_path), seed=123, batch_size=32,
    validation_split=0.2, subset="training")
    class_names = train_ds.class_names
    return class_names
