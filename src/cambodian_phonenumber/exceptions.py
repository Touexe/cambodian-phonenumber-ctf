class InvalidPhoneNumber(ValueError):
    """The provided string is not a valid phone number."""

    def __init__(self) -> None:
        super().__init__("Invalid Cambodian phone number")


class BadPrefix(InvalidPhoneNumber):
    """The prefix does not belong to any known Cambodian carrier."""

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix
        super().__init__()
        self.args = (f"Unknown prefix '{prefix}': not a recognized Cambodian carrier prefix",)


class BadLength(InvalidPhoneNumber):
    """The number has an incorrect digit count for its prefix."""

    def __init__(self, prefix: str, required_length: int, given_length: int) -> None:
        self.prefix = prefix
        self.required_length = required_length
        self.given_length = given_length
        super().__init__()
        self.args = (
            f"Bad length for prefix '{prefix}': "
            f"expected {required_length} digits, got {given_length}",
        )
