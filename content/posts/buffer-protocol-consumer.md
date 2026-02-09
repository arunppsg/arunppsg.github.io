+++
title = "Consuming Buffer Exposed by the Python Buffer Protocol"
date = 2024-02-25
[taxonomies]
tag = ["python"]
+++

Sometime back, I read a wonderful blog post on [Introduction to the Python Buffer Protocol](http://jakevdp.github.io/blog/2014/05/05/introduction-to-the-python-buffer-protocol/) which shared about exposing a python object's underlying memory (buffer) using the [python buffer protocol](https://docs.python.org/3/c-api/buffer.html).
The buffer protocol helps in accessing the underlying memory of an array without creating an intermediate copy of array.
This is useful to manipulate large arrays of data where copying of the entire data can be expensive.
As a follow-up, I decided to figure out how to consume the buffer exposed by the buffer protocol.

The goal of the next section is to develop a module `consumer` which can consume the buffer exposed by `array.array` type via the method `consume`. In other words, we are going to make this below code snippet work:

```py
import array
import consumer as C

arr = array.array('i', [1, 2, 3, 4, 5])
array_consumed = C.consume(arr)
print (array_consumed)
# prints [ 1 2 3 4 5 ]
```

# Step 1
Create a C-library `consumer_lib.c` which defines the `ConsumerArray` and contains utilities for allocating, deallocating and printing the array. This is same as the `mylib.c` from the [Introduction to the Python Buffer Protocol](http://jakevdp.github.io/blog/2014/05/05/introduction-to-the-python-buffer-protocol/) blog post. The `ConsumerArray` is the data-structure which maps to the buffer exposed by `array.array`.
```c
#include <stdlib.h>
#include <stdio.h>

typedef struct {
	int *arr;
	long length;
} ConsumerArray;

void initialize_ConsumerArray(ConsumerArray *a, long length) {
	a->length = length;
	a->arr = (int*)malloc(sizeof(int) * length);
	int i;
	for(i = 0; i < length; i++) {
		a->arr[i] = i;
	}
}

char* stringify_ConsumerArray(ConsumerArray *a, int nmax) {
	char *s = (char*)malloc(nmax * 20);
	int pos = sprintf(&s[0], "[ ");
	int i;
	for(i = 0; i < a->length && i < nmax; i++){
		pos += sprintf(&s[pos], "%d ", a->arr[i]);
	}
	if(i < a->length)
		pos += sprintf(&s[pos], "... ");
	sprintf(&s[pos], "]");
	return s;
}

void print_ConsumerArray(ConsumerArray *a, int nmax) {
	char *string = stringify_ConsumerArray(a, nmax);
	printf("%s", string);
}

void deallocate_ConsumerArray(ConsumerArray *a) {
	free(a->arr);
	a->arr = NULL;
}
```

## Step 2
Create the `consumer` python module with a method `consume` and the type `PyConsumerArray`.
The `consume` method is used for accessing the buffer and mapping it to the `PyConsumerArray` type.

```c
#include <Python.h>
#include "consumer_lib.c"

// Defining the PyConsumerArray type
typedef struct {
	PyObject_HEAD
	ConsumerArray arr;
	int from_buffer;
} PyConsumerArray;

static void
PyConsumerArray_dealloc(PyConsumerArray* self) {
	// If obtained view buffer, only decrement the reference count.
	// Else, if the object was created using malloc, deallocate it using free.
	if (self->from_buffer) {
		Py_XDECREF(&self->arr);
	} else {
		deallocate_ConsumerArray(&self->arr);
	}
	Py_TYPE(self)->tp_free((PyObject*)self);
}

static int
PyConsumerArray_init(PyConsumerArray *self, PyObject *args, PyObject *kwds) {
	int length = 0;
	static char *kwlist[] = {"length", NULL};
	if(!PyArg_ParseTupleAndKeywords(args, kwds, "|i", kwlist, &length)) {
		return -1;
	}

	if (length < 0)
		length = 0;

	initialize_ConsumerArray(&self->arr, length);
	self->from_buffer = 0;
	return 0;
}

static PyObject *
PyConsumerArray_str(PyConsumerArray *self) {
	char *str = stringify_ConsumerArray(&self->arr, 10);
	PyObject *ret = PyUnicode_FromString(str);
	free(str);
	return ret;
}

static PyTypeObject PyConsumerArrayType = {
	.ob_base = PyVarObject_HEAD_INIT(NULL, 0)
	.tp_name = "consumer.PyConsumerArray",
	.tp_doc = PyDoc_STR("Consumer Array objects"),
	.tp_basicsize = sizeof(PyConsumerArray),
	.tp_flags = Py_TPFLAGS_DEFAULT,
	.tp_new = PyType_GenericNew,
	.tp_dealloc = (destructor) PyConsumerArray_dealloc,
	.tp_repr = (reprfunc) PyConsumerArray_str,
	.tp_str = (reprfunc) PyConsumerArray_str,
	.tp_init = (initproc) PyConsumerArray_init,
};

// consume method for consuming the array object
static PyObject *
consumer_consume(PyObject *obj, PyObject *args) {
	PyObject *buffer_obj;
	Py_buffer view;
	if (!PyArg_ParseTuple(args, "O", &buffer_obj)) {
		return NULL;
	}

	if (!PyObject_CheckBuffer(buffer_obj)) {
		PyErr_SetString(PyExc_ValueError, "The object does not support buffer protocol.");
		return NULL;
	}

	if (PyObject_GetBuffer(buffer_obj, &view, PyBUF_SIMPLE) < 0) {
	 	return NULL;
	}

 	PyConsumerArray *ca = (PyConsumerArray *)PyType_GenericAlloc(&PyConsumerArrayType, 0);
	if(ca == NULL) {
		PyBuffer_Release(&view);
		return NULL;
	}

	ca->arr.arr = view.buf;
	ca->arr.length = (long)view.len / view.itemsize;
	ca->from_buffer = 1;

	PyBuffer_Release(&view);
	return (PyObject *)ca;
}

static PyMethodDef ConsumerMethods[] = {
	{"consume", consumer_consume, METH_VARARGS, "consumer method"},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef consumer_module = {
	PyModuleDef_HEAD_INIT,
	.m_name = "consumer",
	.m_doc = "consumer module",
	.m_size = -1,
	.m_methods = ConsumerMethods,
};

PyMODINIT_FUNC
PyInit_consumer(void) {
	PyObject *m;

	if(PyType_Ready(&PyConsumerArrayType) < 0){
		return NULL;
	}

	m = PyModule_Create(&consumer_module);
	if(m == NULL)
		return NULL;

	Py_INCREF(&PyConsumerArrayType);
	if(PyModule_AddObject(m, "PyConsumerArray", (PyObject*)&PyConsumerArrayType) < 0) {
		Py_DECREF(&PyConsumerArrayType);
		Py_DECREF(&m);
		return NULL;
	}

	return m;
}
```

We will save the above in a file named `consumer.c`.

## Step 3 - build it
Build the python module as `python3 setup.py build_ext --inplace` using the `setup.py` script containing:
```py
from distutils.core import setup, Extension

setup(name="consumer", ext_modules=[Extension("consumer", ["consumer.c"])])
```

Now, using the `consumer.consume` method, we can read arrays which support buffer protocol without making a copy of the data.
