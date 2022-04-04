"""
Cases and functions for testing the non- scraping and plotting functions in the
helpers.py file
"""
import pytest
import pandas as pd

from helpers import (
    average_data,
    clean_gdp_data,
    clean_population_data,
    merge_dataframes,
    pivot
)

clean_gdp_data_cases = [
    ("test_data/gdp_test_data1_raw.csv", "test_data/gdp_test_data1_clean.csv"),
    ("test_data/gdp_test_data2_raw.csv", "test_data/gdp_test_data2_clean.csv")
]


@pytest.mark.parametrize("raw,clean", clean_gdp_data_cases)
def test_clean_gdp_data(raw, clean):
    """
    Test the clean_gdp_data() function in helpers.py.

    Args:
        raw: the filepath for the CSV containing the test data to be cleaned.
        clean: the filepath for the CSV containing the test data correctly
            cleaned.
    """
    df_clean = pd.read_csv(clean)
    assert df_clean.equals(clean_gdp_data(raw))


clean_pop_data_cases = [
    ("test_data/pop_test_data1_raw.csv", "test_data/pop_test_data1_clean.csv"),
    ("test_data/pop_test_data2_raw.csv", "test_data/pop_test_data2_clean.csv")
]


@pytest.mark.parametrize("raw,clean", clean_pop_data_cases)
def test_clean_population_data(raw, clean):
    """
    Test the clean_population_data() function in helpers.py.

    Args:
        raw: the filepath for the CSV containing the test data to be cleaned.
        clean: the filepath for the CSV containing the test data correctly
            cleaned.
    """
    df_clean = pd.read_csv(clean)
    assert df_clean.equals(clean_population_data(raw))


def test_merge_dataframe():
    """
    Test the merge_dataframe() function in helpers.py.
    """
    # Load the correctly merged dataframe to check against
    df_merged = pd.read_csv("test_data/merge_test_data.csv")
    # Load the three test dataframes to be merged
    test_medals = pd.read_csv("test_data/medals_test_data_clean.csv")
    test_gdp = pd.read_csv("test_data/gdp_test_data1_clean.csv")
    test_pop = pd.read_csv("test_data/pop_test_data1_clean.csv")
    # Assert the merge done properly
    assert df_merged.equals(merge_dataframes(
        [test_medals, test_gdp, test_pop]))


def test_pivot():
    """
    Test the pivot() function in helpers.py.
    """
    df_clean = pd.read_csv("test_data/pivoting_test_data_clean.csv")
    df_pivot = pd.read_csv("test_data/pivoting_test_data.csv")
    df_pivot = pivot(df_pivot)
    df_pivot.to_csv("test_data/pivoting_test_data_intermediate.csv", index=False)
    df_pivot = pd.read_csv("test_data/pivoting_test_data_intermediate.csv")
    pd.testing.assert_frame_equal(df_clean, df_pivot) 


def test_average_data():
    """
    Test the average_data() function in helpers.py.
    """
    # Load the correctly averaged dataframe to check against
    df_done = pd.read_csv("test_data/averaging_test_data_done.csv")
    # Load test dataframe to be averaged
    df_raw = pd.read_csv("test_data/averaging_test_data.csv")
    # Assert the averaging done properly
    assert df_done.equals(average_data(df_raw))