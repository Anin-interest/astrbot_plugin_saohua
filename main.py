from pathlib import Path

from astrbot import logger
from astrbot.api.event import filter
from astrbot.api.star import Context, Star, register
from astrbot.core import AstrBotConfig
from astrbot.core.platform import AstrMessageEvent

import astrbot.core.message.components as Comp
from astrbot.core.star.filter.event_message_type import EventMessageType

import yaml
import random


@register(
    "astrbot_plugin_reply",
    "安音Anin",
    "根据特定内容回复",
    "1.0.0",
    "",
)
class ReplyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.replys: dict = {}
        self.reply_keys: list = []
        with open(Path(__file__).parent / "resources/reply.yaml", "r", encoding="utf-8") as f:
            self.replys = yaml.safe_load(f)
            self.reply_keys = self.replys.keys()
            f.close()

    @filter.event_message_type(EventMessageType.ALL)
    async def reply_handle(self, event: AstrMessageEvent):
        """
        根据特定内容回复
        """
        messages = event.get_messages()
        reply_msgs : list = []
        for seg in messages:
            if isinstance(seg, Comp.Plain):
                text = seg.text.strip()
                reply_msgs.extend(self.search(text))
        if reply_msgs:
            # 回复消息
            yield event.plain_result(reply_msgs[random.randint(0, len(reply_msgs) - 1)])

    async def search(self, text: str) -> list:
        """
        搜索文本是否在keys中，并返回对应的回复消息
        """
        result = []
        for key in self.reply_keys:
            if key in text:
                result.extend(self.replys[key])
        return result

