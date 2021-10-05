## Bundle basics

There are some differences that distinguish bundle from a standard python package. The most important are the following:

### 1. Bundle initialization file

Usually stored in `src/[rootmodule]/[BundleName].py`.

Imagine having the following SomeBundle file stored in the `[rootmodule]/src/SomeBundle.py` file:

```python
from pyfonybundles.Bundle import Bundle

class SomeBundle(Bundle):
    pass
```

### 2. Entry point registration

Each bundle class must be registered using the following entry point defined in pyproject.toml:

```toml
[tool.poetry.plugins."pyfony.bundle"]
create = "somebundle.SomeBundle:SomeBundle"
```

### 3. Bundle configuration

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
