"""Generates possible intermediate gear ratios.

Ratios are based on an specified overall ratio, a maximum tooth count, number of
 stages, and minimum and maximum individual ratios.
"""

import sympy as sp
from itertools import product, combinations_with_replacement as cwr

total_ratio = sp.Rational(130, 1750, gcd=1)  # Total / overall ratio.
stages = 3
max_tooth_count = 100  # To keep gear sizes small.

min_stage_ratio = sp.Rational(1, 5)
max_stage_ratio = sp.Rational(1, 1)

# Get all factors of the numerator and denominator of the total ratio.
factors = {*sp.divisors(total_ratio.numerator),
           *sp.divisors(total_ratio.denominator)}

# Eliminate factors that are greater than the maximum tooth count.
useable_factors = {factor for factor in factors
                   if factor <= max_tooth_count}

# Combine the factors into all possible gear ratios within the ratio limits.
possible_stage_ratios = {sp.Rational(n, d) for n in useable_factors
                         for d in useable_factors
                         if min_stage_ratio <= sp.Rational(n, d) <= max_stage_ratio}

# Find all possible combinations of the stage ratios that achieve the total ratio.
# Also keep the gear train ratios in (min, mid, max) order.
possible_combination_ratios = {tuple(sorted(ratios)) for ratios in
                               cwr(possible_stage_ratios, stages)
                               if ratios[0] * ratios[1] * ratios[2]
                               == sp.Rational(total_ratio.numerator, 
                                              total_ratio.denominator)}

# Sort the combinations by the range of the ratios.
sorted_by_max_difference = sorted(possible_combination_ratios, 
                                  key=lambda x: x[2] - x[0])

print(*sorted_by_max_difference, sep="\n")
