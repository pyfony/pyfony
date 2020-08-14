import os
from typing import List
from injecta.config.ConfigReaderInterface import ConfigReaderInterface
from injecta.container.ContainerBuilder import ContainerBuilder
from injecta.container.ContainerInitializer import ContainerInitializer
from injecta.container.ContainerInterface import ContainerInterface
from pyfonybundles.Bundle import Bundle
from pyfony.container.PyfonyHook import PyfonyHooks
from injecta.config.ConfigMerger import ConfigMerger

class BaseKernel:

    _allowedEnvironments = ['dev', 'test', 'prod']

    def __init__(
        self,
        appEnv: str,
        configDir: str,
        configReader: ConfigReaderInterface
    ):
        if appEnv not in self._allowedEnvironments:
            raise Exception('Unexpected environment: {}'.format(appEnv))

        self._appEnv = appEnv
        self._configDir = configDir
        self.__configReader = configReader
        self._containerBuilder = ContainerBuilder()
        self.__configMerger = ConfigMerger()

    def initContainer(self) -> ContainerInterface:
        bundles = self._registerBundles()

        hooks = PyfonyHooks(
            bundles,
            self._getConfigPath(),
            self._appEnv
        )

        projectBundlesConfig = self._loadProjectBundlesConfig(bundles)
        projectConfig = self.__configReader.read(self._getConfigPath())

        config = self.__configMerger.merge(projectBundlesConfig, projectConfig)

        containerBuild = self._containerBuilder.build(config, hooks)

        container = ContainerInitializer().init(containerBuild)

        self._boot(container)

        return container

    def _getConfigPath(self):
        return self._configDir + '/config_{}.yaml'.format(self._appEnv)

    def _getProjectBundlesConfigDir(self):
        return os.path.dirname(self._getConfigPath()) + '/bundles'

    def _loadProjectBundlesConfig(self, bundles: List[Bundle]):
        bundlesConfigsDir = self._getProjectBundlesConfigDir()
        config = dict()

        for bundle in bundles:
            rootPackageName = bundle.__module__[:bundle.__module__.find('.')]
            projectBundleConfigPath = bundlesConfigsDir + '/' + rootPackageName + '.yaml'

            if os.path.exists(projectBundleConfigPath):
                projectBundleConfig = self.__configReader.read(projectBundleConfigPath)

                config = self.__configMerger.merge(config, projectBundleConfig, False)

        return config

    def _registerBundles(self) -> List[Bundle]:
        return []

    def _boot(self, container: ContainerInterface):
        for bundle in self._registerBundles():
            bundle.boot(container)
