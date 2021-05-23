#!/usr/bin/env python3
import hashlib, sys, time
import pandas as pd
from itertools import product

def get_algorithm(type):
    # Dynamically creates the right function and returns it
    # using python closure, it is only used to build types_dict
    def algorithm(string):
        h = type()
        h.update(string.encode('utf-8'))
        return h.hexdigest()
    return algorithm


ALGO_DICT = { 'MD5'    : get_algorithm( hashlib.md5 ),
               'SHA1'   : get_algorithm( hashlib.sha1 ),
               'SHA224' : get_algorithm( hashlib.sha224 ),
               'SHA256' : get_algorithm( hashlib.sha256 ),
               'SHA384' : get_algorithm( hashlib.sha384 ),
               'SHA512' : get_algorithm( hashlib.sha512 ) }

class DictionaryAttack():
    """ Main class """
    
    def __init__( self ):
        self.dictionary = None
        self.password = {}
        self.hash_func = None

    def main( self ):
        # Calls the get_hash method
        self.get_dictionary_file()
        self.get_password_file()
        self.get_hash_func()
        result = self.dict_attack()
        with open('result.txt', 'w') as file:
          for key, value in result.items():
            file.write(f'{key} {value}\n')

            
    def get_hash_func(self):
        # Prompts for a cryptographic function
        while True:
            for index, cryp_func in enumerate(ALGO_DICT.keys()):
                print(f'{index+1}. {cryp_func}')

            cryp_func = input('Please choose the cryptographic function (enter the name) or type "exit" to stop the program: ')
            
            if cryp_func == 'exit':
                sys.exit()
            if cryp_func in ALGO_DICT.keys():
                self.hash_func = ALGO_DICT[cryp_func]
                break
            else:
                print(f'{cryp_func} is not supported! Please try again.\n')
                                             
    def get_dictionary_file(self):
        self.dictionary = pd.read_csv("dictionary.txt", names=["Vocabulary"], sep="\"\,\"", dtype='str', engine='python')
        self.dictionary = self.dictionary.applymap(str)    

    def get_password_file(self):
        try:
            file = open('password.txt', 'r', encoding='utf-8')
        except FileNotFoundError:
            print('password.txt is not found in folder')
            sys.exit()
        
        # Reads file and returns a list.
        password = {}
        for line in file:
            (key, val) = line.split()
            password[key] = val
        file.close()
        self.password = password

    def dict_attack(self):
        self.start = time.time()
        result = self.password
        print('Checking...\n\n')
        for key, value in self.password.items():
          changed = False
          for word in self.dictionary.iloc[:,0]:
            test = self.hash_func(word)
            if value == test:
              result[key] = word
              changed = True
          if not changed:
            result[key] = '----- Could not cracked -----'
        return result
                
if __name__ == "__main__":
    runner = DictionaryAttack()
    runner.main()