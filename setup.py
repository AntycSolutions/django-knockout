import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-knockout',
    version='0.6.3',
    packages=['knockout'],
    install_requires=['simplejson'],
    include_package_data=True,
    license='MIT License',
    description='Super easy ModelViews for knockout.js for your Django models',
    long_description=README,
    url='https://github.com/AntycSolutions/django-knockout',
    author='Rich Jones, Airith',
    author_email='rich@openwatch.net',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
