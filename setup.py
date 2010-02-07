import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-mingus',
    version='0.9.7',
    description='A django blog engine.',
    long_description=read('README.textile'),
    author='Kevin Fricovsky',
    author_email='kfricovsky@gmail.com',
    license='BSD',
    url='http://github.com/montylounge/django-mingus/',
    keywords = ['blog', 'django',],
    packages=[
        'mingus',
        'mingus.core',
        'mingus.core.templatetags',
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
    zip_safe=False,
)
