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
    token: '%env(API_TOKEN)%'

services:
    mycompany.api.ApiClient:
      arguments:
        - '@mycompany.api.Authenticator'

    mycompany.api.Authenticator:
      class: mycompany.authenticator.RestAuthenticator
      arguments:
        - '%api.endpoint%'
        - '%api.token%'
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
