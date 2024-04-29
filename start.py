"""Service "toaster.comman-handling-service".
About:
    ...

Author:
    Oidaho (Ruslan Bashinskii)
    oidahomain@gmail.com
"""

import asyncio
from consumer import consumer
from handler import alert_handler
from logger import logger


async def main():
    """Entry point."""
    log_text = "Awaiting alert requests..."
    await logger.info(log_text)

    for data in consumer.listen_queue("alerts"):
        log_text = f"Recived alert request: {data}"
        await logger.info(log_text)

        await alert_handler(data)


if __name__ == "__main__":
    asyncio.run(main())
