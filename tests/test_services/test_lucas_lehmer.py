import pytest
from hypothesis import given, strategies as st
from sympy import isprime

from mersenne.services.lucas_lehmer import LucasLehmer, is_mersenne_prime

# Exponents p where M_p = 2^p - 1 is a known Mersenne prime.
PRIME_EXPONENTS = [3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127]

# Odd primes p where M_p is composite (so the test must return False).
COMPOSITE_EXPONENTS = [11, 23, 29, 37, 41, 43, 47]

# Odd primes used to cross-check against a trusted primality oracle.
ODD_PRIMES = [p for p in range(3, 128) if isprime(p)]


@pytest.mark.parametrize("p", PRIME_EXPONENTS)
def test_detects_mersenne_primes(p: int) -> None:
    assert LucasLehmer(p).test() is True


@pytest.mark.parametrize("p", COMPOSITE_EXPONENTS)
def test_rejects_composite_mersenne_numbers(p: int) -> None:
    assert LucasLehmer(p).test() is False


@pytest.mark.parametrize("p", [2, 1, 0, -1])
def test_rejects_exponents_below_domain(p: int) -> None:
    # The test is defined for p >= 3; p = 2 (and anything lower) is out of
    # domain and must be rejected rather than silently mis-classified.
    with pytest.raises(ValueError):
        LucasLehmer(p)


@given(p=st.sampled_from(ODD_PRIMES))
def test_agrees_with_reference_primality(p: int) -> None:
    assert LucasLehmer(p).test() == isprime(2**p - 1)


@pytest.mark.parametrize(
    "p,expected",
    [(p, True) for p in PRIME_EXPONENTS[:4]]
    + [(p, False) for p in COMPOSITE_EXPONENTS[:3]],
)
def test_is_mersenne_prime_correctness(p: int, expected: bool) -> None:
    # The cached function must agree with a fresh LucasLehmer instance on both
    # prime and composite exponents.
    assert is_mersenne_prime(p) == LucasLehmer(p).test()
    assert is_mersenne_prime(p) is expected


def test_is_mersenne_prime_memoizes() -> None:
    is_mersenne_prime.cache_clear()
    is_mersenne_prime(31)
    is_mersenne_prime(31)
    info = is_mersenne_prime.cache_info()
    assert info.misses == 1
    assert info.hits == 1
