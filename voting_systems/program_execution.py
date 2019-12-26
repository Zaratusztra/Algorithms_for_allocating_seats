#import voting_systems.voting_algorithms.algorithms as algorithms

import os
import sys
import csv
from pathlib import Path

from .voting_algorithms import algorithms

class Executor:

    def __init__(self, profile=None):
        self._profile = profile
        self._seats = 460
    
    @property
    def profile(self):
        return self._profile
        
    @profile.setter
    def profile(self,profile):
        if type(profile) is dict:
            for v in profile.values():
                try:
                    int(v)
                except ValueError:
                    raise ValueError("pierwsza pozycja musi być nazwą a druga liczbą naturalną.")
                #except ValueError as err:
                #   raise err
            self._profile=profile
    
    def add_to_profile(self, new):
        if self._profile is None:
            self.profile = {new[0]:new[1]}
        try:
            self._profile[str(new[0])]=int(new[1])
        except ValueError:
            raise ValueError("Para musi składać się z nazwy i liczby głosów, wyrażonej jako liczba naturalna.")
    
    def delete_from_profile(self, k):
        self._profile.pop(k)
        
    
    def delete_profile(self):
        self._profile = None
    
    def get_profile_repr(self):
        """Zwraca ponumerowaną listę par opcja/kandydat-ilość głosów."""
        if self.profile is None:
            return "Profil głosowania jest pusty."
        rep = "-----------------------------------------\n"
        i=1
        for option in self.profile:
            rep += "{}. {} - {} głosów\n".format(str(i),option,str(self.profile[option]))
            i+=1
        rep += "\n-----------------------------------------\n"
        return rep
    
    def save_profile_to_file(self, filename):
        """Zapisuje aktualny profil głosowania do pliku csv o nzawie podanej jako argument funkcji"""
        if filename == '' or filename == None:
            raise Exception("Nieporawna nazwa pliku.")
            
        if filename.split(".")[-1] == "csv" or filename.split(".")[-1] == "txt":
            filename = ''.join(filename.split('.')[0:-1:1])
        
        # UWAGA! Przygotowywanie i czyszczenie ścieżki do plików z zapisami
        path = Path(os.getcwd())
        if "__main__.py" not in os.listdir(path):
                path = path / sys.argv[0]
        path =  path / "save"
        
        if not os.path.exists(path):
            os.mkdir("save")
            
        with open(path / "{}.csv".format(filename), "w", newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            for row_key in self._profile.keys():
                csv_writer.writerow([row_key, self._profile[row_key]])
    
    def load_profile_from_file(self, filename):
        if filename == '' or filename == None:
            raise Exception("\nNiepoprawna nazwa pliku.")
            
        if filename.split(".")[-1] == "csv" or filename.split(".")[-1] == "txt":
            filename = ''.join(filename.split('.')[0:-1:1])
            
        self._profile = dict()
        
        # UWAGA! Przygotowywanie i czyszczenie ścieżki do plików z zapisami
        path = Path(os.getcwd())
        if "__main__.py" not in os.listdir(path):
                path = path / sys.argv[0]
        path =  path / "save"
        
        with open(path / "{}.csv".format(filename), "r", newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            try:
                for row in csv_reader:
                    print(repr(row))
                    self._profile[row[0]]=int(row[1])
            except ValueError:
                raise ValueError("Napotkano nieprawidłowe dane w pliku {}".format(filename))
    
    def execute_voting(self):
        if self._profile is None:
            return "Profil głosowania jest pusty."
        result = "Testowane algorytmy:\n--------------------------------------------------------------------\n"
        result += algorithms.dHondt(self._profile, self._seats)
        result += "\n\n"+algorithms.Sainte_Lague(self._profile, self._seats)
        #result += "\n\n"+algorithms.Sainte_Lague_mod(self._profile, self._seats)
        result += "\n\n"+algorithms.Hare_Niemeyer(self._profile, self._seats)
        return result
    
