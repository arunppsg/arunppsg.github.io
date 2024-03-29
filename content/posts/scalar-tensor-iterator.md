+++
title = "PyTorch Internals: Scalar and TensorIterator"
date = 2023-08-17
tags = ['pytorch']
+++

This blog touches briefly upon `Scalar` and `TensorIterator`.

## Scalar

Scalar is a data type in pytorch internal implementation.
It is used to represent a scalar value, for example tensors which are 0-dimensional.
A 0-dimensional tensor can represent an integer, a float, a double or any other value.
The type of the scalar is denoted by the attribute `ScalarType`.
`ScalarType` contains mapping to C++ types.
ScalarType stores the type while Scalar stores the value.
Internally, Scalar stores a primitive C++ value.
Both Scalar and ScalarType are implemented as a C++ classes [here](https://github.com/pytorch/pytorch/blob/384e0d104fd077d31efafc564129660e9b7a0f25/c10/core/Scalar.h#L33) and [here](https://github.com/pytorch/pytorch/blob/384e0d104fd077d31efafc564129660e9b7a0f25/c10/core/ScalarType.h#L95) respectively.
Scalars also have a couple of useful operations associated with them `log`, `negation` and then be converted to their primitive C++ type using the `to` operator.

Sample code on using a `Scalar`:

```cpp
  c10::Scalar a = 5.5;
  std::cout << "a=" << a << std::endl;
  std::cout << "element size = " << c10::elementSize(a.type()) << std::endl;

  // Converting scalar to primitive c++ type
  auto b = a.to<float>();
  auto c = a.toDouble();
```

## TensorIterator

Given an input tensor and output tensor, TensorIterator can be used for iterating over the tensors to perform pointwise operations on them. The TensorIterator also provides additional functionalities like shape broadcasting, type promotion which saves a lot of trouble by automatically handling edge cases.

In the below example, I would like to show an example of TensorIterator.
Though this is not the best way to use it, it helps for pedagogical purpose.

```cpp
  torch::Tensor x = torch::ones({2, 3});
  // TensorIterator automatically handles broadcasting
  auto y = torch::randn({3});
  auto output = torch::empty_like(x);
  // A TensorIteratorConfig is used to create a TensorIterator.
  auto iter = torch::TensorIteratorConfig()
                    .add_output(output)
                    .add_input(x)
                    .add_input(y)
                    .build();

  iter.for_each([&](char** data, const int64_t* strides, int64_t n) {
    for(int i=0; i<n; i++) {
      float* out_data = reinterpret_cast<float*>(data[0] + strides[0] * i);
      float* in_data_x = reinterpret_cast<float*>(data[1] + strides[1] * i);
      float* in_data_y = reinterpret_cast<float*>(data[2] + strides[2] * i);
      *out_data = *in_data_x + *in_data_y;
    }
  });
```

To build a `TensorIterator`, we use `TensorIteratorConfig` to specify the input and output tensors along with other additional configurations and then call `TensorIteratorConfig::build` to create the TensorIterator.
`TensorIterator` provides the `for_each` function which can be used to iterate over the tensors in the iterator.

The `for_each` method accepts a loop with a signature of `(char** data, const int64_t* strides, int64_t n)`.
The first argument `char** data` contains a `char*` pointer for each of the tensor in tensor iterator.
Having it as `char*` allows us to represent the underlying data as an array of bytes which can be reinterpreted to any other data type.
In this case, we are reinterpreting the underlying bytes as `float`.
The next argument, `strides` specify, for each of the tensor in tensor iterator, how much bytes should we move to access the next element.
Though tensors are multidimensional, they are represented in memory as a contiguous 1-D array.
The stride of a tensor says how many bytes we have to move to reach the next element along that axis.
Lastly, the argument `n` specifies the number of elements in the tensor.

The for-loop iterates over the memory location of the output and two input tensors stored in `data[0]`, `data[1]`, `data[2]` with a step size of `strides[0]`, `strides[1]`, `strides[2]` respectively.
At each location, it reinterprets the bytes as a `float` and performs the pointwise operation of addition here.


A working example of the above can be found [here](https://github.com/arunppsg/examples/blob/9dddbf809408a047e9d42ed016c888f27348a23f/cpp/others/scalar-tensor-iterator/main.cpp).

For more details about TensorIterator, I refer the readers to [this](https://labs.quansight.org/blog/2021/04/pytorch-tensoriterator-internals-update) blog post and to [this](https://labs.quansight.org/blog/2021/04/pytorch-tensoriterator-internals-update) pytorch-dev podcast by ezyang. The TensorIteratorConfig class is defined in [TensorIterator.h](https://github.com/pytorch/pytorch/blob/384e0d104fd077d31efafc564129660e9b7a0f25/aten/src/ATen/TensorIterator.h#L753) and the `struct TensorIterator` is defined [here](https://github.com/pytorch/pytorch/blob/384e0d104fd077d31efafc564129660e9b7a0f25/aten/src/ATen/TensorIterator.h#L232).

In case you have any comments, questions, I would be glad to hear them. Feel free to reach out to me at arunppsg AT gmail DOT com.
