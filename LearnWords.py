from tkinter import *
from tkinter import filedialog
import sqlite3
# import pickle
import os
from googletrans import Translator


root = Tk()
root.title('Learn Words with Flashcards')


def renew_db():
    conn = sqlite3.connect('dictionary.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE  addresses (
                swedish_word text,
                english_translation text )""")

    conn.commit()
    conn.close()


def save_records():
    conn = sqlite3.connect('dictionary.db')
    c = conn.cursor()

    c.execute("SELECT *,oid FROM addresses")
    var2 = c.fetchall()
    #    print(var2)
    backup_dict = {}
    for i in var2:
        backup_dict[i[0]] = [i[1], i[2]]
    #    print(backup_dict)
#    filename = filedialog.asksaveasfilename(title="Select a File or write a filename",
#                                          filetypes=(("saved data files",
#                                                      "*.dat*"),
#                                                     ("all files",
#                                                      "*.*")))
#    infile = open(f"{filename}.dat", 'wb')
#    pickle.dump(backup_dict, infile)
#    infile.close()
    write_csv(var2)
    swe.set("Total words saved:" + str(len(var2)))

def write_csv(list):
    filename = filedialog.asksaveasfilename(title="Select a file or write a filename",
                                          filetypes=(("CSV files",
                                                      "*.csv*"),
                                                     ("all files",
                                                      "*.*")))
    print(len(filename))
    if filename[-4:] == ".csv":
        filename = filename[:-4]
        print(filename)
    outfile = open(f"{filename}.csv", 'w')
    num = 0
    for i in list:
        outfile.write(list[num][0] + ';' + list[num][1] + ';' + str(list[num][2])  + "\n")
        num+=1


def retrieve_records():
    try:
        renew_db()
    except:
        pass

    backup_dict = load_csv()
#     filename = filedialog.askopenfilename(title="Select a File",
#                                           filetypes=(("saved data files",
#                                                       "*.dat*"),
#                                                      ("all files",
#                                                       "*.*")))
#     infile = open(f"{filename}", 'rb')
#     backup_dict = pickle.load(infile)
#     infile.close()
#    print(backup_dict)

    # existing data
    conn = sqlite3.connect('dictionary.db')
    c = conn.cursor()
    c.execute("SELECT *,oid FROM addresses")
    var2 = c.fetchall()
    current_dict = {}
    for i in var2:
        current_dict[i[0]] = [i[1], i[2]]
    conn.commit()
    conn.close()
#    print(current_dict)
    print("\n"+"Initial total words:", len(current_dict))

    # create an update dictionary
    update_dict = {}
    for i in backup_dict:
        if i not in current_dict:
            update_dict[i] = backup_dict[i]

    for i in update_dict:
        conn = sqlite3.connect('dictionary.db')
        # Create cursor
        c = conn.cursor()
        c.execute("INSERT INTO addresses VALUES(:swedish_word, :english_translation)",
                  {'swedish_word': i,
                   'english_translation': update_dict[i][0]})
        conn.commit()
        conn.close()
#    print(current_dict)
    print("Retrieved words:", len(backup_dict))
    print("Unique words added:", len(update_dict))
    print("Current total words:", len(current_dict) + len(update_dict))
    swe.set("Unique words added:" + str(len(update_dict)))

def load_csv():
    filename = filedialog.askopenfilename(title="Select a File",
                                          filetypes=(("CSV files",
                                                      "*.csv*"),
                                                     ("all files",
                                                      "*.*")))
    infile = open(f"{filename}", 'r')
    listOfRecords = [line.rstrip() for line in infile]
    infile.close()
    dictionary={}
    for i in range(len(listOfRecords)):
        listOfRecords[i] = listOfRecords[i].split(';')
        dictionary[listOfRecords[i][0]] = (listOfRecords[i][1], listOfRecords[i][2])
    return dictionary

def querry_records():
    conn = sqlite3.connect('dictionary.db')
    c = conn.cursor()

    c.execute("SELECT *, oid FROM addresses")
    var1 = c.fetchall()
    print(var1)

    conn.commit()
    conn.close()


# Submit function
def enter_func(event):
    submit()


def submit():
    try:
        import sqlite3

        conn = sqlite3.connect('dictionary.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE  addresses (
                    swedish_word text,
                    english_translation text )""")

        conn.commit()
        conn.close()
    except:
        pass
    if swe.get() != "":
        # Create a database
        conn = sqlite3.connect('dictionary.db')
        # Create cursor
        c = conn.cursor()

        c.execute("INSERT INTO addresses VALUES(:swedish_word, :english_translation)",
                  {'swedish_word': swe.get().lower(),
                   'english_translation': eng.get().lower()})
        conn.commit()
        conn.close()

        # Clear entryboxes
        swe.set("")
        eng.set("")
        swedish_word.focus()


