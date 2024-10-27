import asyncio

from service.kafka_consumer_service import KafkaConsumerService
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

# Initialise the Kafka consumer service
consumer_service = KafkaConsumerService(
    config.get("KAFKA_BROKER_URL"),
    config.get("KAFKA_GROUP_ID"),
    [config.get("KAFKA_TOPIC")]
)

# Consume messages from the Kafka topic
asyncio.run(consumer_service.consume_messages())
