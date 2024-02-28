### Test Case Management

## Setting up the Project

Follow these steps to set up the project:

1. Create a virtual environment named "myEnv" with Python 3:

   ```shell
   virtualenv myEnv -p python3

2. Activate the virtual environment:

   ```shell
   source myEnv/bin/activate


3. Install Flask using pip:
   ```shell
   pip install flask


## Create Database

The database is composed of three tables one of the test assets, testcases, and test results. You can create the db by running db.py

   ```shell
   python db.py

  # to run the app
  python app.py

 # to run unnittests
 python test.py
