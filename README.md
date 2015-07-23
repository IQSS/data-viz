# Dataverse Visualizations

This is a tool for visualizing data from the Dataverse project. It is indended to augment the current analysis tool, TwoRavens, to give it visualisation capability. 

##Setup 
1. Download from Github

1. Software Prerequisites:
  * Python 2.7
  * Python package index (pip). can be downloaded [here] (https://pip.pypa.io/en/latest/installing.html)
  * R
 

2. (Recommended)
  * Before dowloading the neccessary packages for this application, it is recommended to set up a python virtualenv with a virtualenvwrapper. Please see the [virtualenv documentation] and then the [virtualenvwrapper documentation.](http://virtualenvwrapper.readthedocs.org/en/latest/install.html) Note: if you are running windows, download [virtualenvwrapper-win-1.1.5] (https://pypi.python.org/pypi/virtualenvwrapper-win) or [cygwin] (https://www.cygwin.com/) instead of virutalenvwrapper.
 
3. Package Download
 * In your terminal, change directories to the path of the application (data-viz). Then enter the 'DataVisualiations' directory. if you decided to set up an virtualenvwrapper, activate it with the command: ```$ workon your_environment_name```. Then, change directories to the project directory ```data-viz```, then enter the ```DataVisualizations``` folder. To download the contents of the "requirements.txt" file, type the following command into the terminal: ```$ pip install -r /path/to/requirements.txt```
 
4. Starting the App
 * To begin visualizing, make sure you are in the ```DataVisualizations``` directory and run the following command: ```python viz_tool.py```. You will see the following line: ``` * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)```. Go to the listed URL in a browser (preferrabley Chrome), and you will be ready to visualise. 
 
## User Guide
* To see how to use this tool to visualize your data, please see [this 4 minute domo](https://youtu.be/OzrECzPf95g).
 
