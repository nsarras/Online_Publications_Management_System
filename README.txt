READ before running online publication management system.

Please follow the steps below when running the project

1. Run the create.py script to create and populate the database.db with the following command:

	python create.py pubs.txt

Note: The script will attempt to install any needed packages to run the project

2. Launch Jupyter Notebook and run the notebook.ipynb file
This will run all of the test queries on the database, make sure to execute everything in order

3. Run the web service with 
python service.py

Further instructions for the web service are provided in a seperate readme file under that directory. 