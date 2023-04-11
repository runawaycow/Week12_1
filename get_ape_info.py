from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.toChecksumAddress(bayc_address)

#You will need the ABI to connect to the contract
#The file 'abi.json' has the ABI for the bored ape contract
#In general, you can get contract ABIs from etherscan
#https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('/home/codio/workspace/abi.json', 'r') as f:
	abi = json.load(f) 

############################
#Connect to an Ethereum node
api_url = 'ipfs://QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/1E'
provider = HTTPProvider(api_url)
web3 = Web3(provider)

def get_ape_info(apeID):
	assert isinstance(apeID,int), f"{apeID} is not an int"
	assert 1 <= apeID, f"{apeID} must be at least 1"

	data = {'owner': "", 'image': "", 'eyes': "" }

	############################
	#Get Contract ABI from etherscan
	ABI_ENDPOINT = 'https://api.etherscan.io/api?module=contract&action=getabi&address='
	try:
		response = requests.get( f"{ABI_ENDPOINT}{contract_address}", timeout = 20 )	
		abi = response.json()
	except Exception as e:
		print( f"Failed to get {contract_address} from {ABI_ENDPOINT}" )
		print( e )

	bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
	
	############################
	#Connect to an Ethereum node
	token = "Mwb3juVAfI1g2RmA1JCGdYk-2_BmFrnLOtbomP1oDa4"
	api_url = f"https://c2emjgrvmi7cabd41mpg.bdnodes.net?auth={token}"
	provider = HTTPProvider(api_url)
	web3 = Web3(provider)

	contract = web3.eth.contract(address=contract_address,abi=abi)

    # Call the contract function to get the owner of the ape
    owner = contract.functions.ownerOf(apeID).call()

    # Call the contract function to get the image URL of the ape
    image = contract.functions.tokenURI(apeID).call()

    # Call the contract function to get the eye color of the ape
    eyes = contract.functions.getApeDetails(apeID).call()[3]

    # Fill the data dictionary with the results
    data['owner'] = owner
    data['image'] = image
    data['eyes'] = eyes

	assert isinstance(data,dict), f'get_ape_info{apeID} should return a dict' 
	assert all( [a in data.keys() for a in ['owner','image','eyes']] ), f"return value should include the keys 'owner','image' and 'eyes'"
	return data
