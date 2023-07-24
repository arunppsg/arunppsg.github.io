+++
title = "torch.renorm operation in numpy"
date = 2023-07-24
tags = ['numpy', 'pytorch', 'linear-algebra']
+++

I have made a numpy implementation of [`torch.renorm`](https://pytorch.org/docs/stable/generated/torch.renorm.html) operation.

```
import numpy as np

def renorm(x, p, dim, maxnorm):
    x_view = np.rollaxis(x, dim, 0)
    n = x.shape[dim]
    norms = []
    for i in range(n):
        norms.append(np.linalg.norm(x_view[i,:], ord=2))

    factors = []
    for norm in norms:
        if norm > maxnorm:
            factors.append(maxnorm/norm)
        else:
            factors.append(1)
    factors = np.array(factors)
    return x * factors.reshape(-1, 1), factors
```
