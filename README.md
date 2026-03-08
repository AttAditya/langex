# [LangEx](https://pypi.org/project/langex/)

Extended Language Support for Python

## Installation

```sh
pip install langex
```

## About

LangEx is an experimental Python library that introduces additional language-level constructs using decorators, metadata inspection, and structural validation. It focuses on enabling capabilities that Python does not strictly enforce by default, such as interface-like behavior and structured object metadata.

The project builds small language utilities that operate on Python objects (functions, classes, and other callables) to inspect, validate, and extend their behavior while remaining fully compatible with standard Python.

## Features
- Interface-like constructs for Python classes
- Metadata extraction for Python objects and callables
- Runtime validation utilities
- Decorator-based language extensions
- Lightweight core inspection tools

## Example

### Defining an Interface

```py
from langex.interface import interface

@interface
class Repository:
  def save(self, data): ...
  def get(self, id): ...
```

### Implementing the Interface

```py
from langex.interface import implements

@implements(Repository)
class UserRepository:
  def save(self, data):
    ...

  def get(self, id):
    ...
```

If required methods are missing, validation will raise an error.

## Project Structure

```tree
langex
├── __init__.py
├── __main__.py
├── immediate.py
├── interface.py
├── core
│   ├── __init__.py
│   ├── callable_meta.py
│   ├── class_meta.py
│   ├── meta.py
│   ├── object_meta.py
│   └── use.py
```

The core module provides internal abstractions for inspecting Python objects and extracting structured metadata used by higher-level utilities like interfaces and validations.

## Design Philosophy

LangEx is designed around a few principles:
- Pure Python implementation
- Minimal runtime overhead
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

