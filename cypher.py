import sys
import os
import random
from collections import defaultdict, Counter

from fontTools.misc.eexec import encrypt
from sympy.logic.utilities import load_file


def main():
    message = input("Wpisz szyfrogram lub tekst do zaszyfrowania: ")
    process = input("Wpisz 'encrypt' (szyfrowanie) " "lub decrypt' (odszyfrowanie): ")
    while process not in ('encrypt', 'decrypt'):
        process = input("Niepoprawny proces. " "Wpisz 'encrypt' lub 'descrypt': ")
    shift = int(input("Przesuniecie indeksu (1-366) = "))
    while not 1 <= shift <= 366:
        shift = int(input("Niepoprawna wartosc. " "Wpisz liczbe od 1 do 366: "))
    infile = input("Wpisz pełną nazwe pliku: ")

    if not os.path.exists(infile):
        print("Nie znaleziono pliku {}. Program konczy dzialanie.".format(infile), file=sys.stderr)
        sys.exit(1)
    text = load_file(infile)
    char_dict = make_dict(text, shift)
    if process == 'encrypt':
        ciphertext = encrypt(message, char_dict)
        if check_for_fail(ciphertext):
            print("\nNie znaleziono unikalnych kluczy.", file=sys.stderr)
            print("Sprobuj ponownie po zmianie tekstu lub ksiazki.\n", file=sys.stderr)
            sys.exit()
        print("\nLiczba wystapien znakow w char_dict: \n")
        print("{: >10}{: >10}{: >10}".format('Znak', 'Unicode', 'Liczba'))
        for key in sorted(char_dict.keys()):
            print('{:>10}{:>10}{:>10}'.format(repr(key)[1:-1], str(ord(key)), len(char_dict[key])))
        print('\nLiczba roznych znakow: {}'.format(len(char_dict)))
        print("Calkowita liczba znakow: {:,}\n".format(len(text)))
        print("szyfrogram = \n{}\n".format(ciphertext))
        print("tekst jawny = ")
        for i in ciphertext:
            print(text[i - shift], end='', flush=True)
    elif process == 'decrypt':
        plaintext = decrypt(message, text, shift)
        print("\ntekst jawny = \n{}".format(plaintext))


def load_file(infile):
    """Odczytuje i zwraca plik tekstowy jako ciąg znaków złożony z małych liter."""
    with open(infile) as f:
        loaded_string = f.read().lower()
        return loaded_string


def make_dict(text, shift):
    """Zwraca słownik znaków jako kluczy i przesuniętych indeksów jako wartości."""
    char_dict = defaultdict(list)
    for index, char in enumerate(text):
        char_dict[char].append(index + shift)
    return char_dict


def encrypt(message, char_dict):
    """Zwraca listę indeksów reprezentujących znaki w wiadomości."""
    encrypted = []
    for char in message.lower():
        if len(char_dict[char]) > 1:
            index = random.choice(char_dict[char])
            # Random.choice kończy się błędem, jeżeli jest tylko 1 opcja do wyboru
        elif len(char_dict[char]) == 1:
            index = char_dict[char][0]
        elif len(char_dict[char]) == 0:
            print("\nBrak znaku {} w slowniku.".format(char), file=sys.stderr)
            continue
        encrypted.append(index)
    return encrypted


def decrypt(message, text, shift):
    """Odszyfrowuje szyfrogram i zwraca ciąg znaków z tekstem jawnym."""
    plaintext = ''
    indexes = [s.replace(',', '').replace('[', '').replace(']', '') for s in message.split()]
    for i in indexes:
        plaintext += text[int(i) - shift]
    return plaintext

def check_for_fail(ciphertext):
    """Zwraca True, jeżeli szyfrogram zawiera powielone klucze."""
    check = [k for k, v in Counter(ciphertext).items() if v > 1]
    if len(check) > 0:
        return True

if __name__ == '__main__':
    main()
