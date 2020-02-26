import os
from typing import List
from injecta.generator.Tag2ServicesPreparer import Tag2ServicesPreparer
from injecta.compiler.CompilerPassInterface import CompilerPassInterface
from injecta.container.ContainerBuild import ContainerBuild
from injecta.service.ServicesPreparer import ServicesPreparer
from injecta.service.DTypeResolver import DTypeResolver
from injecta.parameter.ParametersParser import ParametersParser
from injecta.service.Classes2ServicesBuilder import Classes2ServicesBuilder
from injecta.autowiring.ArgumentResolver import ArgumentResolver
from injecta.autowiring.ArgumentsAutowirer import ArgumentsAutowirer
from injecta.service.resolved.ResolvedService import ResolvedService
from injecta.service.resolved.ServiceResolver import ServiceResolver
from injecta.service.ServiceParser import ServiceParser
from injecta.service.argument.ArgumentParser import ArgumentParser
from injecta.schema.SchemaValidator import SchemaValidator
from pyfonybundles.Bundle import Bundle
from pyfonybundles.BundleManager import BundleManager
from pyfony.PyfonyBundle import PyfonyBundle

class ContainerBuilder:

    def __init__(self):
        self.__classes2ServicesBuilder = Classes2ServicesBuilder()
        self.__servicesPreparer = ServicesPreparer(
            SchemaValidator(),
            ServiceParser(
                ArgumentParser(),
                DTypeResolver(),
            )
        )
        self.__servicesResolver = ServiceResolver()
        self.__autowirer = ArgumentsAutowirer(
            ArgumentResolver()
        )
        self.__parametersParser = ParametersParser()
        self.__tag2ServicesPreparer = Tag2ServicesPreparer()

    def build(self, appRawConfig: dict, bundles: List[Bundle], appEnv: str, configPath: str) -> ContainerBuild:
        if 'parameters' not in appRawConfig:
            appRawConfig['parameters'] = dict()
        if 'services' not in appRawConfig:
            appRawConfig['services'] = dict()

        bundleManager = BundleManager([PyfonyBundle()] + bundles)

        rawConfig = bundleManager.mergeRawConfig(appRawConfig)
        rawConfig = bundleManager.modifyRawConfig(rawConfig)

        services = self.__servicesPreparer.prepare(rawConfig['services'])
        services = bundleManager.modifyServices(services)

        classes2Services = self.__classes2ServicesBuilder.build(services)
        services2Classes = dict(map(lambda service: (service.name, service.class_), services))

        resolvedServices = list(map(lambda service: self.__servicesResolver.resolve(service, services2Classes), services)) # type: List[ResolvedService]

        tag2Services = self.__tag2ServicesPreparer.prepare(services)

        parameters = self.__parametersParser.parse(rawConfig['parameters'], {
            'project': {
                'configDir': os.path.dirname(configPath),
            },
            'kernel': {
                'environment': appEnv,
            },
        })

        parameters = bundleManager.modifyParameters(parameters)

        containerBuild = ContainerBuild(parameters, resolvedServices, classes2Services, tag2Services, appEnv)

        for compilerPass in bundleManager.getCompilerPasses(): # type: CompilerPassInterface
            compilerPass.process(containerBuild)

        return containerBuild
