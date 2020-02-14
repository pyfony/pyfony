from injecta.autowiring.ArgumentResolver import ArgumentResolver
from injecta.autowiring.ArgumentsAutowirer import ArgumentsAutowirer
from injecta.autowiring.AutowiringCompilerPass import AutowiringCompilerPass
from pyfonybundles.Bundle import Bundle
from injecta.service.DefaultValuesSetter import DefaultValuesSetter
from injecta.service.DefaultValuesSetterCompilerPass import DefaultValuesSetterCompilerPass
from injecta.tag.TaggedServicesCompilerPass import TaggedServicesCompilerPass

class PyfonyBundle(Bundle):

    def getConfigFiles(self):
        return []

    def getCompilerPasses(self):
        return [
            DefaultValuesSetterCompilerPass(DefaultValuesSetter()),
            TaggedServicesCompilerPass(),
            AutowiringCompilerPass(ArgumentsAutowirer(ArgumentResolver())),
        ]
