#!/usr/bin/env python

import sys
import time
import re

# =================================================================    GLOBALS    ==========================================================================

notes_in_order = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
string_values = {
    "standard": ['E', 'A', 'D', 'G', 'B', 'e'],
    "drop d": ['D', 'A', 'D', 'G', 'B', 'e'],
    "drop c#": ['C#', 'G#', 'C#', 'F#', 'A#', 'd#'],
    "open d": ['D', 'A', 'D', 'F#', 'A', 'd'],
    "open g": ['D', 'G', 'D', 'G', 'B', 'd'],
    "open c": ['C', 'G', 'C', 'G', 'C', 'e'],
    "dadgad": ['D', 'A', 'D', 'G', 'A', 'd'],
    "open d minor": ['D', 'A', 'D', 'F', 'A', 'd'],
    "double drop d": ['D', 'A', 'D', 'G', 'B', 'd'],
    "open e": ['E', 'B', 'E', 'G#', 'B', 'e'],
    "open a": ['E', 'A', 'C#', 'E', 'A', 'e'],
    "open e minor": ['E', 'B', 'E', 'G', 'B', 'e'],
    "open c# minor": ['C#', 'G#', 'C#', 'F#', 'G#', 'c#'],
    "new standard": ['C', 'F', 'A#', 'D#', 'G', 'c'],
    "half step down": ['D#', 'G#', 'C#', 'F#', 'A#', 'd#']
}
chords = {
    'a major': ['A', 'C#', 'E'],
    'a minor': ['A', 'C', 'E'],
    'a# major': ['A#', 'D', 'F'],
    'a# minor': ['A#', 'C#', 'F'],
    'b major': ['B', 'D#', 'F#'],
    'b minor': ['B', 'D', 'F#'],
    'c major': ['C', 'E', 'G'],
    'c minor': ['C', 'D#', 'G'],
    'c# major': ['C#', 'F', 'G#'],
    'c# minor': ['C#', 'E', 'G#'],
    'd major': ['D', 'F#', 'A'],
    'd minor': ['D', 'F', 'A'],
    'd# major': ['D#', 'G', 'A#'],
    'd# minor': ['D#', 'F#', 'A#'],
    'e major': ['E', 'G#', 'B'],
    'e minor': ['E', 'G', 'B'],
    'f major': ['F', 'A', 'C'],
    'f minor': ['F', 'G#', 'C'],
    'f# major': ['F#', 'A#', 'C#'],
    'f# minor': ['F#', 'A', 'C#'],
    'g major': ['G', 'B', 'D'],
    'g minor': ['G', 'A#', 'D'],
    'g# major': ['G#', 'C', 'D#'],
    'g# minor': ['G#', 'B', 'D#']
}

# =================================================================    CLASSES    ==========================================================================
# chords are lowercase, notes are uppercase

class guitar:
    def __init__(self, tuning, strings, num_frets):
        self.tuning = tuning
        self.strings = strings
        self.frets = num_frets
    def __str__(self):
        return f'GUITAR ++++> tuning={self.tuning}, strings={self.strings}, frets={self.frets}\n'

class chord:
    def __init__(self, n, t):
        self.note = n
        self.type = t.lower()
        self.name = n.lower() + " " + t.lower()
    def __str__(self):
        return f'CHORD ++++> note={self.note}, type={self.type}, name={self.name}\n'

# =================================================================    MAFS    ==========================================================================

def get_note_at_fret(note, fret):
    return notes_in_order[((notes_in_order.index(note.upper()) - (fret - 1)) + fret) % len(notes_in_order)]

def build_guitar_table(g, c):
    table = [[0] * (g.frets) for _ in range(g.strings)]
    
    for i in range(g.strings):
        for j in range(g.frets):
            if j == 0:
                note = str(string_values.get(g.tuning)[i]).upper()
            else:
                note = get_note_at_fret(note, j)

            for var in chords.get(c.name):
                if var.upper() == note.upper():
                    # table[i][j] = 'o'
                    table[i][j] = note
                    break
                else:
                    table[i][j] = '-'
                
    return table

# =================================================================    PRINTING    ==========================================================================

