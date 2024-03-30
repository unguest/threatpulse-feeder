from socket import inet_aton, error


def validate_ip(s: str) -> bool:
    try:
        inet_aton(s)
        return True
    except error:
        return False
