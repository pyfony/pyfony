# Bundle development

### 1. Development configuration file

Create an empty `src/[rootmodule]/_config/config_dev.yaml` to define your custom development configuration.

### 2. Bundle bootstrap configuration

Add the following configuration into you bundle's pyproject.toml file:

```toml

[pyfony.bootstrap]
container_init = "pyfonycore.container.container_init:init_with_current_bundle"
root_module_name = "somebundle"
```

### 3. Bundle composition test

Create a new test suite (usually in `src/[rootmodule]/SomeBundleTest.py`) to validate that services in your bundle can be properly composed.

The following test code requires:

* pytest - install it by calling `poetry add pytest="^5.2" --dev`
* empty `src/[rootmodule]/_config/config_test.yaml` file to be created 

```python
import unittest
from injecta.testing.services_tester import test_services
from pyfonycore.bootstrap import bootstrapped_container


class SomeBundleTest(unittest.TestCase):
    def test_init(self):
        container = bootstrapped_container.init("test")
        test_services(container)


if __name__ == "__main__":
    unittest.main()
```

### 4. Testing bundle inside your project

In your project's pyproject.toml file add a new development dependency by using the following syntax and call `poetry update some-bundle`.

```toml
[tool.poetry.dependencies]
some-bundle = {path = "/path/to/bundle", develop = true}
```

By using this approach, all the changes made in the bundle's code will be immediately propagated into your project. The bundle directory is simply symlinked into your project virtual environment.

For more details, check [poetry's documentation](https://python-poetry.org/docs/dependency-specification/#path-dependencies)
