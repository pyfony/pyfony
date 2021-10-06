## Bundle basics

There are some differences that distinguish bundle from a standard python package. The most important are the following:

### 1. Base dependencies

```toml
[tool.poetry.dependencies]
pyfony-bundles = "[enter version]" # bundle base libraries
console-bundle = "[enter version]" # (optional) if you want your bundle to be able to define console commands

[tool.poetry.dev-dependencies]
pyfony-core = "[enter version]" # used for testing only in bundle development
```

* [console-bundle](https://github.com/pyfony/console-bundle) - empowering Pyfony with pluggable CLI commands
* [logger-bundle](https://github.com/pyfony/logger-bundle) - base logging bundle, enables stdout logging and introduces API for custom log handlers

### 2. Bundle initialization file

Usually stored in `src/[rootmodule]/[BundleName].py`.

Imagine having the following SomeBundle file stored in the `[rootmodule]/src/SomeBundle.py` file:

```python
from pyfonybundles.Bundle import Bundle

class SomeBundle(Bundle):
    pass
```

### 3. Entry point registration

Each bundle class must be registered using the following entry point defined in pyproject.toml:

```toml
[tool.poetry.plugins."pyfony.bundle"]
create = "somebundle.SomeBundle:SomeBundle"
```

### 4. Bundle configuration

Usually stored in `src/[rootmodule]/_config/config.yaml`.

Each bundle must have its configuration parameters namespaced with the bundle name:

```yaml
parameters:
  somebundle:
    foo:
      bar: "Hello world"
```

Similarly, you can define bundle's services:

```yaml
services:
  somebundle.foo.bar.HelloWorldService:
```
