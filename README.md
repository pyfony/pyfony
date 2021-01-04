# Pyfony framework

Pyfony is a **Dependency Injection (DI) powered framework** written in Python greatly inspired by the [Symfony Framework](https://symfony.com/) in PHP & [Spring Framework](https://spring.io/projects/spring-framework) in Java.

The DI functionality is provided by the [Injecta Dependency Injection Container](https://github.com/pyfony/injecta).

Pyfony = **Injecta + bundles (extensions) API**

## Installation

```
$ pip install pyfony
```

## Pyfony initialization

(The following steps are covered in the [PyfonyBundleTest](src/pyfony/PyfonyBundleTest.py))

To start using Pyfony, create a simple `config_dev.yaml` file to define your DI services:

```yaml
parameters:
  api:
    endpoint: 'https://api.mycompany.com'

services:
    mycompany.api.ApiClient:
      arguments:
        - '@mycompany.api.Authenticator'

    mycompany.api.Authenticator:
      class: mycompany.authenticator.RestAuthenticator
      arguments:
        - '%api.endpoint%'
        - '%env(API_TOKEN)%'
```

Then, initialize the container:

```python
from injecta.config.YamlConfigReader import YamlConfigReader
from pyfony.Kernel import Kernel
from pyfonybundles.loader import pyfonyBundlesLoader

appEnv = 'dev'

kernel = Kernel(
    appEnv,
    '/config/dir/path', # must be directory, not the config_dev.yaml file path!
    pyfonyBundlesLoader.loadBundles(),
    YamlConfigReader()
)

container = kernel.initContainer()
```

Use `container.get()` to finally retrieve your service:

```python
from mycompany.api.ApiClient import ApiClient

apiClient = container.get('mycompany.api.ApiClient') # type: ApiClient   
apiClient.get('/foo/bar')
```

## Advanced examples

1. [Advanced services configuration using Injecta](https://github.com/pyfony/injecta/blob/master/README.md)
1. [Extending Pyfony with bundles](docs/bundles.md)
