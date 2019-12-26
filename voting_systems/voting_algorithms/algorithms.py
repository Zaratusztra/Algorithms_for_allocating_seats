# parties - słownik, kluczami są *nazwy partii*, a wartościami *ilość głosów oddana na daną partię*.

from decimal import Decimal
from collections import namedtuple

def straightforward(options):
    ranking=list()
    for voted in options.keys():
        ranking.append((voted,options[voted]))
    ranking = sorted(ranking, key=lambda x: int(x[1]))
    result = "Zwycięzcą jest {} z wynikiem {} głosów\n".format(ranking[-1][0], ranking[-1][1])
    for r in ranking[0:-1]:
        print(r)
        result += '"{}" otrzymał {} głosów.\n'.format(r[0],[1])
    return result

def dHondt(parties, seats=460):
    result = "Metoda d'Hondta:\n"
    assigned = 0
    
    seats_by_party = parties.copy()
    for k in seats_by_party.keys():     # Znaleźć lepsze rozwiązanie...... :C
        seats_by_party[k]=int(0)

    while assigned < seats:
        coefficient = dict()                    #Współczynniki (liczba głosów)/(l. przydz. miejsc+1) dla każd. partii
        for party in parties.keys():
            coefficient[party]=parties[party]/(seats_by_party[party]+1)
        ranking=[(p,coefficient[p]) for p in parties.keys()]    #para: partia-współczynnik
        ranking.sort(key=lambda element: element[1], reverse=True)            #przebieg wygrywa partia o najwyższym współczynniku
        #print("ranking:",ranking)
        seats_by_party[ranking[0][0]]+=1                        #partia dostaje miejsce
        assigned += 1
    final_list = [(party, seats_by_party[party]) for party in seats_by_party.keys()] # Partie i odpowiadająca im ilość miejsc w formie listy
    final_list = sorted(final_list, key = lambda element: element[1], reverse=True) # Sortujemy według listy miejsc
    #print(final_list)
    for party_seats in final_list: # pary partia-miejsce, posortowane
        result+='\nPartia "{}" otrzymuje {} miejsc.'.format(party_seats[0], party_seats[1])
    return result

def Sainte_Lague(parties, seats=460):
    result = "Metoda Sainte-Langue:\n"
    assigned = 0
    
    seats_by_party = parties.copy()
    for k in seats_by_party.keys():     # Znaleźć lepsze rozwiązanie...... :C
        seats_by_party[k]=int(0)

    while assigned < seats:
        coefficient = dict()                    #Współczynniki (liczba głosów)/(2*(l. przydz. miejsc)+1) dla każd. partii
        for party in parties.keys():
            coefficient[party]=parties[party]/(2*seats_by_party[party]+1)
        ranking=[(p,coefficient[p]) for p in parties.keys()]    #para: partia-współczynnik
        ranking.sort(key=lambda element: element[1], reverse=True)
        seats_by_party[ranking[0][0]]+=1                        #partia dostaje miejsce
        assigned += 1
    final_list = [(party, seats_by_party[party]) for party in seats_by_party.keys()]
    final_list = sorted(final_list, key = lambda element: element[1], reverse=True)

    for party_seats in final_list:
        result+='\nPartia "{}" otrzymuje {} miejsc.'.format(party_seats[0], party_seats[1])
    return result

def Sainte_Lague_mod(parties, seats=460): # Ta metoda preferuje nieco większe partie od wersji niezmodyfikowanej
    result = "Metoda Sainte-Langue (zmodyfikowana):\n"
    assigned = 0
    
    seats_by_party = parties.copy()
    for k in seats_by_party.keys():
        seats_by_party[k]=int(0)

    while assigned < seats:
        coefficient = dict()
        for party in parties.keys():
            coefficient[party]=parties[party]/(2*seats_by_party[party]+1) if seats_by_party[party]==0 else parties[party]/(1.4000)
        ranking=[(p,coefficient[p]) for p in parties.keys()]    #para: partia-współczynnik
        ranking.sort(key=lambda element: element[1], reverse=True)
        seats_by_party[ranking[0][0]]+=1
        assigned += 1
    final_list = [(party, seats_by_party[party]) for party in seats_by_party.keys()]
    final_list = sorted(final_list, key = lambda element: element[1], reverse=True)

    for party_seats in final_list: # pary partia-miejsce, posortowane
        result+='\nPartia "{}" otrzymuje {} miejsc.'.format(party_seats[0], party_seats[1])
    return result

def Hare_Niemeyer(parties, seats=460):
    result = "Metoda Hare-Niemeyer'a:\n"

    total_votes = 0
    for v in parties.values():
        total_votes+=v

    seats_by_party = parties.copy()
    for k in seats_by_party.keys():
        seats_by_party[k] = int(0)

    assigned = 0
    coefficient = dict()
    for party in parties.keys():
        coefficient[party] = Decimal(parties[party]*(seats-assigned)/total_votes)
    for party in seats_by_party.keys():
        seats_by_party[party]=int(coefficient[party])
        assigned += int(coefficient[party])
        coefficient[party]=coefficient[party]-int(coefficient[party])
    while assigned < seats:
        colist = [(k,coefficient[k]) for k in coefficient.keys()] #lista komplementarna do słownika coeficcients
        colist.sort(key=lambda element: element[1], reverse=True) # colist[0][0] - zawiera partię, której przydzielimy miejsca.
        coefficient[colist[0][0]]=0
        seats_by_party[colist[0][0]]+=1
        assigned+=1

    final_list = [(party, seats_by_party[party]) for party in seats_by_party.keys()]
    final_list = sorted(final_list, key=lambda element: element[1], reverse=True)

    for party_seats in final_list:  # pary partia-miejsce, posortowane
        result += '\nPartia "{}" otrzymuje {} miejsc.'.format(party_seats[0], party_seats[1])
    return result












