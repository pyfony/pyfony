# Pyfony framework

Pyfony is a **Dependency Injection (DI) powered framework** written in Python greatly inspired by the [Symfony Framework](https://symfony.com/) in PHP & [Spring Framework](https://spring.io/projects/spring-framework) in Java.

## Installation

```
$ pip install pyfony
```

## Simple container initialization

To start using Pyfony, create a simple `config.yaml` file to define your DI services:

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
from pyfony.ContainerBuilder import ContainerBuilder
from injecta.config.YamlConfigReader import YamlConfigReader
from pyfony.PyfonyBundle import PyfonyBundle
from injecta.container.ContainerInitializer import ContainerInitializer

configPath = '/path/to/config.yaml'
appEnv = 'dev'

containerBuild = ContainerBuilder().build(
    YamlConfigReader().read(configPath),
    [PyfonyBundle()],
    appEnv,
    configPath,
)

container = ContainerInitializer().init(containerBuild)
```

Use `container.get()` to finally retrieve your service:

```python
from mycompany.api.ApiClient import ApiClient

apiClient = container.get('mycompany.api.ApiClient') # type: ApiClient   
apiClient.get('/foo/bar')
```

## Advanced examples

1. [Configuring services using parameters](docs/parameters.md)
1. [Service autowiring](docs/autowiring.md)
1. [Using service factories](docs/factories.md)
1. [Tagged services](docs/tagging.md)
