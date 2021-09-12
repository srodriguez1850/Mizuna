from setuptools import setup, find_packages

v = {}
version = exec(open('mizuna/version.py').read(), v)
description = 'Mizuna is a package that automates uploading visualizations to Overleaf projects (or git repositories).'
long_description = open('README.md').read()

setup(
    name='mizuna',
    version=v['__version__'],
    author='Sebastian Rodriguez',
    author_email='s.rodriguez1850@outlook.com',
    url='https://github.com/srodriguez1850/Mizuna',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT License',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    # install_requires=[],
    keywords=['python', 'workflow', 'data-science',
              'latex', 'overleaf',
              'jupyter',
              'matplotlib', 'seaborn', 'ggplot', 'plotly'],

    project_urls={
        'Bug Reports': 'https://github.com/srodriguez1850/Mizuna/issues',
        'Source': 'https://github.com/srodriguez1850/Mizuna/issues'
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities'
    ]
)
