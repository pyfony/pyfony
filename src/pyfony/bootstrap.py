import os
from pathlib import Path
import tomlkit
from injecta.container.ContainerInterface import ContainerInterface
from injecta.dtype.classLoader import loadClass
from tomlkit.toml_document import TOMLDocument

def initContainer(appEnv: str) -> ContainerInterface:
    initCallable = loadClass(*readContainerInit())

    return initCallable(appEnv)

def readContainerInit():
    workingDir = Path(os.getcwd())
    bootstrapConfig = loadConfig(workingDir.joinpath('pyproject.toml'))

    return getContainerInit(bootstrapConfig)

def configExists(config: dict):
    return 'pyfony' in config and 'bootstrap' in config['pyfony']

def loadConfig(pyprojectPath: Path):
    config = _readPyproject(pyprojectPath)
    return getBootstrapConfig(config)

def getBootstrapConfig(config: dict):
    if 'pyfony' not in config:
        raise Exception('[pyfony] section is missing in pyproject.toml')

    if 'bootstrap' not in config['pyfony']:
        raise Exception('[pyfony.bootstrap] section is missing in pyproject.toml')

    return config['pyfony']['bootstrap']

def getContainerInit(bootstrapConfig: dict):
    if 'container-init' not in bootstrapConfig:
        raise Exception('container-init is missing in [pyfony.boostrap] in pyproject.toml')

    return bootstrapConfig['container-init'].split(':')

def _readPyproject(pyprojectPath: Path) -> TOMLDocument:
    with pyprojectPath.open('r', encoding='utf-8') as t:
        return tomlkit.parse(t.read())
