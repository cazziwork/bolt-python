from typing import Optional, List, Union, Dict

from slack_sdk import WebClient
from slack_sdk.models.attachments import Attachment
from slack_sdk.models.blocks import Block
from slack_sdk.web import SlackResponse

from slack_bolt.context.say.internals import _can_say


class Say:
    client: Optional[WebClient]
    channel: Optional[str]

    def __init__(
        self, client: Optional[WebClient], channel: Optional[str],
    ):
        self.client = client
        self.channel = channel

    def __call__(
        self,
        text: Union[str, dict] = "",
        blocks: Optional[List[Union[Dict, Block]]] = None,
        attachments: Optional[List[Union[Dict, Attachment]]] = None,
        channel: Optional[str] = None,
        thread_ts: Optional[str] = None,
        **kwargs,
    ) -> SlackResponse:
        if _can_say(self, channel):
            text_or_whole_response: Union[str, dict] = text
            if isinstance(text_or_whole_response, str):
                text = text_or_whole_response
                return self.client.chat_postMessage(
                    channel=channel or self.channel,
                    text=text,
                    blocks=blocks,
                    attachments=attachments,
                    thread_ts=thread_ts,
                    **kwargs,
                )
            elif isinstance(text_or_whole_response, dict):
                message: dict = text_or_whole_response
                if "channel" not in message:
                    message["channel"] = channel or self.channel
                return self.client.chat_postMessage(**message)
            else:
                raise ValueError(
                    f"The arg is unexpected type ({type(text_or_whole_response)})"
                )
        else:
            raise ValueError("say without channel_id here is unsupported")
