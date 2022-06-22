from setuptools import setup

setup(
    name='versioned-prov',
    version='1.0.0',
    description='Versioned-PROV website dependencies',
    url='https://github.com/dew-uff/versioned-prov',
    author=('Joao Felipe Pimentel, Paolo Missier, '
            'Leonardo Murta, Vanessa Braganholo'),
    author_email='joaofelipenp@gmail.com',
    license='MIT',
    install_requires = [
        'extensible_provn==0.2.1',
        'pandas==0.20.1',
        'numpy==1.22.0',
        'matplotlib==2.2.2',
        'pypandoc==1.4',
    ],
    zip_safe=False
)

