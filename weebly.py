from web3 import Web3
import json
import os
import pickle
import time

# Connect to the Infura project
your_infura_project_id = "93fd067aa3d34ba1bb7b1110ca535409"
infura_url = f"https://ropsten.infura.io/v3/{your_infura_project_id}"
w3 = Web3(Web3.HTTPProvider(infura_url))

print(f"Web3 is connected?: {w3.isConnected()}")
# vyper -f abi company_stock.vy
ABI = '[{"name": "Transfer", "inputs": [{"name": "sender", "type": "address", "indexed": true}, {"name": "receiver", "type": "address", "indexed": true}, {"name": "value", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "Buy", "inputs": [{"name": "buyer", "type": "address", "indexed": true}, {"name": "buy_order", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "Sell", "inputs": [{"name": "seller", "type": "address", "indexed": true}, {"name": "sell_order", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "Pay", "inputs": [{"name": "vendor", "type": "address", "indexed": true}, {"name": "amount", "type": "uint256", "indexed": false}], "anonymous": false, "type": "event"}, {"stateMutability": "nonpayable", "type": "constructor", "inputs": [{"name": "_company", "type": "address"}, {"name": "_total_shares", "type": "uint256"}, {"name": "initial_price", "type": "uint256"}], "outputs": []}, {"stateMutability": "view", "type": "function", "name": "stockAvailable", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 4952}, {"stateMutability": "payable", "type": "function", "name": "buyStock", "inputs": [], "outputs": [], "gas": 85886}, {"stateMutability": "view", "type": "function", "name": "getHolding", "inputs": [{"name": "_stockholder", "type": "address"}], "outputs": [{"name": "", "type": "uint256"}], "gas": 3171}, {"stateMutability": "view", "type": "function", "name": "cash", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 380}, {"stateMutability": "nonpayable", "type": "function", "name": "sellStock", "inputs": [{"name": "sell_order", "type": "uint256"}], "outputs": [], "gas": 122880}, {"stateMutability": "nonpayable", "type": "function", "name": "transferStock", "inputs": [{"name": "receiver", "type": "address"}, {"name": "transfer_order", "type": "uint256"}], "outputs": [], "gas": 80332}, {"stateMutability": "nonpayable", "type": "function", "name": "payBill", "inputs": [{"name": "vendor", "type": "address"}, {"name": "amount", "type": "uint256"}], "outputs": [], "gas": 40765}, {"stateMutability": "view", "type": "function", "name": "debt", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 14965}, {"stateMutability": "view", "type": "function", "name": "worth", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 15164}, {"stateMutability": "view", "type": "function", "name": "company", "inputs": [], "outputs": [{"name": "", "type": "address"}], "gas": 2658}, {"stateMutability": "view", "type": "function", "name": "totalShares", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2688}, {"stateMutability": "view", "type": "function", "name": "price", "inputs": [], "outputs": [{"name": "", "type": "uint256"}], "gas": 2718}]'
abi = json.loads(ABI)
# vyper -f bytecode company_stock.vy
BYTECODE = '0x60606105e86101403960206105e860c03960c05160a01c1561002057600080fd5b6000610160511161003057600080fd5b6000610180511161004057600080fd5b61014051600055610160516001556101805160025561016051600360005460e05260c052604060c020556105d056600436101561000d576104b6565b600035601c52600051631d1dc1f08114156100ef5734600254808061003157600080fd5b820490509050610140526101405161014051600658016104bc565b610160526101405261016051101561006357600080fd5b600360005460e05260c052604060c0208054610140518082101561008657600080fd5b8082039050905081555060033360e05260c052604060c0208054610140518181830110156100b357600080fd5b808201905090508155506101405161016052337fe3d4187f6ca4248660cc0ac8b8056515bac4a8132be2eca31d6d0cc170722a7e6020610160a2005b34156100fa57600080fd5b633ce828de81141561012057600658016104bc565b610140526101405160005260206000f35b63eeb466348114156101615760043560a01c1561013c57600080fd5b6004356101405261014051600658016104dd565b6101a0526101a05160005260206000f35b63961be391811415610177574760005260206000f35b639104c81e8114156102a65760006004351161019257600080fd5b600435336101405261014051600658016104dd565b6101a0526101a05110156101ba57600080fd5b60043560025480820282158284830414176101d457600080fd5b809050905090504710156101e757600080fd5b60033360e05260c052604060c02080546004358082101561020757600080fd5b80820390509050815550600360005460e05260c052604060c020805460043581818301101561023557600080fd5b808201905090508155506000600060006000600435600254808202821582848304141761026157600080fd5b80905090509050336000f161027557600080fd5b60043561014052337f5e5e995ce3133561afceaa51a9a154d5db228cd7525d34df5185582c18d3df096020610140a2005b637f59e5348114156103855760043560a01c156102c257600080fd5b6000602435116102d157600080fd5b602435336101405261014051600658016104dd565b6101a0526101a05110156102f957600080fd5b60033360e05260c052604060c02080546024358082101561031957600080fd5b80820390509050815550600360043560e05260c052604060c020805460243581818301101561034757600080fd5b8082019050905081555060243561014052600435337fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef6020610140a3005b632293448781141561040b5760043560a01c156103a157600080fd5b60005433146103af57600080fd5b6024354710156103be57600080fd5b60006000600060006024356004356000f16103d857600080fd5b602435610140526004357f357b676c439b9e49b4410f8eb8680bee4223724802d8e3fd422e1756f87b475f6020610140a2005b630dca59c18114156104315760065801610503565b610140526101405160005260206000f35b63ad11c13181141561046c574760065801610503565b61014052610140518082101561045c57600080fd5b8082039050905060005260206000f35b636904c94d8114156104845760005460005260206000f35b633a98ef3981141561049c5760015460005260206000f35b63a035b1fe8114156104b45760025460005260206000f35b505b60006000fd5b61014052600360005460e05260c052604060c0205460005260005161014051565b610160526101405260036101405160e05260c052604060c0205460005260005161016051565b6101405260015461014051600658016104bc565b6101605261014052610160518082101561053057600080fd5b80820390509050600254808202821582848304141761054e57600080fd5b8090509050905060005260005161014051565b61006f6105d00361006f60003961006f6105d0036000f3'


