import pytest
import pandas as pd

from helpers import (
    clean_medal_data
)

clean_medal_data_cases = [

]


# @pytest.mark.parametrize("nucleotide,complement", clean_medal_data_cases)
# def test_clean_medal_data(nucleotide, complement):
#     """
#     Test that each nucleotide is mapped to its correct complement.
#     Given a single-character string representing a nucleotide that is "A", "T",
#     "G", or "C", check that the get_complement function correctly maps the
#     string to a single-character string representing the nucleotide's complement
#     (also "A", "T", "G", or "C").
#     Args:
#         nucleotide: A single-character string equal to "A", "C", "T", or "G"
#             representing a nucleotide.
#         complement: A single-character string equal to "A", "C", "T", or "G"
#             representing the expected complement of nucleotide.
#     """
#     assert clean_medal_data(nucleotide) == complement