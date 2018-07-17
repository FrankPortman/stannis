import setuptools

setuptools.setup(
    name="stannis",
    version="0.1.0",
    url="https://github.com/FrankPortman/stannis",

    author="Frank Portman",
    author_email="frank1214@gmail.com",

    description="Python AI Framework + DSL for (multi)player games",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
