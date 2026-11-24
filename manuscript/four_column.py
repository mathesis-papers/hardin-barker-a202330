import argparse
import itertools
import json
import math


def add_polynomials(*polynomials):
    return tuple(sum(polynomial[degree] for polynomial in polynomials) for degree in range(5))


def shift_polynomial(polynomial):
    return tuple(
        sum(polynomial[power] * math.comb(power, degree) for power in range(degree, 5))
        for degree in range(5)
    )


def evaluate(polynomial, argument):
    return sum(coefficient * argument**degree for degree, coefficient in enumerate(polynomial))


def compatible(first, second, third):
    return all(2 * upper + middle <= 2 * middle + lower for upper, middle, lower in zip(first, second, third))


def brute_count(height):
    count = 0
    for bits in itertools.product((0, 1), repeat=4 * height):
        if not all(
            2 * bits[4 * row + column] + bits[4 * row + column + 1]
            <= 2 * bits[4 * row + column + 1] + bits[4 * row + column + 2]
            for row in range(height)
            for column in range(2)
        ):
            continue
        if all(
            2 * bits[4 * row + column] + bits[4 * (row + 1) + column]
            <= 2 * bits[4 * (row + 1) + column] + bits[4 * (row + 2) + column]
            for row in range(height - 2)
            for column in range(4)
        ):
            count += 1
    return count


def verify(maximum_index):
    rows = [
        row
        for row in itertools.product((0, 1), repeat=4)
        if all(2 * row[column] + row[column + 1] <= 2 * row[column + 1] + row[column + 2] for column in range(2))
    ]
    assert rows == [tuple(map(int, word)) for word in ("0000", "0001", "0010", "0011", "0111", "1111")]
    states = list(itertools.product(range(6), repeat=2))
    successors = {
        (first, second): [(second, third) for third in range(6) if compatible(rows[first], rows[second], rows[third])]
        for first, second in states
    }
    zero = (0, 0, 0, 0, 0)
    polynomial_a = (48, 54, 41, 12, 1)
    polynomial_b = (24, 40, 18, 2, 0)
    polynomial_c = (24, 30, 6, 0, 0)
    polynomial_d = (24, 12, 0, 0, 0)
    polynomial_e = (12, 0, 0, 0, 0)
    vector = {}
    for first, second in states:
        if first == second == 0:
            vector[first, second] = polynomial_a
        elif second in (1, 2) and first in (0, second):
            vector[first, second] = polynomial_b
        elif second == 3 and first <= 3:
            vector[first, second] = polynomial_c
        elif second == 4 and first <= 4:
            vector[first, second] = polynomial_d
        elif second == 5:
            vector[first, second] = polynomial_e
        else:
            vector[first, second] = zero
    one_step = {state: len(successors[state]) for state in states}
    two_step = {state: sum(one_step[target] for target in successors[state]) for state in states}
    for state in states:
        assert 12 * two_step[state] == evaluate(vector[state], 2)
        assert add_polynomials(*(vector[target] for target in successors[state])) == shift_polynomial(vector[state])
    total_polynomial = add_polynomials(*vector.values())
    assert total_polynomial == shift_polynomial((156, 176, 83, 16, 1))
    counts = {1: 36}
    continuation = dict.fromkeys(states, 1)
    for index in range(2, maximum_index + 1):
        continuation = {state: sum(continuation[target] for target in successors[state]) for state in states}
        counts[index] = sum(continuation.values())
    for index, count in counts.items():
        assert 12 * count == index**4 + 16 * index**3 + 83 * index**2 + 176 * index + 156
    brute = {height: brute_count(height) for height in range(2, 5)}
    assert brute == {height: counts[height - 1] for height in range(2, 5)}
    for index in range(6, maximum_index + 1):
        assert counts[index] == 5 * counts[index - 1] - 10 * counts[index - 2] + 10 * counts[index - 3] - 5 * counts[index - 4] + counts[index - 5]
    numerator = [
        sum((-1)**lag * math.comb(5, lag) * counts.get(index - lag, 0) for lag in range(min(5, index) + 1))
        for index in range(maximum_index + 1)
    ]
    assert numerator[:6] == [0, 36, -98, 112, -61, 13]
    assert all(coefficient == 0 for coefficient in numerator[6:])
    assert sum(numerator[:6]) == 2
    return {
        "arithmetic": "exact integers",
        "horizontal_rows": ["".join(map(str, row)) for row in rows],
        "ordered_pair_states": len(states),
        "triple_predicates": 6**3,
        "initial_vector_equalities": 36,
        "polynomial_coefficient_equalities": 36 * 5,
        "sum_polynomial_coefficients": list(total_polynomial),
        "exhaustive_binary_arrays_by_height": {str(height): 2**(4 * height) for height in brute},
        "exhaustive_counts_by_height": brute,
        "dynamic_count_indices": [1, maximum_index],
        "recurrence_indices": [6, maximum_index],
        "generating_function_coefficient_indices": [0, maximum_index],
        "initial_counts": [counts[index] for index in range(1, 11)],
        "numerator_coefficients": numerator[:6],
        "numerator_at_one": 2,
        "status": "all equalities hold",
    }


def main():
    parser = argparse.ArgumentParser(description="Exact checks for four-column binary-array formulas.")
    parser.add_argument("--maximum-index", type=int, default=210)
    arguments = parser.parse_args()
    if arguments.maximum_index < 10:
        parser.error("--maximum-index must be at least 10")
    print(json.dumps(verify(arguments.maximum_index), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
