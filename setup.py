from setuptools import setup, find_packages

setup(
    name='dependencies',
    version='1.0',
    packages=find_packages(),
    install_requires=[],
    author='Renan Oliveira',
    author_email='renanmgx@hotmail.com',
    description='Layout de dependências para projetos Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/RenanMGX/dependencies_patrimar.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