def delete_record():
    conn = sqlite3.connect('dictionary.db')
    c = conn.cursor()

    c.execute("SELECT *,oid FROM addresses")
    var2 = c.fetchall()
    backup_dict = {}
    for i in var2:
        backup_dict[i[0]] = [i[1], i[2]]
    conn.commit()
    conn.close()
    id = ""
    for i in backup_dict:
        if i == swe.get().lower():
            id = str(backup_dict[i][1])
    try:
        conn = sqlite3.connect('dictionary.db')
        c = conn.cursor()
        c.execute("DELETE from addresses WHERE oid=" + id)
        conn.commit()
        conn.close()
        print(swe.get(), "DELETED")

    except sqlite3.OperationalError as e:
        print("The word does not exist.")


def run_app():
    try:
        conn = sqlite3.connect('dictionary.db')
        c = conn.cursor()
        c.execute("SELECT *,oid FROM addresses")
        var2 = c.fetchall()
        current_dict = {}
        for i in var2:
            current_dict[i[0]] = [i[1], i[2]]
        conn.commit()
        conn.close()
    except:
        return
    if len(current_dict) >= 0:
      root.destroy()
      os.system("Word_Mixer.py")


def delete_db():
    os.remove("dictionary.db")

def ask_google():
    translator = Translator()
    word = swe.get()
    out = translator.translate(f"{word}", dest="en")

    eng.set(out.text)

swe = StringVar()
swedish_word = Entry(root, width=30, textvariable=swe, font=('Trebuchet MS', 18))
swedish_word.grid(column=1, row=1, padx=(0, 15), pady=5)
Label(root, text="Word: ", font=('Trebuchet MS', 18)).grid(column=0, row=1, padx=5, pady=(15, 5), sticky=E)
swedish_word.focus()

eng = StringVar()
translation = Entry(root, width=30, textvariable=eng, font=('Trebuchet MS', 18))
translation.grid(column=1, row=2, padx=(0, 15), pady=5)
translation.bind("<Return>", enter_func)


Label(root, text="Translation: ", font=('Trebuchet MS', 18)).grid(column=0, row=2, padx=(15, 5), pady=5)

google_btn1 = Button(root, text="Ask Google", command=ask_google, font=('Trebuchet MS', 15), width=12)
google_btn1.grid(row=4, column=0, columnspan=3, padx=10, pady=10, ipadx=5, sticky=W)

submit_btn1 = Button(root, text="Add Flashcard", command=submit, font=('Trebuchet MS', 18), width=12
                     ).grid(row=4, column=0, columnspan=3, padx=10, pady=10, ipadx=5)

delete_btn = Button(root, text="Delete Record", command=delete_record, font=('Trebuchet MS', 15), width=12
                    ).grid(row=4, column=0, columnspan=3, padx=10, pady=10, ipadx=5, sticky=E)

show_records_button = Button(root, text="Save Records to CSV", command=save_records, font=('Trebuchet MS', 12)
                             ).grid(row=6, column=0, columnspan=3, padx=10, pady=(20, 5), ipadx=5)

retrieve_records_button = Button(root, text="Load records from CSV", command=retrieve_records,
                                 font=('Trebuchet MS', 12)
                                 ).grid(row=7, column=0, columnspan=3, padx=10, pady=5, ipadx=5)

run_the_app = Button(root, text="Run", command=run_app, font=('Trebuchet MS', 13)
                     ).grid(row=7, column=0, columnspan=3, rowspan=2, padx=10, pady=(20, 5), ipadx=5, sticky=E+S)
deleteRecords = Button(root, text="Clean Database", command=delete_db, font=('Trebuchet MS', 10)
                     ).grid(row=7, column=0, columnspan=3, rowspan=2, padx=10, pady=(20, 5), ipadx=5, sticky=W+S)
Label(root, text="Cepni", font=('Trebuchet MS', 6)).grid(column=0, columnspan=3, row=8, padx=(15, 5), pady=5)


var4 = swe.get().lower()

root.mainloop()


