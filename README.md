Welcome to the AO Workflow Developer, an application for designing and developing workflows & testscripts for large-scale applications.

This is written in Python, leveraging the Kivy, SQLAlchemy, and OpenPyXl libraries.

The Workflow Developer is designed to integrate heavily with other applications within a testing suite, a listed of tested integrations are listed below.

#Installation:

##Downloadable

At this time, there is now downloadable executable for the Workflow Developer, this will be updated soon.

##Install From Source

You will need a git client to download the source code (tortoisegit/git-bash/etc)

From a terminal, the below will clone down the repository into a fresh folder on your system (from that folder)

```
git clone *Paste the URL shown in the main page here*
```

###Windows Dependency Installs

####Install Kivy
1.	Install the Kivy Portable Package for Python 2.7, following the [install instructions](http://kivy.org/docs/installation/installation-windows.html)

####Install SQLAlchemy

1.	Find the Python Distribution shipped with your Kivy package (it’s located inside the Kivy folder, wherever you unzipped it to).  Copy the path to the python executable.

2.	Open the command prompt & run the following command:

```
""Path_to_Python_Executable"\python.exe -m pip install sqlalchemy
```

a.	For instance, my system compiled successfully with:

```
C:\Users\ABarry.US\Documents\Development\Python\Kivy-1.9.0-py2.7-win32-x86\python27\python.exe -m pip install sqlalchemy
```

####Install OpenPyXL

4.	Get the Python Distribution shipped with your Kivy package again and copy the path to the python executable

5.	Run the following command:

```
""Path_to_Python_Executable"\python.exe -m pip install openpyxl
```

###Start the Application

6.	Follow [the instructions](http://kivy.org/docs/installation/installation-windows.html#start-a-kivy-application) to start the 'WorkflowDeveloper.py' file


###Linux Dependency Installation

####Install Python

1.	Install Python (may not be necessary depending on distribution & version.  For instance, Python is included with Ubuntu 14.04 and later)

####Install Kivy

2.	Install Kivy using your package manager per the instructions here: http://kivy.org/docs/installation/installation-linux.html

####Install SQLAlchemy

3.	Install SQLAlchemy using PIP: sudo pip install sqlalchemy

####Install OpenPyXL

4.	Install OpenPyXL using PIP: sudo pip install openpyxl

###Start the Application

4.	Start the application using: sudo python WorkflowDeveloper.py

#Use

You can find documentation on using the Workflow Developer in the 'Documentation' folder

#Other Suggested Tools

1.	Microsoft Excel (Proprietary, Windows)

You can get Excel [here](https://products.office.com/en-us/excel)

Excel is used for the Key Action Data Loader as well as for exports

2.	SQLite DB Browser (Open Source, Windows)

You can get the DB Browser [here](http://sqlitebrowser.org/)

The DB Browser can be used to directly interact with the database underneath the application.

3.	sqlite3 (Open Source, Linux)

You can install sqlite3 on Ubuntu 14.04 with the following:

```
sudo apt-get install sqlite3
```
Sqlite3 can be used to directly interact with the database underneath the application.

4.	CSV-Based Scripts

CSV Files are also accepted for Key Action Dataloaders, meant to encourage scripting to generate these lists.
