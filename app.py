from decorators import DateDecorator, HeaderDecorator, SignatureDecorator
from messages import Message
from proxies import ProtectedMessageProxy
from security import AccessPolicy, UserContext


def main() -> None:
    message = Message("С наступающим Новым годом!")
    message = HeaderDecorator(message, "=== Поздравление ===")
    message = SignatureDecorator(message, "С уважением, учебная группа")
    message = DateDecorator(message)

    policy = AccessPolicy("reader")
    reader = UserContext.of("alice", "reader")
    guest = UserContext.of("bob", "guest")

    allowed_message = ProtectedMessageProxy(message, reader, policy)
    print("Успешный доступ:")
    print(allowed_message.render())

    denied_message = ProtectedMessageProxy(message, guest, policy)
    print("\nОтказ в доступе:")
    try:
        print(denied_message.render())
    except PermissionError as error:
        print(error)


if __name__ == "__main__":
    main()
