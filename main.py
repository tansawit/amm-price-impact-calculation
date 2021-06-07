import json
import requests
from web3 import Web3

web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/394ff03e59644af0a007bed4cdc414d4"))

uniswap_router_address = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
uniswap_router_abi_file = open("abis/UniswapV2Router02.json")
uniswap_router_abi = json.load(uniswap_router_abi_file)

erc20_router_abi_file = open("abis/ERC20.json")
erc20_router_abi = json.load(erc20_router_abi_file)

usdt_address = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
usdt_contract = web3.eth.contract(address=usdt_address, abi=erc20_router_abi)
usdt_decimals = usdt_contract.functions.decimals().call()

weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
weth_contract = web3.eth.contract(address=weth_address, abi=erc20_router_abi)
weth_decimals = weth_contract.functions.decimals().call()

# swapping 10K ETH to USDT
path = [weth_address, usdt_address]
amount_in = 10000

# get expected output in case of perfect price swap
band_enpoint = "https://asia-rpc.bandchain.org/oracle/request_prices"
payload = {"symbols": ["ETH"], "min_count": 10, "ask_count": 16}
response = requests.request("POST", band_enpoint, json=payload).json()
eth_price = int(response["result"][0]["px"]) / 1e9
expected_amount_out = eth_price * amount_in

# get actual estimate output from a swap
uniswap_router_contract = web3.eth.contract(address=uniswap_router_address, abi=uniswap_router_abi)
actual_amount_out = uniswap_router_contract.functions.getAmountsOut(amount_in * 10 ** weth_decimals, path).call()[
    1
] / (10 ** usdt_decimals)

print(f"swapping {amount_in} ETH to USDT")
print(f"expected (perfect) amount out: {expected_amount_out} USDT")
print(f"actual estimated amount out: {actual_amount_out} USDT")
print(f"price impact: {(actual_amount_out-expected_amount_out)/expected_amount_out*100}%")
