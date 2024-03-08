import os
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import json

load_dotenv()

# Connect to a local Ethereum node (you should replace 'http://localhost:7545' with your node's address)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# GC Token
with open(Path('gc_abi.json')) as f:
        gc_abi = json.load(f)

deployer_contract = w3.eth.contract(address='0x862f66C506D73D603113728B88F02e0474FC9e2c', abi=gc_abi)

# GC Token Crowdsale
with open(Path('gc_abi2.json')) as f:
        gc_abi2 = json.load(f)

deployer_contract2 = w3.eth.contract(address='0x90dDC06B3Cd62a6D631Bc63d047AaEE0E7567E37', abi=gc_abi2)

# Streamlit App
st.title("GC Token Crowdsale App")

# # Page 1 content
# def page1():
#     st.title("Page 1")
#     #st.write("This is the content of Page 1.")

#     # Form to deploy a new crowdsale
#     st.header("Deploy New Crowdsale")

#     token_name = st.text_input("Token Name:")
#     token_symbol = st.text_input("Token Symbol:")
#     wallet_address = st.text_input("Wallet Address:")


#     if st.button("Deploy Crowdsale"):
#         # Deploy a new crowdsale
#         try:
#             transaction_hash = deployer_contract.functions.DEPLOY(token_name, token_symbol, wallet_address).transact()
#             st.success(f"Transaction Hash: {transaction_hash.hex()}")
#         except Exception as e:
#             st.error(f"Error deploying crowdsale: {e}")


# Page 2 content
def page2():
    st.title("Page 2")
    #st.write("This is the content of Page 2.")

    # Display existing crowdsale details
    st.header("Existing Crowdsale Details")

    total_supply = deployer_contract.functions.totalSupply().call()
    st.write(f"Total Supply: {total_supply}")

    symbol = deployer_contract.functions.symbol().call()
    st.write(f"Symbol: {symbol}")

    name = deployer_contract.functions.name().call()
    st.write(f"Name: {name}")

    decimals = deployer_contract.functions.decimals().call()
    st.write(f"Desimals: {decimals}")

    accounts = w3.eth.accounts
    selected_address = st.selectbox("Select Account", options=accounts)
    Balance = deployer_contract.functions.balanceOf(selected_address).call()
    st.write(f"Balance: {Balance}")

# Page 1 content
def page3():
    st.title("Page 3")
    #st.write("This is the content of Page 3.")
    #buy = st.text_input("Buy Tokens:")
    #buytokens = deployer_contract2.functions.buyTokens(buy).call()
    #st.write(f"Buy Tokens: {buytokens}")

    # if st.button("Buy Tokens"):
    #     # Deploy the crowdsale
    #     try:
    #         transaction_hash = deployer_contract2.functions.deployNewCrowdsale(token_name, token_symbol, wallet_address).transact()
    #         st.success(f"Transaction Hash: {transaction_hash.hex()}")
    #     except Exception as e:
    #         st.error(f"Error deploying crowdsale: {e}")
    # Form to buy tokens
    st.header("Buy Tokens")

    buyer_address = st.text_input("Buyer Address:")
    buy_amount = st.text_input("Amount to Buy (in Wei):")

    if st.button("Buy Tokens"):
        # Buy tokens
        try:
            transaction_hash = deployer_contract2.functions.buyTokens(buyer_address).transact(
                {'from': buyer_address, 'value': buy_amount, 'gas': 100000}
            )
            st.success(f"Tokens Purchased. Transaction Hash: {transaction_hash.hex()}")
        except Exception as e:
            st.error(f"Error buying tokens: {e}")

    rate = deployer_contract2.functions.rate().call()
    st.write(f"Rate: {rate}")

    token = deployer_contract2.functions.token().call()
    st.write(f"Token: {token}")

    wallet = deployer_contract2.functions.wallet().call()
    st.write(f"Wallet: {wallet}")

    weiraised = deployer_contract2.functions.weiRaised().call()
    st.write(f"Wei Raised: {weiraised}")


# Main app
def main():
    # Create a navigation sidebar
    page = st.sidebar.selectbox("Go to", ["Page 1", "Page 2", "Page 3"])

    # Handle page selection
    if page == "Page 1":
        page1()
    elif page == "Page 2":
        page2()
    elif page == "Page 3":
        page3()

# Run the app
if __name__ == "__main__":
    main()