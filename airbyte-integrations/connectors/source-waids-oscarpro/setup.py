#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

from setuptools import find_packages, setup

## These requirements are from QHR, we might have something similar
MAIN_REQUIREMENTS = [
    "airbyte-cdk",
    "beautifulsoup4",

#     "airbyte-cdk~=0.2",
#     "azure-keyvault-secrets",
#     "azure-identity",
#     "pysftp",
#     "docker",
#     "pyodbc",
#     "kubernetes"
]

TEST_REQUIREMENTS = [
    "airbyte-cdk",
    "pytest",

#     "requests-mock~=1.9.3",
#     "pytest-mock~=3.6.1",
#     "pytest~=6.2",
#     "connector-acceptance-test",
]

setup(
    entry_points={
        "console_scripts": [
            "source-waids-oscarpro=source_waids_oscarpro.run:run",
        ],
    },
    name="source_waids_oscarpro",
    description="Source implementation for Waids Oscar Pro.",
    author="Airbyte",
    author_email="contact@airbyte.io",
    packages=find_packages(),
    install_requires=MAIN_REQUIREMENTS,    
    extras_require={
        "tests": TEST_REQUIREMENTS,
    },
    package_data={
        "": [
            # Include yaml files in the package (if any)
            "*.yml",
            "*.yaml",
            # Include all json files in the package, up to 4 levels deep
            "*.json",
            "*/*.json",
            "*/*/*.json",
            "*/*/*/*.json",
            "*/*/*/*/*.json",
        ]
    },
)
