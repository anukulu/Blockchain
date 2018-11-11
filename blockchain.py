# creating a blockchain

#importing the libraries
import datetime   #required to timestamp a blockchain
import hashlib 
import json
from flask import Flask, jsonify

#Part--1 : Building a blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof': proof, # it is the nonce of the block
                 'previous_hash' : previous_hash}
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1 #This is the nonce that can be varied in the block to find the hash
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000': #These are the leading zeros or target hash below which the hashes have to be
                                             #found for adding the block to the blockchain
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
            #if proof_of_work(previous_proof) != proof:
                return False
            block_index += 1
            previous_block = block
        return True
        
#Part--2 : Mining a blockchain

#Creating a webapp to interact with the blockchain
app = Flask(__name__)

#Creating the insatnce of the blockchain
blockchain = Blockchain()

#Mining the block
@app.route('/mine_block', methods=['GET']) #It routes the web app to the specified URL using the method GET to get info
                                             #The URL is 127.0.0.1:5000/mine_block for mining function
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : 'Congratulations you just mined a block',
                'index' : block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash' : block['previous_hash']}
    return jsonify(response), 200 #200 is the HTTP status code for OK signal

#Getting the blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain' : blockchain.chain,
                'length' : len(blockchain.chain)}
    return jsonify(response), 200 #return statement returns this object whenever we make requests in the 
                                #browser using the URL specified for the Flask server ie: 127.0.0.1 in this case

#checking if the blockchain is valid or not
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    if blockchain.is_chain_valid(blockchain.chain) is True:
        response = {'message': 'The blockchain is valid'}
    else:
        response = {'message': 'The blockchain is invalid'}
    return jsonify(response), 200

#Running the application
app.run(host = '0.0.0.0', port = 5000) #this specifies the host(0.0.0.0 means publicly available) and the 
                                        #port number which is 5000 for flask server
    
    
    
    
    
    
    
    
    
    