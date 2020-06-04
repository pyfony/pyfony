# Extending Pyfony with bundles

Pyfony can be easily extended using first or third party bundles.

The default Pyfony setup is shipped with the following bundles:

* [console-bundle](https://github.com/pyfony/console-bundle) - empowering Pyfony with pluggable CLI commands
* [logger-bundle](https://github.com/pyfony/logger-bundle) - base logging bundle, enables stdout logging and introduces API for custom log handlers

To enable these bundles, create a custom Kernel:   

```python
from typing import List
from pyfonybundles.Bundle import Bundle
from pyfony.kernel.BaseKernel import BaseKernel
from loggerbundle.LoggerBundle import LoggerBundle
from consolebundle.ConsoleBundle import ConsoleBundle

class AppKernel(BaseKernel):

    def _registerBundles(self) -> List[Bundle]:
        return [
            ConsoleBundle(),
            LoggerBundle(),
        ]
```

Then, use the `AppKernel` to initialize the container:

```python

from injecta.config.YamlConfigReader import YamlConfigReader

appEnv = 'dev'

kernel = AppKernel(
    appEnv,
    '/config/dir/path', # must be directory, not the config_dev.yaml file path!
    YamlConfigReader()
)

container = kernel.initContainer()
```
