import asyncio

from service.broker_service import BrokerService
from service.etherscan_service import EtherscanService
from service.infura_service import InfuraService
from utils.config import Config

config = Config()

ethereum_transaction_schema = {
    "type": "record",
    "name": "EthereumTransaction",
    "fields": [
        {"name": "blockNumber", "type": "string"},
        {"name": "timeStamp", "type": "string"},
        {"name": "hash", "type": "string"},
        {"name": "nonce", "type": "string"},
        {"name": "blockHash", "type": "string"},
        {"name": "from", "type": "string"},
        {"name": "contractAddress", "type": "string"},
        {"name": "to", "type": "string"},
        {"name": "value", "type": "string"},
        {"name": "tokenName", "type": "string"},
        {"name": "tokenSymbol", "type": "string"},
        {"name": "tokenDecimal", "type": "string"},
        {"name": "transactionIndex", "type": "string"},
        {"name": "gas", "type": "string"},
        {"name": "gasPrice", "type": "string"},
        {"name": "gasUsed", "type": "string"},
        {"name": "cumulativeGasUsed", "type": "string"},
        {"name": "input", "type": "string"},
        {"name": "confirmations", "type": "string"}
    ]
}

transaction_message_schema = {
    "type": "record",
    "name": "TransactionMessage",
    "fields": [
        {
            "name": "args",
            "type": {
                "type": "record",
                "name": "Args",
                "fields": [
                    {"name": "sender", "type": "string"},
                    {"name": "recipient", "type": "string"},
                    {"name": "amount0", "type": "string"},
                    {"name": "amount1", "type": "string"},
                    {"name": "sqrtPriceX96", "type": "string"},
                    {"name": "liquidity", "type": "string"},
                    {"name": "tick", "type": "int"}
                ]
            }
        },
        {"name": "event", "type": "string"},
        {"name": "logIndex", "type": "int"},
        {"name": "transactionIndex", "type": "int"},
        {"name": "transactionHash", "type": "bytes"},
        {"name": "address", "type": "string"},
        {"name": "blockHash", "type": "bytes"},
        {"name": "blockNumber", "type": "long"}
    ]
}

# Initialising Kafka Broker service
broker_url = config.get("KAFKA_BROKER_URL")
broker_service = BrokerService(broker_url)

# Initialising Etherscan service
etherscan_api_key = config.get("ETHERSCAN_API_KEY")
etherscan_service = EtherscanService(etherscan_api_key)

# Initialising Infura service
infura_service = InfuraService(etherscan_service, broker_service, config.get("INFURA_PROJECT_ID"))

# Listen for events
asyncio.run(infura_service.listen())
