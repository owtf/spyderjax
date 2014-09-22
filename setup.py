from setuptools import setup

setup(
    name='spyderjax',
    version='0.2',
    description='AJAX crawler for pentesting',
    url='https://github.com/owtf/spyderjax',
    author='Viyat Bhalodia',
    author_email='viyat001@gmail.com',
    license='Custom',
    packages=['spyderjax'],
    zip_safe=False,
    install_requires=open('requirements.txt').readlines(),
    long_description=open('README.md').read(),
    scripts=['bin/spyderjax'],
)
