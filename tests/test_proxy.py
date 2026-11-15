import pytest

from interfaces import BaseMessage
from messages import Message
from proxies import ProtectedMessageProxy
from security import AccessPolicy, UserContext


def test_proxy_allows_user_with_required_role() -> None:
    proxy = ProtectedMessageProxy(
        Message("secret"),
        UserContext.of("alice", "reader"),
        AccessPolicy("reader"),
    )

    assert proxy.render() == "secret"
    assert isinstance(proxy, BaseMessage)


def test_proxy_denies_user_without_required_role() -> None:
    proxy = ProtectedMessageProxy(
        Message("secret"),
        UserContext.of("bob", "guest"),
        AccessPolicy("reader"),
    )

    with pytest.raises(PermissionError):
        proxy.render()
