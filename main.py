#!/usr/bin/env python3

from simulator import Simulator


if __name__ == "__main__":
    s = Simulator(10, False)
    s.run()
    s.display_stats()
