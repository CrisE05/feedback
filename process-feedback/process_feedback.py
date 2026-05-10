#!/usr/bin/env python3

import sys
import os
import csv
import unicodedata


def get_eval(s):
    if not isinstance(s,str):
        return s
    if s.startswith("5"):
        return 5
    if s.startswith("4"):
        return 4
    if s.startswith("3"):
        return 3
    if s.startswith("2"):
        return 2
    if s.startswith("1"):
        return 1
    if s.startswith("0"):
        return 0

    return 0


def get_h(s):
    # Students can choose between the following options:
    # We will consider the middle value.
    if s == "80% .. 100%":
        return 5
    if s == "60% .. 80%":
        return 4
    if s == "40% .. 60%":
        return 3
    if s == "20% .. 40%":
        return 2
    if s == "0% .. 20%":
        return 1

    return 0


def get_nota(s):
    if s == "sub 5":
        return 4
    return int(s)


def get_load(s):
    if s == "DA":
        return 2
    if s == "NU":
        return 0

    return 1


def get_uniq_elem_at_column(csv_data, c):
    uniq = set([])
    for line in csv_data:
        uniq.add(line[c])
    return list(uniq)


def average_at_column(csv_data, f, c):
    s = 0
    num = 0
    for line in csv_data:
        if line[c] == "":
            continue
        n = f(get_eval(line[c]))
        if n == 0:
            continue
        s += n
        num += 1.0
    if num == 0:
        return 0
    return round(s/num, 2)


def min_at_column(csv_data, f, c):
    minimum = -1    # for the rare case when all grades are 0
    for i in range(0, len(csv_data)):
        if csv_data[i][c] == "":
            continue
        if f(get_eval(csv_data[i][c])) == 0:
            continue
        minimum = f(get_eval(csv_data[i][c]))
        break
    for line in csv_data:
        if line[c] == "":
            continue
        if f(get_eval(line[c])) == 0:
            continue
        if f(get_eval(line[c])) < minimum:
            minimum = f(get_eval(line[c]))
    return minimum


def max_at_column(csv_data, f, c):
    maximum = 5
    for i in range(0, len(csv_data)):
        if csv_data[i][c] == "":
            continue
        maximum = f(get_eval(csv_data[i][c]))
        break
    for line in csv_data:
        if line[c] == "":
            continue
        if f(get_eval(line[c])) > maximum:
            maximum = f(get_eval(line[c]))
    return maximum


def get_header(csv_data):
    csv_data[0][2] = "Categorie"
    csv_data[0][3] = "Count"
    return csv_data[0][2:-4]


def get_stats(text, csv_data, f):
    # titular, asistent
    row = [text, len(csv_data)]

    # evaluare generala
    row.append(f(csv_data, get_eval, 4))
    # nota asteptata
    row.append(f(csv_data, float, 5))
    # incarcarea generala
    row.append(f(csv_data, get_eval, 6))
    # dotare locatie
    row.append(f(csv_data, get_eval, 7))
    # participare
    row.append(f(csv_data, get_h, 8))
    # cadrul didactic stapaneste
    row.append(f(csv_data, get_eval, 9))
    # metoda de expunere
    row.append(f(csv_data, get_eval, 10))
    # cursul a stimulat
    row.append(f(csv_data, get_eval, 11))
    # comportament cadru didactic
    row.append(f(csv_data, get_eval, 12))
    # materialele didactice suficiente pentru curs
    row.append(f(csv_data, get_eval, 13))
    # cadrul didactic stapaneste
    row.append(f(csv_data, get_eval, 14))
    # cadrul didactic sustine activitatea individuala
    row.append(f(csv_data, get_eval, 15))
    # cadrul didactic a raspuns intrebarilor
    row.append(f(csv_data, get_eval, 16))
    # comportament adecvat
    row.append(f(csv_data, get_eval, 17))
    # materiale didactice suficiente pentru aplicatii
    row.append(f(csv_data, get_eval, 18))
    # nr. ore saptamana pt teme
    row.append(f(csv_data, float, 19))
    # nr. + dificultate teme
    row.append(f(csv_data, get_eval, 20))
    # temele au ajutat la intelegerea materiei
    row.append(f(csv_data, get_eval, 21))

    return row


def filter_stats(f, f_id, csv_data, writer):
    p = f(csv_data, f_id)
    total = 0
    for e in p:
        a = [row for row in csv_data if row[f_id] == e]
        row = get_stats(e, a, average_at_column)
        total += int(row[1])
        writer.writerow(row)

    return total


def gather_data(infd, outfd):
    csv_data = []
    reader = csv.reader(infd)
    for line in reader:
        if line[0].startswith("Obs.:") or line[0] == "":
            break
        else:
            #print("--->>" + str(line))
            csv_data.append(line)
            
    # print(csv_data)
    writer = csv.writer(outfd, quoting=csv.QUOTE_ALL)

    writer.writerow(get_header(csv_data))

    writer.writerow([""])
    row = get_stats("Minim", csv_data[1:], min_at_column)
    writer.writerow(row)

    row = get_stats("Mediu", csv_data[1:], average_at_column)
    writer.writerow(row)

    row = get_stats("Maxim", csv_data[1:], max_at_column)
    writer.writerow(row)

    writer.writerow([""])
    writer.writerow(["Titulari Curs"])
    total_t = filter_stats(get_uniq_elem_at_column, 2, csv_data[1:], writer)
    writer.writerow(["Total:", total_t])

    writer.writerow([""])
    writer.writerow(["Asistenți"])
    total_a = filter_stats(get_uniq_elem_at_column, 3, csv_data[1:], writer)
    writer.writerow(["Total:", total_a])

def main():
    gather_data(sys.stdin, sys.stdout)

if __name__ == "__main__":
    sys.exit(main())
