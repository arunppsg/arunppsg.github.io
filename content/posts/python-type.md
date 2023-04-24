+++
title = "Objects in Python"
date = 2023-04-03
tags = ["python"]
+++

Everything in Python has a type (even the type `type`!) because everything is an object.

Objects are abstraction of data in Python.
All data in a Python program is stored as a object.

Instances can be created from objects, which themselves are another kind of object.
Objects created can be destroyed by garbage collection.

An object has three properties - identity, value, type.
The `id` of an object never changes once an object is created.
`id(x)` returns an unique identity to the object `x`. 

When the value of object is changeable, the object is said to be mutable and when the value is not changeable, the object is said to be immutable.

## `type` object

`type` is an object which can be used to create other objects.
For example, the `type` object is used internally to create `class` objects.
An user-defined class is an object of type `type`.
It is a new kind of type (instance) of the type class.

The type of `type` object is `type`.
For `type` object, the type is an identity.
Example: `print (type(type))` prints `<class 'type'>`

## `function` object

A function is also another instance of `type` object.
When we define a function, the defined function is an instance of the function object.

Example:
```
def foo():
    return

print (type(foo))  # <class 'function'>
print (type(type(foo)))  # <class 'type'>
```

## `class` object
In python, all classes are themselves instances of other classes.
`class` objects are instances of `type` class.
A class also allows to makes instances of it's type.


```python3
class Foo:
    pass

print (type(Foo)) # <class 'type'>
```

### Instance method object

A instance method object is same as a function object but it accepts a class instance as a first argument.
It combines a class, a class instance and any callable user-defined function.

Example:

```python3
class Foo():
    def print_self(self):
         print ('type ': self, 'id ': id(self))

f = Foo()
print (type(f))  # output: type <class '__main__.Foo'> id 4408722096
f.print_self()  # output: type <class '__main__.Foo'> id 4408722096
```

The above example shows that both the instance `f` and `self` are the same and that `f` is passed as an argument to the method object in the class.

```python3
class Foo():
    
    def __init__(self):
        self.b = 5

    def bar(self):
        print ('in bar')

f = Foo()

print (id(Foo.bar), id(f.bar))  # (4573538336, 4573593280)
```
Note that `Foo.bar` has a different id from `f.bar`.
When an instance of the class is created, the instance method objects are also recreated in the instance.

## `list` object

A list is also an object of type class.
`type(list)` , prints `<class 'type'>`.
Instances of list class can be created using the shorthand of square brackets.
Example: `a = [1, 2]` creates a `list` object identified by `a`.

## `int` class 

A question and an answer.

Why does id(a) and id(b) are same in below example but different in the following example?

```
# case 1: same identity
>>> a_int, b_int = 1, 1
>>> id(a_int), id(b_int)
(4298998000, 4298998000)

# case 2: different identity
>>> a_list, b_list = [], []
>>> id(a_list), id(b_list)
(4303367872, 4303371648)
```

In case 1, the token `1` is an object of class int.
`print (type(1))` returns `<class 'int'>`.
`print (type(type(1))` and it returns `<class 'type'>`.
Hence, the token `1` is an object of class int.
All objects have ids.
The id of token 1 can be seen by `print(id(1))` and it can be inferred that it is same as `id(a_int)`.

In the assignment `a_int = 1`, `a_int` becomes a reference to the token `1`.
Python makes a reference here because `1` is an object of immutable type in python.

But in case 2, the values are copied because `[]` is a mutable type.
Hence, in case 2, `a_list` and `b_list` have different ids.

## Other notes

`id` is itself an object of class `builtin_function_or_method`.
Since it is an object, it also has an `id` which can be viewed as `id(id)`.

`lambda` expressions are object of type `function`.

The keywords `staticmethod` and `classmethod` are objects themselves.

## Acknowledgment

A special thanks to [Rahul Sai Poruri](https://rahulporuri.github.io/) and [Tony Davis](https://tonyd.co/) for discussions and feedbacks on earlier versions of the draft.