print("Checking for saved receiver account")
if os.path.exists("receiver_account.p"):
    file = open("receiver_account.p", 'rb')
    receiver_account = pickle.load(file)
    file.close()
else:
    print("Couldn't find saved receiver account, creating a new one.")
    receiver_account = w3.eth.account.create("receiver_account")
    file = open("receiver_account.p", 'wb')
    pickle.dump(receiver_account, file)
    file.close()

print("Checking for saved sender account")
if os.path.exists("sender_account.p"):
    file = open("sender_account.p", 'rb')
    sender_account = pickle.load(file)
    file.close()
else:
    print("Couldn't find saved sender account, creating a new one.")
    sender_account = w3.eth.account.create("sender_account")
    file = open("sender_account.p", 'wb')
    pickle.dump(sender_account, file)
    file.close()
    print("Getting ropsten token, you can do this only once per day.")
    os.system(f"wget https://faucet.ropsten.be/donate/{sender_account.address}")

# ================ BUILD CONTRACT ================
company_shares = 100000
company_shares_price = 1

company_stock = w3.eth.contract(abi=abi, bytecode=BYTECODE)
construct_txn = company_stock.constructor(sender_account.address, company_shares, company_shares_price).buildTransaction({
    'chainId': 3,
    'from': sender_account.address,
    'gas': 700000,
    'gasPrice': w3.toWei('220', 'gwei'),
    'nonce': w3.eth.getTransactionCount(sender_account.address)})
# You may need to adjust the gas and the gasPrice for this to complete.
# Upon completion, all of the shares will be given to the contract creator.

# Sign, create the contract, and wait until the transaction is complete.
print("Creating the contract transaction")
signed_txn = w3.eth.account.signTransaction(construct_txn, sender_account.privateKey)
print(f"Signed Txn: {signed_txn}")
tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
print(f"tx HASH: {tx_hash}")
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(f"TX RECEIPT: {tx_receipt}")
print(f"NEW CONTRACT ADDRESS: {tx_receipt.contractAddress}")

time_to_wait = 240
print(f"It may take a few minutes to create your contract, sleeping for {time_to_wait} seconds.")
time.sleep(time_to_wait)
# =========================
amount_to_buy = 20

contract_addr = tx_receipt.contractAddress
# contract_addr="0x39898B49021fa1d7847D8C507fe3a750f5DcDfba"
contract_instance = w3.eth.contract(address=contract_addr, abi=abi)

print(f"Sender Account: {sender_account.address}")
# print(f"Sender Account Private Key: {sender_account.privateKey}")
print(f"Receiver Account: {receiver_account.address}")
# print(f"Receiver Account Private Key: {receiver_account.privateKey}")
print(f"Contract Address: {contract_addr}")
contract_owner = sender_account.address
contract_owner_private = sender_account.privateKey
print(f"Contract Owner address: {contract_owner}")

print(f"Get holding for contract_addr:")
print(contract_instance.functions.getHolding(contract_addr).call())
print(f"Get holding for contract_owner address:")
print(contract_instance.functions.getHolding(contract_owner).call())
print(f"Get holding for sender_account address:")
print(contract_instance.functions.getHolding(sender_account.address).call())
print(f"Get holding for receiver_account address:")
print(contract_instance.functions.getHolding(receiver_account.address).call())


print(f"\n{receiver_account.address} is transferring {amount_to_buy} shares of stock.\n")
# Functions: payBill, sellStock, buyStock, transferStock
transaction = contract_instance.functions.transferStock(receiver_account.address, amount_to_buy).buildTransaction({'chainId': 3, 'gas': 75000, 'nonce': w3.eth.getTransactionCount(sender_account.address)})
signed_txn = w3.eth.account.signTransaction(transaction, sender_account.privateKey)
txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.waitForTransactionReceipt(txn_hash)

print(f"Get holding for Contract address:")
print(contract_instance.functions.getHolding(contract_addr).call())
print(f"Get holding for sender_account address:")
print(contract_instance.functions.getHolding(sender_account.address).call())
print(f"Get holding for receiver_account address:")
print(contract_instance.functions.getHolding(receiver_account.address).call())

print("\nFINISHED.")
