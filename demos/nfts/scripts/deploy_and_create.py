from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import AdvancedCollectable

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"


def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectable.deploy({"from": account})


def main():
    deploy_and_create()


def mint():
    
