# # Command to run script:
# python create.py pubs.txt
# Nadim Sarras


import sys, os
import db_manager

# Parses input data file and generates database.db file. Then proceeds to populate the
# database from the data of the input file. The database creation, insert statements, and parsing
# definitions can be found in the db_manager.py file

def main():
    if len(sys.argv) != 2:
        raise IOError("Invalid Argument" + "Unexpected error:", sys.exc_info())
    else:
        # Ensures environment contains necessary packages, if not will run pip install command
        shell_path_root = (os.path.dirname(os.path.realpath(__file__)))
        req_file_path = shell_path_root + os.sep + 'req.txt'
        if os.path.isfile(req_file_path):
            os.system('pip install -r ' + req_file_path)
            inputDir = os.path.abspath(os.path.expanduser(sys.argv[1]))
            try:
                #Creates database
                db_manager.create_database()
                #Populates database
                db_manager.parser(inputDir)
            except RuntimeError as e:
                print e
            except Exception:
                raise sys.exc_info()

        else:
            raise OSError('Req file not found...pkg corrupted')


if __name__ == "__main__": main()
