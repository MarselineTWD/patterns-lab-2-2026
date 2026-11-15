import base64
from datetime import date

from decorators import (
    Base64Decorator,
    DateDecorator,
    HeaderDecorator,
    MessageDecorator,
    SignatureDecorator,
)
from interfaces import BaseMessage
from messages import Message


def test_base_decorator_returns_message_text() -> None:
    decorated = MessageDecorator(Message("hello"))

    assert decorated.render() == "hello"
    assert isinstance(decorated, BaseMessage)


def test_header_decorator_adds_header() -> None:
    decorated = HeaderDecorator(Message("hello"), "News")

    assert decorated.render() == "News\nhello"


def test_signature_decorator_adds_signature() -> None:
    decorated = SignatureDecorator(Message("hello"), "Alice")

    assert decorated.render() == "hello\nAlice"


def test_date_decorator_adds_date() -> None:
    decorated = DateDecorator(Message("hello"), date(2026, 11, 16))

    assert decorated.render() == "hello\n2026-11-16"


def test_base64_decorator_encodes_whole_message() -> None:
    decorated = Base64Decorator(Message("привет"))
    expected = base64.b64encode("привет".encode("utf-8")).decode("ascii")

    assert decorated.render() == expected


def test_decorators_can_be_combined() -> None:
    message = Message("hello")
    message = HeaderDecorator(message, "News")
    message = SignatureDecorator(message, "Alice")
    message = DateDecorator(message, date(2026, 11, 16))

    assert message.render() == "News\nhello\nAlice\n2026-11-16"
