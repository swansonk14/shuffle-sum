#!/usr/bin/env python3
"""
prime_gen.py
Boucher, Govedič, Saowakon, Swanson 2019

Contains methods for generating prime numbers.

"""
from random import randint

from crypto_voting.utils import powmod


def is_prime(p: int) -> bool:
    """ Returns whether p is probably prime.

    This should run enough iterations of the test to be reasonably confident that p is prime.
    """
    for _ in range(100):
        if powmod(2, p - 1, p) != 1:
            return False
    return True


def gen_prime(b: int) -> int:
    """ Returns a prime p with b bits."""
    while True:
        p = randint(2 ** (b - 1), 2 ** b - 1)
        if is_prime(p):
            return p


def gen_safe_prime(b: int) -> int:
    """ Return a safe prime p with b bits."""
    while True:
        q = gen_prime(b - 1)
        if is_prime(q):
            p = 2 * q + 1
            if is_prime(p):
                return p


def get_order_in_safe_prime(x: int, p: int) -> int:
    """ Gets the order of x in Z_p^* where p = 2q + 1 is a safe prime.

    Note: Only possible orders are 1, 2, q, or 2q.
    """
    q = (p - 1) // 2

    # Order 1
    if powmod(x, 1, p) == 1:
        return 1

    # Order q
    if powmod(x, 2, p) == 1:
        return 2

    # Order q
    if powmod(x, q, p) == 1:
        return q

    # Order 2q
    return 2 * q


def is_quadratic_residue(x: int, p: int) -> int:
    """ Checks if x is a quadratic residue in Z_p^*.

    x must have order 1 or q (i.e. not 2 or 2q) in Z_p^* to be a quadratic residue.
    """
    q = (p - 1) // 2

    return get_order_in_safe_prime(x, p) in {1, q}


def is_quadratic_residue_generator(g: int, p: int) -> int:
    """ Checks if g is a generator of the group Q_p^* of quadratic residues of Z_p^*.

    g must have order q in Z_p^* in order for g to be a generator of Q_p^*.
    """
    q = (p - 1) // 2

    return get_order_in_safe_prime(g, p) == q


def gen_safe_prime_generator(p: int) -> int:
    """ Returns a generator of a Q_p, for a safe prime p."""
    while True:
        g = randint(2, p - 1) ** 2 % p
        if is_quadratic_residue_generator(g, p):
            return g
