from yzu_ddns_client.logger import logger
from yzu_ddns_client.providers.bunny import BunnyProvider
from yzu_ddns_client.config import Config

class ProviderManager:
    _provider = None

    @classmethod
    def setup(cls, config: Config):
        if cls._provider is not None:
            logger.warning("Provider is already initialized. Re-initializing...")

        match config.provider:
            case "bunny":
                cls._provider = BunnyProvider(config)
                logger.debug("Initialized BunnyProvider with config.")
            case _:
                logger.error("Unsupported provider: %s", config.provider)
                raise ValueError(f"Unsupported provider: {config.provider}")

    @classmethod
    def get_provider(cls):
        if cls._provider is None:
            logger.error("Provider has not been initialized. Call setup() first.")
            raise RuntimeError("Provider has not been initialized. Call setup() first.")
        return cls._provider