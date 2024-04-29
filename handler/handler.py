from vk_api import VkApiError
from logger import logger
from db import db
from .abc import ABCHandler


class AlertHandler(ABCHandler):
    """Event handler class that recognizes commands
    in the message and executing attached to each command
    actions.
    """

    async def _handle(self, event: dict, kwargs) -> bool:
        try:
            log_chats = await self._get_log_chats()

            alert_type = event.get("alert_type")
            if alert_type == "command":
                message_text = (
                    f"{self._tag(event, 'user')} вызвал команду. \n"
                    f"Команда: /\"{event.get('command_name')}\" \n"
                    f"Беседа: {event.get('peer_name')} \n"
                )

            elif alert_type == "warn":
                message_text = (
                    f"{self._tag(event, 'user')} был предупрежден. \n"
                    f"Инициатор: {self._tag(event, 'moderator')} \n"
                    f"Получено предупреждений: {event.get('wanrs')} \n"
                    f"Всего предупреждений: {event.get('total_warns')} \n"
                    f"Беседа: {event.get('peer_name')} \n"
                )

            elif alert_type == "unwarn":
                message_text = (
                    f"{self._tag(event, 'user')} был амнистирован.\n"
                    f"Инициатор: {self._tag(event, 'moderator')} \n"
                    f"Снято предупреждений: {event.get('wanrs')}\n"
                    f"Всего предупреждений: {event.get('total_warns')} \n"
                    f"Беседа: {event.get('peer_name')} \n"
                )

            elif alert_type == "kick":
                message_text = (
                    f"{self._tag(event, 'user')} итсключен из беседы. \n"
                    f"Инициатор: {self._tag(event, 'moderator')} \n"
                    f"Беседа: {event.get('peer_name')} \n"
                )

            self.api.messages.send(
                peer_ids=log_chats,
                random_id=0,
                message=message_text,
                forward=event.get("forward"),
            )
            log_text = "Alert sent."
            await logger.info(log_text)
            return True

        except VkApiError:
            return False

    @staticmethod
    async def _get_log_chats() -> str:
        peer_ids = db.execute.select(
            schema="toaster",
            table="conversations",
            fields=("conv_id",),
            conv_mark="LOG",
        )
        result = [str(peer_id[0]) for peer_id in peer_ids]
        return ", ".join(result)

    @staticmethod
    def _tag(event: dict, entity: str):
        entity_name = entity + "_name"
        entity_id = entity + "_id"

        return f"[id{event.get(entity_id)}|{event.get(entity_name)}]"


alert_handler = AlertHandler()
