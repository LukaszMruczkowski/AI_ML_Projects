# Traffic

An AI that uses Tensorflow to train a convolutional neural network to identify which traffic sign appears in a photograph

## Background

As research continues in the development of self-driving cars, one of the key challenges is computer vision, allowing these cars to develop an understanding of their environment from digital images. In particular, this involves the ability to recognize and distinguish road signs – stop signs, speed limit signs, yield signs, and more

The dataset that will be used is the [German Traffic Sign Recognition Benchmark (GTSRB)](https://benchmark.ini.rub.de/?section=gtsrb&subsection=news) dataset, which contains thousands of images of 43 different kinds of road signs

## Files

The dataset is too large, therefore the `data` directory only contains the links to download them. After downloading, the `data` directory should be replaced by the downloaded folder, namely "gtsrb". The `traffic.py` file contains the main functions including loading data, getting the model, training the model, and evaluating the model

## How to Use

Make sure `Tensorflow`, `opencv-python` and `scikit-learn` are installed. If not, run the following command

`pip install tensorflow opencv-python scikit-learn`

In the `traffic` directory, run the command

`python traffic.py data model_filename`

Where `data` should be either gtsrb or gtsrb-small which are downloaded through the links in the `data` directory. `Model_filename` is an optional argument that will store the trained model in the specifiled path

## Example Output

```shell
$ python traffic.py gtsrb
Epoch 1/10
500/500 [==============================] - 5s 9ms/step - loss: 3.7139 - accuracy: 0.1545
Epoch 2/10
500/500 [==============================] - 6s 11ms/step - loss: 2.0086 - accuracy: 0.4082
Epoch 3/10
500/500 [==============================] - 6s 12ms/step - loss: 1.3055 - accuracy: 0.5917
Epoch 4/10
500/500 [==============================] - 5s 11ms/step - loss: 0.9181 - accuracy: 0.7171
Epoch 5/10
500/500 [==============================] - 7s 13ms/step - loss: 0.6560 - accuracy: 0.7974
Epoch 6/10
500/500 [==============================] - 9s 18ms/step - loss: 0.5078 - accuracy: 0.8470
Epoch 7/10
500/500 [==============================] - 9s 18ms/step - loss: 0.4216 - accuracy: 0.8754
Epoch 8/10
500/500 [==============================] - 10s 20ms/step - loss: 0.3526 - accuracy: 0.8946
Epoch 9/10
500/500 [==============================] - 10s 21ms/step - loss: 0.3016 - accuracy: 0.9086
Epoch 10/10
500/500 [==============================] - 10s 20ms/step - loss: 0.2497 - accuracy: 0.9256
333/333 - 5s - loss: 0.1616 - accuracy: 0.9535
```
