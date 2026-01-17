import pandas as pd
from datacure.validate_numeric_column  import validate_numeric_column  # adjust import if needed

df = pd.DataFrame({
    "age": [25, -3, 200, None, 40],
    "price": [1000, 0, -50, 5000, 999999],
    "qty": [1, 2, 3, 4, -1],
    "name": ["Alice", "Bob", "Chris", "Dora", "Eve"]
})

print(df)


violations_age = validate_numeric_column(
    df, column="age", min_value=0, max_value=120, allow_negative=False
)
print("\nAGE VIOLATIONS:")
print(violations_age)


violations_qty = validate_numeric_column(
    df, column="qty", allow_negative=False
)
print("\nQTY VIOLATIONS:")
print(violations_qty)


violations_qty = validate_numeric_column(
    df, column="qty", allow_negative=False
)
print("\nQTY VIOLATIONS:")
print(violations_qty)
