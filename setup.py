from setuptools import setup, find_packages
import os

setup(
	name= 'DataChartWireframe',
	version= '0.1',
	description= 'Data Visualiztions for TwoRavens (Harvard IQSS) data.',
	author='Tamir Bennatan',
	author_email= 'timibennatan@gmail.com',
	url='https://github.com/IQSS/data-viz/tree/master/DataChartWireframe',
	#packages = find_packages(exclude=['data_preview*', 'requirements*']),
	packages= ['DataChartWireframe'],
	license= 'MIT',
	install_requires = ['betterpath==0.2.2',
	'Flask==0.10.1',
	'itsdangerous==0.24',
	'Jinja2==2.7.3',
	'l==0.3.1',
	'MarkupSafe==0.23',
	'pandas==0.16.2',
	'python-dateutil==2.4.2',
	'pytz==2015.4',
	'requests==2.7.0',
	'rpy2==2.6.1',
	'singledispatch==3.4.0.3',
	'six==1.9.0',
	'vcversioner==2.14.0.0',
	'Werkzeug==0.10.4',
	'wheel==0.24.0',
	'zope.interface==4.1.2'],
	install_package_data=True,
	package_data = {'static':'DataChartWireframe/static/*','templates':'DataChartWirefame/templates/*'}
	
	)