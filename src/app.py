from flask import Flask,render_template,request,url_for
import json
from web3 import Web3, HTTPProvider
import paho.mqtt.client as mqtt

blockchain_address = 'http://127.0.0.1:7545'
web3 = Web3(HTTPProvider(blockchain_address))
web3.eth.defaultAccount = web3.eth.accounts[0]

compiled_contract_path = '../build/contracts/iot.json'
deployed_contract_address = '0xe33807230b498D76dd97756DD40D22e34688f503'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

app = Flask(__name__,static_url_path='/static')
m=''
client=mqtt.Client()
client.connect('broker.hivemq.com',1883)

@app.route('/on/',methods=["POST"])
def on():
	print("Bulb On")
	m="Bulb On"
	client.publish('madblocks','on')

	tx_hash = contract.functions.controlBulb(1).transact()
	web3.eth.waitForTransactionReceipt(tx_hash)

	return (render_template('index.html',m=m,thash=tx_hash))

@app.route('/off/',methods=["POST"])
def off():
	print('Bulb Off')
	m='Bulb Off'
	client.publish('madblocks','off')
	tx_hash = contract.functions.controlBulb(0).transact()
	web3.eth.waitForTransactionReceipt(tx_hash)

	return (render_template('index.html',m=m,thash=tx_hash))

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True, host='127.0.0.1')
