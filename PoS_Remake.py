from ast import Return
import hashlib
import json
import random
import datetime

class Block :
    
    # Dans cette classe je défini ce qu'est un block de la blockchain, je lui donne des données "initiales" 
    # Il a donc un index : numéro de block, un timestamp : date et heure de creation, une data : la donnée que contient le block
    # Il a un previous_hash : le hash du block precedent, il a un hash : poour l'identifier uniquement et une preuve comme quoi il a respecté la preuve de minage
    
    def __init__(self, index, data, previous_hash, preuve):
        self.index = index
        self.timestamp = str(datetime.datetime.now())
        self.data = data
        self.previous_hash = previous_hash
        self.preuve = preuve
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        chaine_block = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(chaine_block).hexdigest()
        
    
class Blockain :
    
    # Dans cette classe, j'initalise une chaine appelée "chain" qui est une liste de block et j'initalise egalement une liste de posseseur de jeton
    
    def __init__(self):
        self.chain = [self.creation_premier_block()]
        self.posseseur_de_jetons = []
        
    # Ici, je crée le block initial de la chaine
    
    def creation_premier_block(self):
        init_data = 'premier_block_créé'
        index_premier_block = 0
        premier_block = Block(index_premier_block, init_data, hashlib.sha256(init_data.encode('utf-8')).hexdigest(),0)
        return premier_block
    
    # Ici je récupère le dernier block de la chain pour ensuite ajouter des nouveaux blocks
    
    def recup_block_precedent(self):
        return self.chain[-1]
    
    # Je défini la fonction pour ajouter un nouveau block
    
    def ajout_block(self, nv_blkock, preuve):
        nv_blkock.previous_hash = self.recup_block_precedent().hash
        nv_blkock.preuve = preuve
        nv_blkock.hash = nv_blkock.calculate_hash()
        self.chain.append(nv_blkock)
        
    def chaine_valid(self, chain):
        dernier_block = chain[0]
        index = 1
        
        while index < len(chain):
            block_regarde = chain[index]
            
            if block_regarde.previous_hash != dernier_block.hash :
                return False
            
            if not self.preuve_valid(dernier_block.preuve, block_regarde.preuve):
                return False
            
            dernier_block = block_regarde
            index += 1
        
        return True
    
    def preuve_valid(self, preuve_precedente, preuve):
        guess = f'{preuve_precedente}{preuve}'.encode()
        print(guess)
        guess_devine = hashlib.sha256(guess).hexdigest()
        print(guess_devine)
        print('------')
        return guess_devine[:2] == '00'
    
    def preuve_enjeu(self, block, derniere_preuve):
        preuve = 0
        
        while self.preuve_valid(derniere_preuve, preuve) is False :
            preuve +=1
            
        block.preuve = preuve
        return preuve
            
            
Test_blockchain = Blockain()

print(Test_blockchain.chain[0].previous_hash)

#print(Test_blockchain.preuve_valid(0o5,63))


Test_blockchain.ajout_block(Block(1, 'block2', Test_blockchain.chain[-1].previous_hash, Test_blockchain.chain[-1].preuve),Test_blockchain.preuve_enjeu(Test_blockchain.chain[-1],Test_blockchain.chain[-1].preuve))

print(len(Test_blockchain.chain))
'''print(Test_blockchain.chain[0])
print(Test_blockchain.chain[1])

'''
for i in range(0, len(Test_blockchain.chain)):
  print('numero du block :' , Test_blockchain.chain[i].index)
  print('Hash:' , Test_blockchain.chain[i].hash)
  print('Data :' , Test_blockchain.chain[i].data)
  print('Preuve :' , Test_blockchain.chain[i].preuve)
  print( '-------------------------')