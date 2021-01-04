# Extending Pyfony with bundles

Pyfony can be easily extended using first or third party bundles. Bundle is a standard python package with some extra configuration.

The default Pyfony setup is shipped with the following bundles:

* [console-bundle](https://github.com/pyfony/console-bundle) - empowering Pyfony with pluggable CLI commands
* [logger-bundle](https://github.com/pyfony/logger-bundle) - base logging bundle, enables stdout logging and introduces API for custom log handlers

To add a new bundle, use `poetry add package-name`. For example you can add the [azure-logger-bundle](https://github.com/pyfony/azure-logger-bundle) to send your logging data to Azure Log Analytics by running the `poetry add azure-logger-bundle` command.
