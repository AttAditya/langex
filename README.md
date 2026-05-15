# [LangEx](https://pypi.org/project/langex/) 

Extended Language Support for Python

[![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpypi.org%2Fpypi%2Flangex%2Fjson&query=info.version&prefix=v&style=for-the-badge&logo=pypi&logoColor=%23ffffff&label=PyPI%20Release&labelColor=%230073b7&color=%23ffffff&link=https%3A%2F%2Fpypi.org%2Fproject%2Flangex%2F&cacheSeconds=30)](https://pypi.org/project/langex/)
[![Sponsor](https://img.shields.io/badge/Sponsor%20PROJECT-db61a2?style=for-the-badge&logo=github)](https://github.com/sponsors/AttAditya)

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
- Utility classes like Singleton
- Runtime validation utilities
- Decorator-based language extensions
- Runtime argument and return type checking
- Lightweight core inspection tools
- An abstracted testing toolkit

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

### Singleton Class Example

```py
from langex.core.classes import singleton

@singleton
class IdGenerator:
  def __init__(self, initial = 0):
    self.value = initial

  def next_id(self):
    self.value += 1
    return self.value

id_gen1 = IdGenerator()
id_gen2 = IdGenerator()

print(id_gen1.next_id()) # prints 1 in console
print(id_gen1.next_id()) # prints 2 in console
print(id_gen2.next_id()) # prints 3 in console

print(id_gen1 is id_gen2) # prints True in console
```

## Project Structure

```tree
langex
├── __init__.py
├── __main__.py
├── classes
│   ├── __init__.py
│   ├── class_meta.py
│   ├── methods_meta.py
│   └── singleton.py
├── constants
│   ├── __init__.py
│   ├── contents.py
│   ├── keys.py
│   └── labels.py
├── core
│   ├── __init__.py
│   ├── classes.py
│   ├── functions.py
│   └── testing.py
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
│   ├── signature_parser.py
│   └── signature.py
├── testing
│   ├── __init__.py
│   ├── data.py
│   └── helpers.py
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
- The **constants** module contains constant strings and keys used across the project for metadata, attributes and validation.
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

## Contributors

<a href="https://github.com/attaditya/langex/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=attaditya/langex" />
</a>

## Support

If you find this project useful, please consider supporting it by **starring the GitHub repository** or sharing it with others who might benefit from it.

Your support helps in the continued development and improvement of the project.

You can also **contribute to the project** by submitting issues, suggesting features, or even contributing code through pull requests.

You can also sponsor the project on GitHub Sponsors: [GitHub Sponsors - AttAditya](https://github.com/sponsors/AttAditya)

---

> _Made with <3 by [AttAditya](https://github.com/AttAditya)_

