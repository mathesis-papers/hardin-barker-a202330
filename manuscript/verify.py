import itertools
import json
import math
from fractions import Fraction

import four_column


def polynomial_add(*polynomials):
    size = max(map(len, polynomials))
    result = [Fraction(0) for degree in range(size)]
    for polynomial in polynomials:
        for degree, coefficient in enumerate(polynomial):
            result[degree] += coefficient
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def polynomial_multiply(first, second):
    result = [Fraction(0) for degree in range(len(first) + len(second) - 1)]
    for first_degree, first_coefficient in enumerate(first):
        for second_degree, second_coefficient in enumerate(second):
            result[first_degree + second_degree] += first_coefficient * second_coefficient
    return polynomial_add(result)


def polynomial_scale(polynomial, factor):
    return polynomial_add([coefficient * factor for coefficient in polynomial])


def rational_add(first, second):
    first_numerator, first_denominator = first
    second_numerator, second_denominator = second
    return (
        polynomial_add(
            polynomial_multiply(first_numerator, second_denominator),
            polynomial_multiply(second_numerator, first_denominator),
        ),
        polynomial_multiply(first_denominator, second_denominator),
    )


def count_formula(height, width):
    return 2 + 2 * math.comb(height + width, height) + math.comb(height + width - 2, height - 1)


def count_polynomial(width):
    first = [Fraction(2, math.factorial(width))]
    for offset in range(2, width + 2):
        first = polynomial_multiply(first, [offset, 1])
    second = [Fraction(1, math.factorial(width - 1))]
    for offset in range(1, width):
        second = polynomial_multiply(second, [offset, 1])
    return polynomial_add([2], first, second)


def local_valid(bits):
    return all(2 * first + middle <= 2 * middle + last for first, middle, last in zip(bits, bits[1:], bits[2:]))


def transfer_counts(width, maximum_height):
    rows = [row for row in itertools.product((0, 1), repeat=width) if local_valid(row)]
    assert len(rows) == width + 2
    states = list(itertools.product(range(len(rows)), repeat=2))
    successors = {
        (first, second): [
            (second, third)
            for third in range(len(rows))
            if all(2 * upper + middle <= 2 * middle + lower for upper, middle, lower in zip(rows[first], rows[second], rows[third]))
        ]
        for first, second in states
    }
    vector = dict.fromkeys(states, 1)
    counts = {2: sum(vector.values())}
    for height in range(3, maximum_height + 1):
        vector = {state: sum(vector[next_state] for next_state in successors[state]) for state in states}
        counts[height] = sum(vector.values())
    return counts


def brute_count(height, width):
    total = 0
    for bits in itertools.product((0, 1), repeat=height * width):
        if all(local_valid(bits[row * width:(row + 1) * width]) for row in range(height)) and all(local_valid(bits[column::width]) for column in range(width)):
            total += 1
    return total


def verify_diagonal_identities():
    coefficient_lists = [
        [[-40, -13, 27], [100, 123, -135], [-20, -126, 108], [-40, 16]],
        [[8, -11, -10, 9], [-20, 13, 68, -45], [12, -2, -58, 36]],
    ]
    identity_sizes = []
    for coefficients in coefficient_lists:
        assert polynomial_add(*coefficients) == [0]
        result = ([Fraction(0)], [Fraction(1)])
        for lag, coefficient in enumerate(coefficients):
            numerator = polynomial_multiply(coefficient, [5 - 9 * lag, 9])
            denominator = [1 - lag, 1]
            for offset in range(lag):
                numerator = polynomial_multiply(numerator, [-offset, 1])
                denominator = polynomial_multiply(denominator, [-4 * offset - 2, 4])
            result = rational_add(result, (numerator, denominator))
        assert result[0] == [0]
        identity_sizes.append(len(result[1]) - 1)
    return identity_sizes


