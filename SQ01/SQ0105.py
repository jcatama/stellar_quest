import requests
from stellar_sdk import Server, Keypair, Network, TransactionBuilder, Asset

server = Server("https://horizon-testnet.stellar.org")
source = Keypair.from_secret("[QUEST_SECRET]")
source_account = server.load_account(source.public_key)

random_keypair = Keypair.random()

response = requests.get(
    "https://friendbot.stellar.org",
    params={'addr': random_keypair.public_key}
)

asset = Asset("jcatama", random_keypair.public_key)

transaction = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_change_trust_op(
        asset=asset
    )
    .build()
)
transaction.sign(source.secret)
response = server.submit_transaction(transaction)

issuer = server.load_account(random_keypair.public_key)
transaction = (
    TransactionBuilder(
        source_account=issuer,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_payment_op(
        destination=source.public_key,
        amount="69",
        asset=asset
    )
    .build()
)

transaction.sign(random_keypair.secret)
response = server.submit_transaction(transaction)

if response:
    print(response)
else:
    print("Failed")
