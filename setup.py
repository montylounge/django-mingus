import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-mingus',
    version='0.8.5',
    description='A django blog engine.',
    long_description=read('README.textile'),
    author='Kevin Fricovsky',
    author_email='kfricovsky@gmail.com',
    license='BSD',
    url='http://github.com/montylounge/django-mingus/tree',
    packages=[
        'mingus',
        'mingus.core',
        'mingus.templatetags'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    package_data = {
            'mingus': [
                'media/mingus/css/*.css',
                'media/mingus/img/*.png',
                'media/mingus/js/*.js',
            ]
        },
    zip_safe=False, # required to convince setuptools/easy_install to unzip the package data
)
