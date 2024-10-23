from setuptools import setup

setup(
    name='portl',
    version='1',
    description='SpeedGuide.net port lookup utility',
    author='James Conlan',
    url='https://github.com/JamesConlan96/portl',
    py_modules=[
        'portl'
    ],
    install_requires=[
        'argparse',
        'beautifulsoup4',
        'requests',
        'tabulate',
        'lxml'
    ],
    python_requires='>=3.0.0',
    entry_points={
        'console_scripts': [
            'portl = portl:main'
        ]
    }
)
