import pytest
import pandas as pd

from helpers import (
    clean_medal_data
)

clean_medal_data_cases = [
    "test_data/medals_original.csv", "test_data/medals_cleaned.csv"
]


@pytest.mark.parametrize("raw,cleaned", clean_medal_data_cases)
def test_clean_medal_data(raw, cleaned):
   df_raw = pd.read_csv(raw)
   df_cleaned = pd.read_csv(cleaned)
   assert df_cleaned.equals(clean_medal_data(df_raw))


   # try assert_frame_equal