def print_guitar(t):
    for i in range (len(t[0]) + 1):
        if i == 0:
            print("{: <5}".format(""), end="")
        else:
            print("{: <5}".format(i - 1), end="")
    print()
    for i in range (len(t)):
        print ("{: <5}".format(string_values.get(g.tuning)[i]), end="")
        for j in (range(len(t[i]))):
            print ("{: <5}".format(t[i][j]), end="")
        print()
    print()

def slow_print(string, delay=0.01):
    for char in string:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def print_table_opener(labels):
    print ("\n\n")
    tmp = "\t|{: ^78}|"
    print("\t{:->{}}".format("", 80))
    print("\t|{: ^30}".format(""), "+{:-^14}+".format(""), "{: ^30}|".format(""))
    for i in range (3):
        if i == 1:
            if labels == "available tunings":
                print ("\t|{: ^30}".format(""), "|{:^14}|".format("avail. tunings"), "{: ^30}|".format(""))
            else:
                print ("\t|{: ^30}".format(""), "|{:^14}|".format(labels), "{: ^30}|".format(""))
        else:
            print ("\t|{: ^30}".format(""), "|{:^14}|".format(""), "{: ^30}|".format(""))
    print ("\t|{: ^30}".format(""), "+{:-^14}+".format(""), "{: ^30}|".format(""))
    for i in range (3):
        print (tmp.format(""))

# =================================================================    SCRIPTING    ==========================================================================

def get_music_information():
    slow_print("Would you would like to use a 6 string guitar with 22 frets?")
    base = input_checking(input("y/n: "), "y/n")
    if base.lower() == "n":
        slow_print("Select the number of strings and number of frets on your guitar.")
        strs = int(input_checking(input("Strings: "), "Strings"))
        if (strs == None):
            strs = 6
        frets = int(input_checking(input("Fret Count: "), "Fret Count"))
        if frets == None:
            frets = 22
    else:
        strs = 6
        frets = 22
    slow_print("Next, select your tuning, if standard you may hit enter instead:")
    outer_bo = False
    while not outer_bo:
        tune = input("Tuning: ")
        if not tune.strip():
            tune = "standard"
        if tune.lower() == "custom":
            tmp_bo = False
            while not tmp_bo:
                tuning_name = input("Enter a name for your custom tuning:\n")
                tuning_input = input("Enter your custom tuning, separated by commas. Example: e, a, d, g, d#...\n").lower()
                tuning_list = tuning_input.split(",")
                if len(tuning_list) != strs:
                    print(f"Error: Your custom tuning must include {strs} strings.")
                    continue
                tuning_list = [string.strip().upper() for string in tuning_list]
                invalid_note = False
                for note in tuning_list:
                    if note not in notes_in_order:
                        print(f"Error: {note} is not a valid note. Please try again")
                        invalid_note = True
                        continue
                if invalid_note:
                    continue
                tmp_bo = True
            string_values.update({tuning_name : tuning_list})
            tune = tuning_name
        tune = input_checking(tune, "Tuning", string_values)
        if len(string_values.get(tune)) is strs:
            outer_bo = True
        else:
            print("The tuning you chose does not match the number of string specified")
    slow_print("Now that we have your guitar settings specified. What chord would you like help with? Ex: c major, g# minor")
    ch = input_checking(input("Chord: "), "Chord", chords)
    return strs, frets, tune, ch

def input_checking(text, prompt, arr = {}):
    if text == "quit":
        sys.exit()
    if text == "exit":
        return text
    con = False
    while not con:
        if text.lower() == "help":
            help_menu()
            text = input(prompt + ": ")
            if prompt == "Tuning" and not text.strip():
                text = "standard"
            continue
        if len(text) == 0 and prompt != "Tuning":
            print("Length of input cannot be 0, please try again.")
            text = input(prompt + ": ")
            continue
        if len(text) > 17:
            print("Length of input " + str(text) + " was too long. Please re-enter your input")
            text = input(prompt + ": ")
            continue
        if len(arr) != 0:
            try:
                if (str(arr.get(text)).lower() == None):
                    print ("The input was not found in the list of available resources. Please enter a correct input.")
                    text = input(prompt + ": ")
                    if not text.strip():
                        text == "standard"
                    continue
            except:
                print ("The input was not found in the list of available resources and threw an exception. Please enter a correct input.")
                text = input(prompt + ": ")
                continue
        if prompt == "y/n":
            if text != 'y' and text != 'n':
                print("Value has to be \'y\' or \'n\'.")
                text = input(prompt + ": ")
                continue
        if prompt == "Strings" or prompt == "Fret Count":
            if not text.isdigit():
                print ("Value needs to be a number.")
                text = input (prompt + ": ")
                continue
            if prompt == "Strings":
                if int(text) > 12 or int(text) <= 0:
                    print ("Please ensure the number of guitar strings is between 1 and 12.")
                    text = input (prompt + ": ")
                    continue
            if prompt == "Fret Count":
                if int(text) > 42 or int(text) < 10:
                    print ("Please ensure the number of frets is between 10 and 42.")
                    text = input (prompt + ": ")
                    continue
        if prompt == "Chord":
            if len(text.split(" ")) != 2:
                if re.match(r"^(?P<note>[a-g](?:#|b)?)(?P<quality>major|minor)", text, flags=re.IGNORECASE):
                    print ("did you mean to type \'", text[0:text.lower().index("m")].lower(), " ", text[text.lower().index("m"):].lower(), "\'", "?", sep="")
                else:
                    print (text, "is not a valid chord, please check your chord and try again")
                text = input(prompt + ": ")
                continue
        con = True
    return text

