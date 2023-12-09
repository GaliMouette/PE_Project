from register import WriteRegister, ReadRegister


class Instruction:
    def __init__(
        self,
        op: str,
        rd: WriteRegister | None,
        rs1: ReadRegister | None,
        rs2: ReadRegister | None,
    ):
        self.op = op
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2

    def __str__(self) -> str:
        return f"{self.op} {self.rd}, {self.rs1}, {self.rs2}"


class AL(Instruction):
    def __init__(self) -> None:
        super().__init__("AL", WriteRegister(), ReadRegister(), ReadRegister())


class ALI(Instruction):
    def __init__(self) -> None:
        super().__init__("ALI", WriteRegister(), ReadRegister(), None)


class L(Instruction):
    def __init__(self) -> None:
        super().__init__("L", WriteRegister(), ReadRegister(), None)


class S(Instruction):
    def __init__(self) -> None:
        super().__init__("S", None, ReadRegister(), ReadRegister())


class J(Instruction):
    def __init__(self) -> None:
        super().__init__("J", None, ReadRegister(), ReadRegister())


class CB(Instruction):
    def __init__(self) -> None:
        super().__init__("CB", None, ReadRegister(), ReadRegister())


class NOP(Instruction):
    def __init__(self) -> None:
        super().__init__("NOP", None, None, None)
