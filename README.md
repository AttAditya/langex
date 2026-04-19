# [LangEx](https://pypi.org/project/langex/)

Extended Language Support for Python

## Installation

```sh
pip install langex
```

## About

LangEx is an experimental Python library that introduces additional language-level constructs using decorators, metadata inspection, and runtime validation.

It focuses on enabling capabilities that Python does not strictly enforce by default, such as interface-like structures, structured metadata, and runtime type validation.

The project builds small language utilities that operate on Python objects (functions, classes, and other callables) to inspect, validate, and extend their behavior while remaining fully compatible with standard Python.

## Features

- Interface-like constructs for Python classes  
- Metadata extraction for Python objects and callables  
- Runtime validation utilities  
- Decorator-based language extensions  
- Runtime argument and return type checking  
- Lightweight core inspection tools  

## Example

### Defining and using an Interface

```py
from langex.core.classes import implements, interface
from langex.core.functions import args_required, returns

@interface
class InterfaceClass:
  @args_required(int)
  @returns(int)
  def method1(self, a: int) -> int:
    ...

  @args_required(str)
  @returns(str)
  def method2(self, b: str) -> str:
    ...

@implements(InterfaceClass)
class ImplementationClass:
  def __init__(self, factor):
    self.factor = factor

  def method1(self, a: int) -> int:
    return a * self.factor

  def method2(self, b: str) -> str:
    return b.upper() * self.factor

instance = ImplementationClass(3)
print(instance.method1(5)) # prints 15 in console
print(instance.method2("hi")) # prints "HIHIHI" in console
print(instance.method1("5")) # raises Langex Validation Error
print(instance.method2(5)) # raises Langex Validation Error
```

### Runtime Type Enforcement

```py
from langex.core.functions import args_required, returns

@args_required(int, int)
@returns(int)
def add(a, b):
  return a + b

print(add(1, 2)) # prints the integer 3 in console
print(add("1", "2")) # raises Langex Validation Error
```

LangEx records type metadata and enforces it when the function is executed.

## Project Structure

```tree
langex
├── __init__.py
├── __main__.py
├── classes
│   ├── __init__.py
│   ├── class_meta.py
│   └── methods_meta.py
├── core
│   ├── __init__.py
│   ├── classes.py
│   └── functions.py
├── errors
│   ├── __init__.py
│   ├── instantiation.py
│   ├── langex.py
│   ├── misapplication.py
│   ├── unimplemented.py
│   └── validation.py
├── functions
│   ├── __init__.py
│   ├── args_meta.py
│   ├── function_meta.py
│   ├── returns_meta.py
│   └── signature.py
├── utils
│   ├── __init__.py
│   ├── extracter.py
│   └── matcher.py
└── validation
    ├── __init__.py
    ├── kw_args_validator.py
    ├── pos_args_validator.py
    ├── returns_validator.py
    └── validator.py
```

### Module Overview

- The **core** module contains the core decorators and utilities for language extensions.
- The **classes** module contains tools for class inspection and interface-like constructs.
- The **functions** module contains tools for function metadata and signature inspection.
- The **validation** modules contain logic for validating function arguments and return values at runtime.
- The **utils** module contains helper functions for type matching and other utilities.
- The **errors** module defines custom exceptions for validation and other errors.

## Design Philosophy

LangEx is designed around a few principles:

- Pure Python implementation
- Explicit developer intent
- Small composable language utilities

Rather than acting as a framework, LangEx provides foundational language tools that can be used to build higher-level abstractions.

## Status

Experimental and under active development.  
APIs and structure may evolve as the project grows.

## Links

- [PyPI](https://pypi.org/project/langex/)
- [GitHub](https://github.com/attaditya/langex)
- [License](https://github.com/attaditya/langex/tree/main/LICENSE)

> _Made with <3 by [AttAditya](https://github.com/AttAditya)_

