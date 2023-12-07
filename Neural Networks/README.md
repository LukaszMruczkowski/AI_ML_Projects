# Neural Networks

One area in modern machine learning is neural networks (NN). NN is inspired by how human brains function, neurons in human brains communicate information with each other and learn about the world, machine learning imitates that and uses artificial neurons to process and learn from data

## Structure and Algorithms

In the previous lecture, the AI takes input and multiplies the input by some weights to produce an output. For example, when the input is x1 and x2, AI learns from data what the weights for each of the inputs should be, multiplies inputs by their weights, and uses the output function to either perform classification tasks or regression tasks. NN shares the same idea, graphically

<img src="https://user-images.githubusercontent.com/99038613/177021892-e4d378fe-870a-4377-8e1a-c93fd4eb127d.jpg" width=60% height=60%>

### [Gradient Descent](https://en.wikipedia.org/wiki/Gradient_descent)

Gradient Descent is an algorithm for minimizing loss when training neural networks. In calculus, there is a term called "gradient", or slope of a function at any given input. The Gradient Descent algorithm utilizes this mathematical principle to minimize the loss function by looking at all the data points and calculating the gradient that will lead to decreasing loss. By repeating this process, the weights should converge and the loss will be minimized

However, there is a limitation to this algorithm. When there is a lot of data, which is most likely the case in real-world problems, the step of looking at all the data points becomes computationally costly and time-inefficient

- **Stochastic Gradient Descent (SGD)**: The traditional gradient descent algorithm takes too much computational effort to calculate gradients based on all data points. Therefore, SGD is introduced to minimize this cost. SGD proposes only looking at one random data point at each iteration. Though the gradient will not be as accurate, this algorithm takes much less time to compute
- **Mini-Batch Gradient Descent**: While the traditional gradient descent takes too much time and the SGD is not as accurate, the Mini-Batch Gradient Descent algorithm is introduced to find a balance point. This approach uses neither all the data points nor one random one but randomly selects a batch of data points (batch size customizable) and calculates the gradient based on them

### Multilayer Neural Network

Simple NN connects input neurons directly to output neurons, which can only provide a linear relationship between input and output; however, real-world problems can rarely be solved by linear relationships. Therefore, the Multilayer Neural Network (MNN) is introduced to form more complex relationships between input and output neurons

<img src="https://user-images.githubusercontent.com/99038613/177021897-6d1b29d1-48b4-4a5b-bc92-b638442cea2c.jpg" width=60% height=60%>

The middle layers of neural networks are called the hidden layers. Mathematically, they serve the purpose of creating complex functions relating to input and output. In a real-world sense, they can be interpreted as individual neural networks that learn different features from the input and combine them to form a more accurate output

### Backpropagation

The gradient descent algorithm is used for simple NN since we know what the actual values of the input and output should be so we can calculate the loss and gradient. But in MNN, we have no idea what the actual value of the hidden layers should be, that's where the Backpropagation algorithm comes in. Since we only know the loss of the output given the input, we will start with the output neurons and backtrack each hidden layer to the input. The key here is that we have information about the weights of each neuron in the hidden layers, so we can estimate what proportion of loss is due to which neuron

### Overfitting

Sometimes the number of hidden layers and neurons is too many for a certain problem, which leads to overfitting since the AI is learning too closely to the given data so it fails to generalize. One way to combat overfitting is by dropping out. In this technique, during each learning epoch/iteration, the NN randomly "hides" some neurons (as they do not exist) to prevent relying too heavily on certain neurons

![3](https://user-images.githubusercontent.com/99038613/177021902-2f5c2a5c-5255-4dc6-a458-58bc43e8a36f.jpg)

## Computer Vision

Computer vision encompasses the different computational methods for analyzing and understanding digital images, and it is often achieved using NN. For instance, in Apple's Photo app, the AI can recognize which photos have a certain person's face

A way the AI can achieve this is by inputting every pixels colour information as input neurons and through MNN to recognize features in images; however, this method is too computationally expensive since the input size is enormous as there are millions of pixels in modern devices

### Image Convolution

A way to simplify the input neurons is by convolution. Image convolution is applying a filter that adds each pixel value of an image to its neighbors, weighted according to a kernel matrix. Doing so alters the image and can help the neural network process it. For instance, in the figure below, by multiplying and adding in all possible 3x3 matrices by the kernel matrix, the resultant is a 2x2 matrix which shrinks the size of the input

<img src="https://user-images.githubusercontent.com/99038613/177021906-20c04bea-ebd9-4602-8bd6-73d3c8eea9df.jpg" width=60% height=60%>

Furthermore, image convolution can do more than shrink the input size, by applying a certain kernel matrix, we can get certain features on the image. For instance, by applying the famous matrix in the figure below

![5](https://user-images.githubusercontent.com/99038613/177021910-a65a8268-72d0-4068-b2e0-edf60c770ff0.jpg)

we are able to get a convoluted image that only has the boundaries of objects in the image like the below figure

![6](https://user-images.githubusercontent.com/99038613/177021911-64560667-076f-458e-a44f-1d0b4d63ee8b.jpg)

### Pooling

Another way to simplify the image is by the method of pooling. In this method, the input size is shrunk even more by sampling from regions of the image. A typical pooling method is Max-Pooling, where we take the maximum value in a region to be the representative and put it in a new matrix. See the below figure, for every 2x2 matrix in the 4x4 matrix, extracting the maximum value in it and forming a new 2x2 matrix

<img src="https://user-images.githubusercontent.com/99038613/177021913-e6733878-9cef-4d01-9cbc-091ce357391c.jpg" width=60% height=60%>

### Convolutional Neural Network

A convolutional neural network is a neural network that uses convolution, usually for analyzing images. It starts by applying image convolution and pooling to simplify the image and then inputs the information about each pixel to the input neurons. See the figure below

<img src="https://user-images.githubusercontent.com/99038613/177021914-61081035-0e63-46f7-bbb2-1223ab6f4311.jpg" width=60% height=60%>

## [Recurrent Neural Networks](https://en.wikipedia.org/wiki/Recurrent_neural_network)

Feed-forward neural Networks are the type of neural networks discussed so far, where input data is provided to the network, which eventually produces some output. Whereas in recurrent neural networks, input and output are not one, depending on the structure and design of the network, the output of the network is fed into the input again to process continuous input such as videos or voices

<img src="https://user-images.githubusercontent.com/99038613/177021919-0c884ca8-07b4-4e12-b8b6-190660250a49.jpg" width=60% height=60%>
