import os
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import json
from streamlit import session_state

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

# Page 1 content
def page1():
    st.title("Page 1")
    #st.write("This is the content of Page 1.")

    # Form to deploy a new crowdsale
    st.header("GLOBAL COIN")
    st.image('globalcoin.png', caption=None, width=500, use_column_width=500, clamp=False, channels="RGB", output_format="auto")
    st.markdown('''
    # Welcome to Global Coin

Unlock the Power of :orange[Fungible Tokens on the Ethereum Blockchain]

Are you ready to redefine your investment journey? Introducing Global Coin, the ultimate gateway to the world of fungible tokens, where your choices are limitless and your investments are empowered.

# Why Global Coin?

Global Coin is not just a token; it's your passport to a diverse world of investment opportunities. We believe in making financial markets :orange[accessible to everyone], and with Global Coin, you can seamlessly :orange[buy tokens that represent the S&P 500, handpicked stocks, popular cryptocurrencies], or even invest in :red[cutting-edge AI trading algorithms].

# Key Features:

- :orange[Fungible Token Freedom]: Global Coin operates on the ERC-20 smart contract standard, ensuring compatibility and liquidity across a wide range of platforms. Trade, transfer, and invest with ease.

- :orange[Diverse Investment Options]: Choose from a curated selection of tokens representing renowned indices, individual stocks, cryptocurrencies, or venture into the exciting realm of algorithmic trading. Your investment, your rules.

- :orange[Transparent and Secure]: We prioritize the security of your investments. Global Coin leverages the robust security features of the Ethereum blockchain, providing transparency and peace of mind.

- :orange[Accessible to All]: Whether you're a seasoned investor or just getting started, Global Coin welcomes you. No barriers, no restrictions – just a world of possibilities at your fingertips.

# How It Works:

1. :orange[Create Your Account]: Sign up for your Global Coin account and gain access to a world of investment opportunities.

2. :orange[Explore Tokens]: Browse through our diverse selection of fungible tokens. From traditional indices to futuristic trading algorithms, there's something for every investor.

3. :orange[Buy and Trade]: Purchase tokens seamlessly using your preferred payment method. Trade on our user-friendly platform, anytime, anywhere.

4. :orange[Diversify Your Portfolio]: Tailor your investment portfolio to match your unique preferences and risk tolerance. The power to diversify is in your hands.

# Join Global Coin Today and Elevate Your Investment Experience!

Global Coin is not just about investing; it's about :orange[empowering you to shape your financial future]. Join us on this exciting journey as we redefine the way the world invests. Your financial adventure begins here at Global Coin.

Ready to start investing? Sign up now and embark on a new era of financial freedom.
    ''')

# User Login
def login():
    # Define predefined username and password
    valid_username = "user"
    valid_password = "password"

    # Input fields for username and password
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    # Check credentials on button click
    if st.button("Login"):
        if username == valid_username and password == valid_password:
            st.success("Login successful!")
            # Set login status in session state
            session_state.logged_in = True
        else:
            st.error("Invalid username or password. Please try again.")

# Page 2 content
def page2():
    st.title("Page 2")
    st.header("Existing Crowdsale Details")
    if not session_state.get('logged_in'):
        login()
    else:
        # Display existing crowdsale details
        #st.header("Existing Crowdsale Details")

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


# Page 3 content
def page3():
    st.title("Page 3")
    st.header("Buy Tokens")

    if not session_state.get('logged_in'):
        login()
    else:
        #st.header("Buy Tokens")
        selected_option = st.selectbox("Choose an option:", ["US Market", "AI Algorithm", "Specific Market"])

        # Display input fields based on the selected option
        if selected_option == "US Market":
            # Input for US Market
            us_market_input = st.text_input("Enter US Market details:")
            st.write("Selected Option: US Market")
            st.write("Input for US Market:", us_market_input)
        elif selected_option == "AI Algorithm":
            # Input for AI Algorithm
            ai_algorithm_input = st.text_input("Enter AI Algorithm details:")
            st.write("Selected Option: AI Algorithm")
            st.write("Input for AI Algorithm:", ai_algorithm_input)
        elif selected_option == "Specific Market":
            # Input for Specific Market
            specific_market_input = st.text_input("Enter Specific Market details:")
            st.write("Selected Option: Specific Market")
            st.write("Input for Specific Market:", specific_market_input)


        buyer_address = st.text_input("Buyer Address:")
        buy_amount = st.text_input("Amount to Buy (in Wei):")

        if st.button("Buy Tokens"):
            # Buy tokens
            try:
                transaction_hash = deployer_contract2.functions.buyTokens(buyer_address).transact(
                    {'from': buyer_address, 'value': buy_amount, 'gas': 3000000}
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
    elif page =="Page 4":
        page4()   

# Run the app
if __name__ == "__main__":
    main()