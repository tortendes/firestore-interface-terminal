import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import inquirer

from methods.add import add

## Insert your firebase credentials path here
cred = credentials.Certificate("accountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def process():       
        questions = [
                    inquirer.List('select', message="Welcome to Kirby. Select a proccess", 
                        choices=[("Add new Entry", 0), ("Edit an entry", 1), ("Delete an entry", 2), ("Exit", 3)]
                        )
                ]

        answers = inquirer.prompt(questions)

        print(answers)

        if answers['select'] == 0:
            add(db, process)
        elif answers["select"] == 3:
                exit(1)
        else:
            print('Function not currently supported, select another option.')
            process()
process()
db.close()
