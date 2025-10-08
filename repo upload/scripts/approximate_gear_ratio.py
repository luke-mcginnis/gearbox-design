"""Generates possible intermediate gear ratios.

Ratios are based on an specified overall ratio, a maximum tooth count and a
number of stages. Generates stage ratios where all stages are identical to
minimize total package size.
"""

from fractions import Fraction
import pandas as pd

input_speed = 1750 # rpm
target_output_speed = 130 # rpm
number_of_stages = 3
maximum_tooth_count = 150

target_ratio = Fraction(target_output_speed, input_speed)
target_stage_ratio = Fraction(target_ratio ** (1/number_of_stages))

ratios = []
max_denominator = maximum_tooth_count

# Iteratively reduce denominator until all close ratios are found.
while max_denominator > 1:
    stage_ratio = target_stage_ratio.limit_denominator(max_denominator)
    ratios.append(stage_ratio)
    max_denominator = stage_ratio.denominator - 1

# Store data in Dataframe.
df = pd.DataFrame({"Stage Ratio": ratios})
df["Overall Train Value"] = df["Stage Ratio"].astype(float) ** 3 
df["Output Speed (rpm)"] = df["Overall Train Value"] * input_speed
df["Output Speed Error (rpm)"] = (df["Output Speed (rpm)"] - target_output_speed).abs()
