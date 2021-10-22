from tkinter import  *
import random
import sqlite3


def random_word():
    global wordlist_counter
    global counter
    global correct
    global wordlist
    global dictionary1
    global dictionary2

    try:
        l.set(wordlist[wordlist_counter])
        wordlist_counter +=1
    except:

        if len(dictionary2) > 0:
            popup=Tk()
            popup.title("score")
            Label(popup, text="Your score: "+str(correct)+" out of "+str(counter), font=('Trebuchet MS', 18)
                  ).pack(padx=25, pady=25)
            correct=0
            counter=0
            wordlist_counter = 0

            wordlist = []
            dictionary1 = dict(dictionary2)
            dictionary2 = {}
            wordlist=[]
            for i in dictionary1:
                wordlist.append(i)
            l.set(wordlist[wordlist_counter])
            wordlist_counter +=1
        else:
            popup = Tk()
            popup.title("score")
            Label(popup, text="Well done!", font=('Trebuchet MS', 18)
                  ).pack(padx=25, pady=25)
            l.set("Finished")
            cb["state"] = DISABLED

def check_word():
    global correct
    global counter
    global ent_box
    global dictionary1
    global dictionary2
    given_a=answer.get().lower()
    correct_a=dictionary1[l.get()]
    counter += 1
    if given_a == correct_a:
        correct+=1
        ent_box["fg"] = "green"
    else:
        ent_box["fg"] = "red"
        dictionary2[l.get()]=correct_a

    answer.set("")
    random_word()
    correct_ans.set(correct_a)

def enter_func(event):
    check_word()

conn = sqlite3.connect('dictionary.db')
c = conn.cursor()
c.execute("SELECT *, oid FROM addresses")
var1=c.fetchall()
#print(var1)
conn.commit()
conn.close()

dictionary1={}
dictionary2 = {}

for i in var1:
    dictionary1[i[0]]=i[1]

wordlist=[]
for i in dictionary1:
    wordlist.append(i)

random.shuffle(wordlist)
wordlist_counter=0

#print(wordlist)

counter=0
correct=0


mixer = Tk()
mixer.title('Word Mixer')

# make a function to do random selection from the word list
l=StringVar()
Label(mixer, textvariable=l, font=('Trebuchet MS', 18)).grid(column=0, row=0, padx=10, pady=(10, 5))

#random_word_button=Button(mixer, text="Show Random Word", command=lambda: random_word(), font=('Trebuchet MS', 15)
#                           ).grid(column=0, row=1, padx= 20, pady=(5, 10))
random_word()
answer=StringVar()
entryWidget = Entry(mixer, textvariable=answer, font=('Trebuchet MS', 18), justify='center')
entryWidget.grid(column=0, row=2, padx=10, pady=(0, 5))
entryWidget.bind("<Return>", enter_func)
entryWidget.focus()


cb = check_answer_button=Button(mixer, text="Check Answer", command=lambda: check_word(), font=('Trebuchet MS', 15))
cb.grid(column=0, row=3, padx= 20, pady=(5, 10))


Label(mixer, text='Correct Answer').grid(column=0, row=4, padx=10, pady=(10, 0))
correct_ans=StringVar()
ent_box = Entry(mixer, textvariable=correct_ans, state='readonly', font=('Trebuchet MS', 18, 'bold'), justify='center')
ent_box.grid(column=0, row=5, padx=10, pady=(0, 10))


mixer.mainloop()