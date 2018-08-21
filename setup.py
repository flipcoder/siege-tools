from setuptools import setup, find_packages
setup(
    name='siegetools',
    description='',
    url='https://github.com/filpcoder/siege-tools',
    author='Grady O\'Connell',
    author_email='flipcoder@gmail.com',
    license='MIT',
    packages=find_packages('.'),
    scripts=['sgmake','sgmake.py','sgrun','sgrun.py'],
    install_requires=["psutil"],
    zip_safe=False
)

