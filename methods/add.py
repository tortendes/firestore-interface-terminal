import inquirer
from halo import Halo
from lib.defs import ratings, chapterLength, tags

manhwa = {}
manhwa['data'] = {}
manhwa['sources'] = []
manhwa['notes'] = []

def titleCheck(db):
    answers = inquirer.prompt([     
            inquirer.Text('title', message="Please enter Title"),
        ])

    spinner = Halo(text="Checking title", spinner="dots")
    spinner.start()

    user_doc_ref = db.collection('titles').where('title', '==', answers["title"]).stream()
    documents = [d for d in user_doc_ref]

    if len(documents):
        for document in documents:
            spinner.fail('Title already taken, choose another title.')
            titleCheck(db)
    else:
        manhwa["title"] = answers["title"]
        spinner.stop()
        spinner.clear()
def initialQuestions():
    questions = [
        inquirer.Editor('description', message="Please add Description"),
        inquirer.Editor('image', message="Please add the Image Link for the title, the bigger, the better."),
        inquirer.Checkbox(
            "tags",
            message="Please add the coressponding tags that fit this title.",
            choices=tags
            ),
        inquirer.List(
            "chaplen",
            message="How many chapter there is in this Title?",
            choices=chapterLength
            ),
        inquirer.List(
            "rating",
            message="What's the rating for this title",
            choices=ratings
            ),
        inquirer.Confirm('finished', message="Is this title Completed?")
    ]
    answers = inquirer.prompt(questions)

    manhwa["description"] = answers["description"]
    manhwa["imageLink"] = answers["image"]
    manhwa["data"]["chapCount"] = answers["chaplen"]
    manhwa["data"]["rating"] = answers["rating"]
    manhwa["data"]["completed"] = answers["finished"]
    manhwa["data"]["tags"] = answers["tags"]
    print(answers)

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

def add(db, home):
    titleCheck(db)
    initialQuestions()
    sourcesQuestion()
    notesQuestion()

    spinner = Halo(text="Inserting Data To Database", spinner="dots")
    spinner.start()

    db.collection('titles').add(manhwa)

    spinner.succeed('Added a title to the database successfully.')
    home()
