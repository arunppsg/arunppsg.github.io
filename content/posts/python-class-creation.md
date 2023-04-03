+++
title = "Class Creation in Python"
date = 2023-03-07
tags = ["python"]
+++

In python, all classes are an instance of an other class.
An user-defined class is an instance of `type` class.

```python
class Foo:
    
    def __init__(self, a):
        self.a = a 

    def get_a(self):
        return self.a

    def set_a(self, a):
        self.a = a
```
For the above class `Foo`, `print (type(Foo))` shows `<class 'type'>`.
The `class` keyword creates an instance of `type` object which can be identified using `Foo`.
A class object also allows to makes instances of it's type by using its identifier (`Foo`).

Here is an another way to create a class object by directly creating an instance of type class.

```

def get_a(arg1):
    return arg1.a

def set_a(arg1, i):
    arg1.a = i

def __init__(arg1, a):
    arg1.a = a

Foo = type('Foo', (), dict(get_a=get_a, set_a=set_a, 
          __init__=__init__))
```

Here, we directly invoke `type()` constructor to create the class object.
The `type()` constructor has the signature `type(name, bases, namespace)`.
`name` is a string giving the name of the class to be constructed, `bases` is a tuple which identifies the parent classes of the class to be constructed and `namespace` is a dictionary of attributes and methods of the class to be constructed.



## Customising class creation

### Using `__new__` method

`__new__` can be used to control creation of object.
For example, to implement a singleton object, we can use `__new__`.
Here is another example of using `__new__` object:
```
class Number(tuple):

    def __new__(cls, *args):
        if not isinstance(args[0], int):
            raise ValueError('argument should be an integer')

        if (args[0] % 2 == 0):
            return tuple.__new__(tuple, (args[0], 'even'))
        elif (args[0] % 2 == 1):
            return tuple.__new__(tuple, (args[0], 'odd'))

a = Number(1)  # `a` stores (1, 'odd')
b = Number(2)  # `b` stores (2, 'even')
```

In the above example, we customise the creation of a tuple.
The `__new__` method is used to customise the creation of `tuple` since once a tuple is created, it cannot be modified.

`__new__` creates a new instance of the class.
The `__new__` method is the different from `__init__`.
It creates the actual class object while the `__init__` method customizes the created object.

### Customising via metaclass

The class of a class is knows as metaclass.
Most classes have `type` as their metaclass as `type` is the class which is used to create the *class*.

We can customise class creation by using the `metaclass` keyword in class definition or by inheriting from an existing class that included such argument.

A metaclass can customise preparation of class namespace and resolving of method resolution order.

Example
```
class Meta(type):
    pass

class Foo(metaclass=Meta):

    def __init__(self):
        pass

if __name__ == "__main__":
    print ('type of Foo is ', type(Foo))  # shows `<class '__main__.Meta'>`
    print ('type of Meta is ', type(Meta))  # shows `<class 'type'>`.
```

The above snippet shows `<class '__main__.Meta'>` and `<class 'type'>`.
I leave it to a future post for covering customisation of class creation via metaclasses.

### `__init_subclass__` hook

The `__init_subclass__` hook when defined in the parent class of a class can modify attributes in the subclass, thus changing the subclass's behavior.
For more details, I refer the reader to [python documentation](https://docs.python.org/3/reference/datamodel.html#object.__init_subclass__)

## References
- [`__new__` vs `__init__` from python mailing list](https://mail.python.org/pipermail/tutor/2008-April/061426.html)
- [Data Model](https://docs.python.org/3/reference/datamodel.html)

## Acknowledgemnets

A special thanks to [Rahul Sai Poruri](https://rahulporuri.github.io/) for discussions and feedbacks on earlier versions of the draft.
