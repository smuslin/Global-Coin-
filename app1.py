import os
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import json

load_dotenv()

# Connect to a local Ethereum node (you should replace 'http://localhost:7545' with your node's address)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Address of the deployed GC_TokenCrowdsaleDeployer contract
deployer_contract_address = "SMART_CONTRACT_ADDRESS"
#deployer_contract_abi = []  # ABI of GC_TokenCrowdsaleDeployer contract
with open(Path('gc_abi.json')) as f:
        gc_abi = json.load(f)

# Connect to the deployed GC_TokenCrowdsaleDeployer contract
deployer_contract = w3.eth.contract(address='0xF55a6f104BF9E4A3f307022f0Dca4084799F8b80', abi=gc_abi)

# Streamlit App
st.title("GC Token Crowdsale App")

# Form to deploy a new crowdsale
st.header("Deploy New Crowdsale")

token_name = st.text_input("Token Name:")
token_symbol = st.text_input("Token Symbol:")
wallet_address = st.text_input("Wallet Address:")

if st.button("Deploy Crowdsale"):
    # Deploy a new crowdsale
    try:
        transaction_hash = deployer_contract.functions.deployNewCrowdsale(token_name, token_symbol, wallet_address).transact()
        st.success(f"Transaction Hash: {transaction_hash.hex()}")
    except Exception as e:
        st.error(f"Error deploying crowdsale: {e}")

# Display existing crowdsale details
st.header("Existing Crowdsale Details")

total_supply = deployer_contract.functions.totalSupply().call()
#gc_token_name = GC_TOKEN.functions.name().call()

st.write(f"Total Supply: {total_supply}")

accounts = w3.eth.accounts
#address = st.selectbox(“Select Account”, options=accounts)
selected_address = st.selectbox("Select Account", options=accounts)
Balance = deployer_contract.functions.balanceOf(selected_address).call()
st.write(f"Balance: {Balance}")
#st.write(f"GC Crowdsale Address: {gc_token_name}")

#Here's an example demonstrating how you can structure your Streamlit app to have multiple pages:
#6:04
#Code:
# page1.py

#def page1():
#    st.title("Page 1")
#    st.write("This is the content of Page 1.")
# page2.py

#def page2():
#    st.title("Page 2")
#    st.write("This is the content of Page 2.")
# main.py

#from page1 import page1
#from page2 import page2
# Create a navigation sidebar
#page = st.sidebar.selectbox("Go to", ["Page 1", "Page 2"])
# Handle page selection
#if page == "Page 1":
#    page1()
#elif page == "Page 2":
#    page2()