def help_menu():
    con = False
    while not con:
        tmp = "\t|{: ^78}|"
        print_table_opener("Help")
        print (tmp.format("Please type an option from below or type \'exit\' to quit"))
        options = {"chord names": "x", "available tunings" : "x", "how to use": "x", "report a bug" : "x", "other": "x"}
        print (tmp.format(""))
        print (tmp.format("{:-^20}".format("")))
        for var in options.keys():
            print (tmp.format("-{:^20}-".format(var)))
        print (tmp.format("{:-^20}".format("")))
        print("\t{:->{}}".format("", 80))
        direction = input_checking(input(""), "Direction", options).lower()
        if direction == "exit":
            break

        print_table_opener(direction)
        if direction == "available tunings":
            for var in string_values:
                print (tmp.format("-{:^20}-".format(var)))
            print(tmp.format(""))
            print(tmp.format("If you are using a guitar with more or less than"))
            print(tmp.format("6 strings you may add a custom tuning by typing custom"))
        if direction == "chord names":
            for var in chords:
                print (tmp.format("-{:^20}-".format(var)))
        if direction == "how to use":
            print(tmp.format("1. Ensure you have read the README.md file"))
            print(tmp.format("2. Follow the prompts as the program outputs"))
            print(tmp.format("3. Read the output of the program and see what notes would sound good"))
        if direction == "report a bug":
            print(tmp.format("If there is a bug present in the program that is causing"))
            print(tmp.format("you problems you may go to the git repository for this project"))
            print(tmp.format("and open a new issue explaining what caused the error and"))
            print(tmp.format("what the output of the error is."))
        if direction == "other":
            print(tmp.format("Any question not answer in the help menu can be "))
            print(tmp.format("directed to the creator's email @etroknick@gmail.com."))
        if direction == "exit":
            break
        print(tmp.format(""))
        print("\t{:->{}}".format("", 80))
        print()
        print ("\tIs there anything else you need help with y/n?")
        tf = input_checking(input(""), "y/n")
        if tf == "n" or tf == "exit":
            con = True

# =================================================================    MAIN    ==========================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Wrong number of arguments. Expected none")
        sys.exit()
    else:
        slow_print("Welcome to my guitar lab. This platform will show you the notes of a fretboard that match any major or minor chord!")
        slow_print("If at any time you need help, type \"help\" and to terminate the program type \"quit\"")
        strs, frets, tune, ch = get_music_information()

    g = guitar(str(tune), int(strs), int(frets) + 1)
    c = chord(str(ch.split(" ")[0]), str(ch.split(" ")[1]))
    table= build_guitar_table(g, c)
    print ("The fret board for a guitar in", g.tuning, "over the chord", c.name, "is below.", "The notes in the chord are", chords.get(c.name), "\n\n")
    print_guitar(table)
    con = False
    while not con:
        ch = input_checking(input("Chord: "), "Chord", chords)
        c = chord(str(ch.split(" ")[0]), str(ch.split(" ")[1]))
        table= build_guitar_table(g, c)
        print ("The fret board for a guitar in", g.tuning, "over the chord", c.name, "is below.", "The notes in the chord are", chords.get(c.name), "\n\n")
        print_guitar(table)
    print()

    