class EthUtil:
    @staticmethod
    def gas_to_eth(gas_used: int, gas_price: int):
        """
        Convert gas used and gas price to ETH.

        Args:
            gas_used (int): The amount of gas used.
            gas_price (int): The price of gas in GWEI.

        Returns:
            float: The amount of ETH spent.
        """
        return (gas_used * gas_price) / 1e18
