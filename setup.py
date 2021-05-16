from setuptools import setup, find_packages

setup(name='kiero_data_models',
    version='0.0.1',
    description='data models',
    author='jdiazvera',
    url='https://github.com/jdiazvera/models_example',
    packages=['kiero_models'],
    install_requires=[
        'sqlalchemy',
        'flask_sqlalchemy'
    ]
)