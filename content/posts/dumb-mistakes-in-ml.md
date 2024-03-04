+++
title = "Log: My Dumb Mistakes in Machine Learning"
date = 2024-03-04
tags = ["python", "ml"]
+++

A log of my dumb mistakes in machine learning.

1.

I had the below piece of code in a training loop:
```py
outputs = model(**inputs)
loss = outputs.get("loss")
loss.backward()
optimizer.zero_grad()
optimizer.step()
```
The model was not getting trained despite debugging by varying the learning rates, changing optimizers and checking other issues. But the issue was `optimizer.zero_grad()` cleared out the gradient accumulated by `loss.backward()`.
Correct code:
```py
optimizer.zero_grad()
outputs = model(**inputs)
loss = outputs.get("loss")
loss.backward()
optimizer.step()
```

2. Not normalizing y-values in validation dataset.

I was training a regression model using deep neural networks.
The training loss decreased, training evaluation metrics were good and the training progressed well. But the RMSE in validation metrics was very high (100x the RMSE of training evaluation). It turned out that I didn't normalize the values in validation dataset.

3. Training loss not improving in a contrastive distillation based setting

There was the teacher model, the student model.
The issue here was I had only passed the parameters of the teacher model to the optimizer and not the student model, and thus the students model was not learning.

4. Subnet configuration in multi-node training

Multi-node training - I was debugging multi-node training and for some reason the training did not start. I could see no checkpoints nor anything in training logs except that data is getting loaded. The issue was in configuring of AWS Subnet - there was a misconfiguration in the subnet that made the nodes not to communicate with each other.
