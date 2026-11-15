import base64
from datetime import date

from interfaces import BaseMessage


class MessageDecorator(BaseMessage):
    """Базовый декоратор, который хранит другое сообщение."""

    def __init__(self, message: BaseMessage) -> None:
        self._message = message

    def render(self) -> str:
        return self._message.render()


class HeaderDecorator(MessageDecorator):
    def __init__(self, message: BaseMessage, header: str) -> None:
        super().__init__(message)
        self._header = header

    def render(self) -> str:
        return f"{self._header}\n{super().render()}"


class SignatureDecorator(MessageDecorator):
    def __init__(self, message: BaseMessage, signature: str) -> None:
        super().__init__(message)
        self._signature = signature

    def render(self) -> str:
        return f"{super().render()}\n{self._signature}"


class DateDecorator(MessageDecorator):
    def __init__(self, message: BaseMessage, value: date | None = None) -> None:
        super().__init__(message)
        self._date = value if value is not None else date.today()

    def render(self) -> str:
        return f"{super().render()}\n{self._date.isoformat()}"


class Base64Decorator(MessageDecorator):
    def render(self) -> str:
        text = super().render()
        encoded = base64.b64encode(text.encode("utf-8"))
        return encoded.decode("ascii")
