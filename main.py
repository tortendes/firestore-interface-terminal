import inquirer
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from halo import Halo

cred = credentials.Certificate("accountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

manhwa = {}
manhwa['data'] = {}
manhwa['sources'] = []
manhwa['notes'] = []

def initialQuestions():
    questions = [
        inquirer.Text('title', message="Please enter Title"),
        inquirer.Editor('description', message="Please add Description"),
        inquirer.Editor('image', message="Please add the Image Link for the title, the bigger, the better."),
        inquirer.List(
            "chaplen",
            message="How many chapter there is in this Title?",
            choices=[('Under 100 Chapters (UH)', 0), ('Over 100 Chapters (OH)', 1)]
            ),
        inquirer.List(
            "rating",
            message="What's the rating for this title",
            choices=[("Highly Recommended (HR)", 4), ("Recommended (R)", 3), ("Good (G)", 2), ("Decent (D)", 1), ("Meh (M)", 0)]
            ),
        inquirer.Confirm('finished', message="Is this title Completed?")
    ]
    answers = inquirer.prompt(questions)

    manhwa["title"] = answers["title"]
    manhwa["description"] = answers["description"]
    manhwa["imageLink"] = answers["image"]
    manhwa["data"]["chapCount"] = answers["chaplen"]
    manhwa["data"]["rating"] = answers["rating"]
    manhwa["data"]["completed"] = answers["finished"]

def sourcesQuestion():
    questions = [
        inquirer.Text('sitename', message="Enter the site name you're adding"),
        inquirer.Editor('sitelink', message="Please enter the link for this link."),
        inquirer.List('from', message="What is this site?", choices=[("Agressor", 0), ("Scan Group", 1), ("Official", 3)])
    ]
    sourceanswer = inquirer.prompt(questions)
    manhwa['sources'].append(sourceanswer)

    question2 = [
            inquirer.Confirm('again', message="Do you want to add another source?")
        ]
    ans = inquirer.prompt(question2)
    if ans["again"] == True:
        sourcesQuestion()
    else:
        return

def notesQuestion():
    preliminary = [
            inquirer.Confirm('notes', message="Do you want to add notes?")
        ]
    addnote = inquirer.prompt(preliminary)
    if addnote['notes'] == False:
        return

    questions = [
            inquirer.Editor('note', message="What is the note would you want to add?")
        ]
    noteans = inquirer.prompt(questions)
    manhwa['notes'].append(noteans['note'])

    question2 = [
            inquirer.Confirm('again', message="Do you want to add another note?")
        ]
    ans = inquirer.prompt(question2)
    if ans["again"] == True:
        notesQuestion()
    else:
        return


initialQuestions()
sourcesQuestion()
notesQuestion()

spinner = Halo(text="Inserting Data To Database", spinner="dots")
spinner.start()

db.collection('titles').add(manhwa)

spinner.succeed('Added db sucessfully')

print(manhwa)