def verify():
    source_polynomials = {
        4: ['13', '44/3', '83/12', '4/3', '1/12'],
        5: ['15', '1169/60', '89/8', '3', '3/8', '1/60'],
        6: ['17', '295/12', '5779/360', '16/3', '17/18', '1/12', '1/360'],
        7: ['19', '4191/140', '974/45', '5999/720', '265/144', '167/720', '11/720', '1/2520'],
        8: ['21', '1243/35', '140383/5040', '1439/120', '8927/2880', '59/120', '67/1440', '1/420', '1/20160'],
    }
    source_numerators = {
        4: [36, -98, 112, -61, 13],
        5: [49, -165, 250, -203, 86, -15],
        6: [64, -257, 485, -523, 331, -115, 17],
        7: [81, -378, 854, -1148, 966, -502, 148, -19],
        8: [100, -532, 1400, -2254, 2366, -1636, 722, -185, 21],
    }
    grid = []
    for width in range(2, 9):
        counts = transfer_counts(width, 14)
        for height, observed in counts.items():
            assert observed == count_formula(height, width)
            assert observed == count_formula(width, height)
            grid.append([height, width, observed])
    exhaustive = []
    for height in range(2, 5):
        for width in range(2, 5):
            observed = brute_count(height, width)
            assert observed == count_formula(height, width)
            exhaustive.append([height, width, observed])
    for width, coefficients in source_polynomials.items():
        assert count_polynomial(width) == list(map(Fraction, coefficients))
        counts = [0] + [count_formula(index + 1, width) for index in range(1, 211)]
        numerator = [
            sum((-1)**lag * math.comb(width + 1, lag) * counts[index - lag] for lag in range(min(index, width + 1) + 1))
            for index in range(len(counts))
        ]
        assert numerator == [0] + source_numerators[width] + [0] * (209 - width)
        assert sum(source_numerators[width]) == 2
    diagonal_degrees = verify_diagonal_identities()
    for index in range(1, 211):
        central = math.comb(2 * index, index)
        assert Fraction(9 * index + 5, index + 1) * central + 2 == count_formula(index + 1, index + 1)
        assert count_formula(index + 1, 2) == (index + 3)**2
        assert count_formula(index + 1, 3) == Fraction(2 * index**3 + 21 * index**2 + 61 * index + 66, 6)
    permutation_maxima = []
    cyclic_values = [0, 1] + [(2 * order**3 + 3 * order**2 - 11 * order + 18) // 6 for order in range(2, 211)]
    cyclic_numerator = [sum((-1)**lag * math.comb(4, lag) * cyclic_values[index - lag] for lag in range(min(index, 4) + 1)) for index in range(len(cyclic_values))]
    assert cyclic_numerator == [0, 1, 0, 1, 1, -1] + [0] * 205
    for order in range(2, 9):
        observed = max(sum(permutation[position] * permutation[(position + 1) % order] for position in range(order)) for permutation in itertools.permutations(range(1, order + 1)))
        assert observed == (2 * order**3 + 3 * order**2 - 11 * order + 18) // 6
        permutation_maxima.append([order, observed])
    return {
        'status': 'all equalities hold',
        'arithmetic': 'exact integers and rational polynomial coefficients',
        'arbitrary_width_transfer_grid': {'heights': [2, 14], 'widths': [2, 8], 'equalities': len(grid)},
        'exhaustive_binary_array_counts': exhaustive,
        'source_polynomial_widths': list(source_polynomials),
        'source_generating_function_indices': [0, 210],
        'fixed_width_minimality_certificate': 'each numerator at one equals 2',
        'diagonal_rational_identity_denominator_degrees': diagonal_degrees,
        'diagonal_and_column_formula_indices': [1, 210],
        'exhaustive_cyclic_permutation_maxima': permutation_maxima,
        'cyclic_product_generating_function_indices': [0, 210],
        'four_column_continuation_identity': four_column.verify(210),
    }


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2, sort_keys=True))
