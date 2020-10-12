import os
from typing import List
from box import Box
from injecta.compiler.CompilerPassInterface import CompilerPassInterface
from injecta.config.ConfigMerger import ConfigMerger
from injecta.container.ContainerBuild import ContainerBuild
from injecta.container.Hooks import Hooks
from injecta.service.Service import Service
from pyfonybundles.Bundle import Bundle
from pyfonybundles.BundleManager import BundleManager

class PyfonyHooks(Hooks):

    def __init__(
        self,
        bundles: List[Bundle],
        configPath: str,
        projectBundlesConfigDir: str,
        appEnv: str
    ):
        self.__configMerger = ConfigMerger()
        self.__bundleManager = BundleManager(bundles)
        self.__configPath = configPath
        self.__projectBundlesConfigDir = projectBundlesConfigDir
        self.__appEnv = appEnv

    def start(self, rawConfig: dict) -> dict:
        bundlesConfig = self.__bundleManager.getBundlesConfig()
        projectBundlesConfig = self.__bundleManager.getProjectBundlesConfig(self.__projectBundlesConfigDir)

        rawConfig = self.__configMerger.merge(
            self.__configMerger.merge(bundlesConfig, projectBundlesConfig),
            rawConfig
        )

        return self.__bundleManager.modifyRawConfig(rawConfig)

    def servicesPrepared(self, services: List[Service]) -> List[Service]:
        return self.__bundleManager.modifyServices(services)

    def getCustomParameters(self) -> dict:
        pyfonyCustomParameters = {
            'project': {
                'configDir': os.path.dirname(self.__configPath),
            },
            'kernel': {
                'environment': self.__appEnv,
            },
        }

        return self.__configMerger.merge(super().getCustomParameters(), pyfonyCustomParameters, False)

    def parametersParsed(self, parameters: Box) -> Box:
        return self.__bundleManager.modifyParameters(parameters)

    def containerBuildReady(self, containerBuild: ContainerBuild):
        for compilerPass in self.__bundleManager.getCompilerPasses(): # type: CompilerPassInterface
            compilerPass.process(containerBuild)
