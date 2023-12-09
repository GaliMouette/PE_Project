from random import randint


class Register:
    def __init__(self, reg: int) -> None:
        self.rx = reg

    def __str__(self) -> str:
        return f"r{self.rx}"

    def __eq__(self, __value: object) -> bool:
        if __value is None:
            return False
        elif not isinstance(__value, Register):
            return False
        else:
            return self.rx == __value.rx


class WriteRegister(Register):
    def __init__(self) -> None:
        super().__init__(randint(0, 28))


class ReadRegister(Register):
    def __init__(self) -> None:
        super().__init__(randint(0, 31))
