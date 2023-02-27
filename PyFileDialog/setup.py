from setuptools import Extension, setup, find_packages

setup(
    name='pyfiledialog',
    version='1.0.0',
    description='A Python package for selecting files and folders using Windows file dialogs',
    author='Kevin Robben',
    author_email='your.email@example.com',
    url='https://github.com/your-username/pyfiledialog',
    package_data={"pyfiledialog": ["PyFileDialog.dll"]},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.6',
)
