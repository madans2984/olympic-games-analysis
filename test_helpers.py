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
    df_clean = pd.read_csv(clean)
    assert df_clean.equals(clean_gdp_data(raw))


clean_pop_data_cases = [
    ("test_data/pop_test_data1_raw.csv", "test_data/pop_test_data1_clean.csv"),
    ("test_data/pop_test_data2_raw.csv", "test_data/pop_test_data2_clean.csv")
]


@pytest.mark.parametrize("raw,clean", clean_pop_data_cases)
def test_clean_population_data(raw, clean):
    df_clean = pd.read_csv(clean)
    assert df_clean.equals(clean_population_data(raw))


def test_merge_dataframe():
    df_merged = pd.read_csv("test_data/merge_test_data.csv")
    test_medals = pd.read_csv("test_data/medals_test_data_clean.csv")
    test_gdp = pd.read_csv("test_data/gdp_test_data1_clean.csv")
    test_pop = pd.read_csv("test_data/pop_test_data1_clean.csv")
    assert df_merged.equals(merge_dataframes(
        [test_medals, test_gdp, test_pop]))

def test_pivot():
    df_clean = pd.read_csv("test_data/pivoting_test_data_clean.csv")
    df_pivot = pd.read_csv("test_data/pivoting_test_data.csv")
    df_pivot = pivot(df_pivot)
    print(df_pivot)
    print(df_clean)
    assert df_clean.equals(df_pivot)

def test_average():
    df_clean = pd.read_csv("test_data/averaging_test_data_clean.csv")
    df_average = pd.read_csv("test_data/averaging_test_data.csv")
    assert df_clean.equals(average_data(df_average))
