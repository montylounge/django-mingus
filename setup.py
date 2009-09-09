from distutils.core import setup

setup(
    name='django-mingus',
    version='0.4.5',
    description='A django blog engine.',
    author='Kevin Fricovsky',
    author_email='kfricovsky@gmail.com',
    license='BSD',
    url='http://github.com/montylounge/django-mingus/tree',
    packages=[
        'mingus',
        'mingus.core',
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
)
