'''
The setup.py file is a core component of Python 
projects that defines the project's configuration and metadata for packaging and distribution. It is primarily used for 
packaging Python libraries and modules for easy installation, as well as specifying dependencies and other important settings.
'''
from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    """"
    This function will return List of requirements
    """
    requirement_lst:List[str] = []
    try:
        with open('requirements','r') as files:
            #read the lines from the file
            lines=files.readlines()
            #process each line
            for line in lines:
                requirement=line.strip()
                #ignore -e (which calls the setup tools)
                if requirement and requirement != '-e':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print('requirements.txt file not found')
    
    return requirement_lst

setup(
    name='Big_mart_sales',
    version='0.0.1',
    author='Nikhil Botta',
    author_email='nikhilbotta26@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)


