#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Główna klasa programu"""

# DODAĆ WYJĄTKI - OBSŁUGĘ BŁĘDÓW

import os
import sys
from pathlib import Path

import voting_systems.program_execution

def cls():
    if os.name == 'nt':
            os.system("cls")
    elif os.name == 'posix':
        os.system("clear")

def wait():
    input("\nNaciśnij dowolny klawisz aby kontynuować.")
    cls()
    

def add_to_list(executor):
    try:
        if executor.profile is None:
            pair = input('\nPodaj parę [głosowana-opcja], [ilość-głosów]: ').split(',')
            executor.profile={pair[0]:int(pair[1])}
            return
        pair = input('\nPodaj parę [głosowana-opcja], [ilość-głosów]: ').split(',')
        executor.add_to_profile(pair)
        cls()
    except Exception as err:
        print(err)
        wait()

def delete_from_list(executor):
    print(executor.get_profile_repr())
    try:
        executor.delete_from_profile( input("\nKtórą opcję? (wpisz nazwę)") )
    except KeyError:
        print("\nTakiej opcji nie ma na liście")
        wait()

def clear_list(executor):
    executor.delete_profile()
    cls()

def main(): #zaimportować klasę obsługującą test i zapewnić interfejs tekstowy.
    options="""
    [1] - Zaktualizuj profil głosowania
    [2] - Wykonaj głosowanie
    [3] - Wyświetl bieżący profil głosowania
    [4] - Zapisz bieżący profil głosowania do pliku
    [5] - Wczytaj profil głosowania z pliku
    [X] - Zakończ pracę programu
    """
    executor=voting_systems.program_execution.Executor()
    if len(sys.argv)>1:
        if sys.argv[1] == '-gui':
            # tu uruchomimy eksperymentalne GUI
            return 0
        if sys.argv[1] == "-ffile":
            try:
                executor.load_profile_from_file(sys.argv[2])
            except Exception as err:
                print(err)
    
    option=True
    cls()
    while option!='X' and option!='x' and option != 'exit':
        #print(sys.argv[0])
        print("\n  ",os.getcwd())
        print(options)
        option=input('>')
        cls()
        if option == '1': # AKTUALIZACJA
            choice = input("Chcesz [d]odać czy [u]sunąć pozycję z listy? Możesz też wy[c]zyścić listę.")
            if choice == 'c':
                clear_list(executor)
            elif choice == 'u':
                delete_from_list(executor)
            elif choice == 'd':
                add_to_list(executor)
            else: 
                print("\nNieznane polecenie, spróbuj ponownie")
                wait()
            cls()
        if option == '2': # WYKONANIE GŁOSOWANIA
            print('\n\n\t')
            print(executor.execute_voting())
            wait()
        if option == '3': # WYŚWIETLANIE PROFILU
                print('\n')        
                print(executor.get_profile_repr())
                wait()
        if option == '4': # ZAPISYWANIE PROFILU DO PLIKU
            try:
                executor.save_profile_to_file(input("\nWpisz nazwę pliku: "))
                cls()
            except Exception as err:
                print(err)
                wait()
        if option == '5': # WCZYTYWANIE PROFILU Z PLIKU
        
            path = Path(os.getcwd())
            if "__main__.py" not in os.listdir(path):
                path = path / sys.argv[0]
            path = path / "save"
            print(path,"\n+\n|\n|")
            for x in os.listdir(path): print("|-",x)
            
            try:
                executor.load_profile_from_file(input("\nWpisz nazwę pliku: "))
                cls()
            except Exception as err:
                print(err)
                wait()

main()
