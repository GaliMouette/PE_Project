from random import choice
from enum import Enum
from typing import List
from instruction import AL, ALI, L, S, J, CB, NOP, Instruction


class Stage(Enum):
    FETCH = 0
    DECODE = 1
    EXECUTE = 2
    MEMORY = 3
    WRITE_BACK = 4
    NB_STAGES = 5


class Simulator:
    def __init__(self, n: int, with_branch_prediction: bool) -> None:
        self.n = n
        self.instructions = [
            choice([AL(), ALI(), L(), S(), J(), CB()]) for _ in range(n)
        ]
        self.pipeline: List[Instruction] = [NOP() for _ in range(Stage.NB_STAGES.value)]

        self.nb_added_cycles = 0
        self.nb_rw_conflict = 0
        self.nb_mem_conflict = 0
        self.nb_pc_conflict = 0
        self.nb_wrong_predictions = 0

        self.with_branch_prediction = with_branch_prediction

    def move_instruction_trough_pipeline(
        self, start: Stage, stop: Stage, to_insert: Instruction
    ) -> None:
        for i in range(start.value, stop.value, -1):
            self.pipeline[i] = self.pipeline[i - 1]
        self.pipeline[stop.value] = to_insert

    def step_no_bubble(self):
        self.move_instruction_trough_pipeline(
            Stage.WRITE_BACK, Stage.FETCH, self.instructions.pop(0)
        )

    def step_insert_bubble_fetch(self):
        self.move_instruction_trough_pipeline(Stage.WRITE_BACK, Stage.FETCH, NOP())
        self.nb_added_cycles += 1

    def step_insert_bubble_execute(self):
        self.move_instruction_trough_pipeline(Stage.WRITE_BACK, Stage.EXECUTE, NOP())
        self.nb_added_cycles += 1

    def step_insert_bubble_decode(self):
        self.move_instruction_trough_pipeline(Stage.WRITE_BACK, Stage.DECODE, NOP())
        self.nb_added_cycles += 1

    def read_after_write_conflict(self):
        writes = [
            w.rx
            for w in [
                self.pipeline[Stage.EXECUTE.value].rd,
                self.pipeline[Stage.MEMORY.value].rd,
            ]
            if w is not None
        ]
        decode = self.pipeline[Stage.DECODE.value]
        reads = [r.rx for r in [decode.rs1, decode.rs2] if r is not None]
        conflicts = [read in writes for read in reads]
        if any(conflicts):
            self.nb_rw_conflict += 1
            return True
        return False

    def memory_access_conflict(self):
        execute = self.pipeline[Stage.EXECUTE.value]
        if isinstance(execute, L) or isinstance(execute, S):
            self.nb_mem_conflict += 1
            return True
        return False

    def pc_conflict(self):
        fetch = self.pipeline[Stage.FETCH.value]
        if self.with_branch_prediction:
            if isinstance(fetch, J):
                self.nb_pc_conflict += 1
                return True
        else:
            if isinstance(fetch, J) or isinstance(fetch, CB):
                self.nb_pc_conflict += 1
                return True
        return False

    def branch_wrongly_predicted(self):
        decode = self.pipeline[Stage.DECODE.value]
        if isinstance(decode, CB):
            prediction = choice([True, False])
            self.nb_wrong_predictions += prediction
            return prediction
        return False

    def step(self):
        if self.read_after_write_conflict():
            self.step_insert_bubble_execute()
        elif self.with_branch_prediction and self.branch_wrongly_predicted():
            self.step_insert_bubble_decode()
        elif self.memory_access_conflict():
            self.step_insert_bubble_fetch()
        elif self.pc_conflict():
            self.step_insert_bubble_fetch()
        else:
            self.step_no_bubble()

    def display_stats(self):
        print(f"Running with branch prediction: {self.with_branch_prediction}")
        print(f"Number of cycles: {self.nb_added_cycles + self.n}")
        print(f"Number of bubbles: {self.nb_added_cycles}")
        print(f"Number of RW conflicts: {self.nb_rw_conflict}")
        print(f"Number of MEM conflicts: {self.nb_mem_conflict}")
        print(f"Number of PC conflicts: {self.nb_pc_conflict}")
        print(f"Number of wrong predictions: {self.nb_wrong_predictions}")
        print(f"IPC: {self.n / (self.nb_added_cycles + self.n):.2f}")

    def run(self):
        while self.instructions:
            self.step()
