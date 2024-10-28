import asyncio

from service.binance_service import BinanceService
from service.broker_service import BrokerService
from service.etherscan_service import EtherscanService
from service.infura_service import InfuraService
from utils.config import Config

config = Config()

# Initialising Binance service
binance_service = BinanceService()

# Initialising Kafka Broker service
broker_url = config.get("KAFKA_BROKER_URL")
broker_service = BrokerService(broker_url)

# Initialising Etherscan service
etherscan_api_key = config.get("ETHERSCAN_API_KEY")
etherscan_service = EtherscanService(etherscan_api_key)

# Initialising Infura service
infura_service = InfuraService(
    etherscan_service,
    broker_service,
    binance_service,
    config.get("INFURA_PROJECT_ID")
)

# Listen for events
asyncio.run(infura_service.listen())
