from functools import lru_cache


class LucasLehmer:
    """
    The Mersenne number Mp is prime if and only if the Lucas-Lehmer residue of Mp is equal to zero.

    The test is defined for exponents p >= 3 (conventionally an odd prime), and the
    biconditional holds across that whole domain. p = 2 is outside it: M_2 = 3 is prime,
    but the recurrence tests s_0 = 4 against M_2 = 3 and would report composite, so the
    exponent is rejected rather than special-cased.
    """

    def __init__(self, mersenne_index: int, s1: int = 4) -> None:
        if mersenne_index < 3:
            raise ValueError(
                f"Lucas-Lehmer is defined for exponents p >= 3, got {mersenne_index}."
            )

        self.mersenne_index = mersenne_index
        self.mersenne_number = 2**mersenne_index - 1

        # Test defaults
        self.s1 = s1

    def test(self) -> bool:
        s = self.s1
        for _ in range(self.mersenne_index - 2):
            s = (s * s - 2) % self.mersenne_number
        return s % self.mersenne_number == 0


@lru_cache(maxsize=4096)
def is_mersenne_prime(p: int) -> bool:
    """Cached Lucas-Lehmer primality test for M_p = 2**p - 1.

    The result is deterministic in p, so memoizing it lets repeated requests
    skip the CPU-bound recurrence. Keyed on p only (the seed is always the
    standard 4).
    """
    return LucasLehmer(p).test()
