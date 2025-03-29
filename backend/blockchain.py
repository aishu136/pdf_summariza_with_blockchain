from web3 import Web3
import os

# Connect to Ethereum via Infura
INFURA_URL = "https://sepolia.infura.io/v3/11fae2668eea4166aea904be0ebd390c"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

if w3.is_connected():
    print("Connected to Ethereum via Infura")
else:
    raise Exception("Failed to connect to Infura")

# Smart Contract Details
contract_address = "0xd9145CCE52D386f254917e481eB44e9943F39138"
abi =  [
	{
		"inputs": [],
		"name": "getSummary",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_summary",
				"type": "string"
			}
		],
		"name": "storeSummary",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "summary",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]   

contract = w3.eth.contract(address=contract_address, abi=abi)

# Ethereum Account Details
ACCOUNT = "0xb3e3E425b2Ed361556F577950189Bef3D6531C2C"
PRIVATE_KEY = "6a49c26135f5731219219bb278d5c547731859f729dfbb0c220d5363af579956"

def store_summary_on_blockchain(summary):
    try:
        tx = contract.functions.storeSummary(summary).build_transaction({
            "from": ACCOUNT,
            "nonce": w3.eth.get_transaction_count(ACCOUNT),
            "gas": 2000000,
            "gasPrice": w3.to_wei("20", "gwei"),
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)  
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction) 

        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        return tx_receipt.transactionHash.hex()

    except Exception as e:
        return f"Error: {str(e)}"

