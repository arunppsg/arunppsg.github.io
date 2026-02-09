+++
title = "Time series anomaly detection using Generative Adversarial Nets"
date = "2021-04-21"
[taxonomies]
tag = ["ml"]
+++

This post describes the use of Generative Adversarial Networks for detecting anomalies in time series data and it is based on the <a href="https://arxiv.org/pdf/2009.07769.pdf">paper</a> with the same title as this blog.</p>
Table of Contents
 - Anomalies in time series data
 - Data Preprocessing
 - Model Architecture
 - Training procedures - loss function, optimizer, gradient penalty loss
 - Anomaly Detection
 - References

### Anomalies in Time Series Data
Many real world data have a time component with them, like the data from stock exhange, network events etc. Anomaly detection or the detection of interesting events can offer information related to critical events like breach of security. Anomalies can be broadly classified into two types: Point anomalies where the anomaly is a single point and Collective Anomaly where the anomaly is a sequence of points. There are other types like the Contextual Anomaly where a data point is supposes to be normal but unusual due to the time when the signal is observed.

There are various ways to detect anomalies in time series data like proximity based methods (data points which are over a distant from the other non-anamlous data points), prediction based methods (predicts the expected value of a point and the point is labelled as anomalous if there is high deviation from the actual value ex: ARIMA), reconstruction-based methods (maps the data point to a latent space, reconstructs it and detect anomalies by finding reconstruction error). In this paper, the problem of anomaly detection is framed as an unsupervised learning problem and a Generative Adversarial Networks(GAN) framework is proposed to detect anomalies from the time series data.

### Data Preprocessing

Steps in preprocessing:
- Produce equally spaced time series sequence.
- Impute the missing values.
- Min-max scale the signals between -1 and +1.
- Roll the signal into windows of size 100. Hence, the dimension of input domain will be 100 X 1.

### Model Architecture

There are four key components in the architecture of the model. They are an encoder, decoder, critic X, critic Z.

- Encoder: The role of the encoder &#8496 is to learn a mapping between the input domain and the latent domain. The rolled signals acts as input to the model and they are mapped into a latent space of dimension 20. The encoder learns the mapping between input space to latent space. The encoder is a 1-layer bi-directional LSTM with 100 hidden units.
- Decoder: The decoder learns the mapping between the latent space to the input domain. It learns how to reconstruct a signal given the signal in lower dimension. The decoder or the generator (it generates the signal from the random noise) is a 2-layer bidirectional LSTM with 64 hidden units.
- Critic X (Discriminator X): Critic X is trained to distinguish between the real signal and fake signal. It uses Wasserstein loss function for learning to distinguish between real and fake signals. Fake signals are signals which are samples from noise.
- Critic Z (Discriminator Z) - Critic Z is trained to distinguish between the random noise from the latent domain and encoded samples. Critic Z also uses wasserstein loss function during training. Both the critics are 1-D convolutional layers.

### Training Procedure

#### Loss functions

GANs are zero-sum games. The direction of gradient update of the generator is opposite to the direction of gradient update of the discriminator. Generator here refers to the encoder-decoder architecture and discriminator refers to critic X and critic Z. The loss function for the generator is the sum of reconstruction error loss and the wasserstein loss. The wasserstein loss aims to maximize the distance between the real samples distributions and fake sample distribution. Let's consider the encoder. The encoder encodes the real samples from the time series. It also encodes random noise samples from the space of input domain. The role of critic X is to distinguish between the encoded real samples and noise samples. Hence, the desired learning for critic X is to produce a high score for real samples and a low score for fake samples. Critic X has to maximize the wasserstein distance between the real samples and fake samples. Hence, the critic X updates its gradient in the direction which maximizes the wasserstein distance. The role of encoder is to make a good mapping between input space and latent space i.e to reduce wasserstein loss.Hence it updates the gradients in the the direction opposite to the wasserstein distance. The decoder follows the similar procedure except it uses wasserstein loss from Critic Z. The reconstruction error for the time series data is found using the method of dynamic time warping.


The model is trained on one specific dataset for 2000 epochs with a batch size of 64. In an epoch, the encoder-decoder are iterated through the dataset once and the critic x and critic z are iterated through the dataset n<sub>critic</sub> where n<sub>critic</sub> is chosen as 5. The training process juggles between the training of discrinimator and the generator. The discriminator tries to figure out how to distinguish real data from fake and it has to learn to recognize generator's flaws. The learning of discriminator is more important because if the discriminator can't tell the difference between real and fake samples, the traning of generator fails. Hence, the discriminator is iterated 5 time through the dataset for every 1 iteration of the dataset through the generator in an epoch. In the training process, gradient penalty loss is also used. In gradient penalty, we penalize the norm of the gradient of the critic with respect to the input which adds more stability to the training.

#### Anomaly Detection

The encoder and decoder maps the signal from input space to latent space and reconstructs the signal from latent space to input space respectively. This mapping helps in anomaly detection. For an anomalous point, thepoint is first encoded into latent space and the encoded anomalous point will deviate from the distribution of encoding of non-anomalous points. Encoding of the anomalous point maps it to the noise distribution and hence when we decode the encoded anomalous point, a high reconstruction error will be observed which can be used to detect anomalies.The critic X helps in distinguishing between the real samples and fake samples. It produces a high score for real samples and low score for fake and anomalous samples. Anomalies are detected using the reconstruction error and critic score. An anomalous point will have high reconstruction error and low critic score. We consider the anomaly score to be the product of reconstruction error and inverse of critic score. Anomalous points are points which will be having high anomaly scores. These points can be detected by considering a moving window and points exceeding 3 standard deviation from the mean and standard deviation of that window.

## References

- [TadGAN](https://arxiv.org/pdf/2009.07769.pdf)
- [Wasserstein GAN](https://arxiv.org/pdf/1701.07875.pdf)
- [Improved training of WGAN with Gradient Penalty Loss](https://arxiv.org/pdf/1704.00028.pdf)
- [Dynamic Time Warping](https://en.wikipedia.org/wiki/Dynamic_time_warping)
