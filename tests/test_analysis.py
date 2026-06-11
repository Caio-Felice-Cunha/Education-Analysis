"""Smoke tests for the Education Analysis datasets and headline metrics.

These tests recompute the numbers quoted in the README straight from the CSV
files, so a future pandas upgrade or a data change that breaks the pipeline is
caught here instead of silently producing wrong figures.

They also exercise the column-selected groupby aggregation
(df.groupby(key)[col].mean()) that the notebook depends on. The older
whole-frame form (df.groupby(key).mean()[col]) raises TypeError on pandas 2.0
and later because it tries to average non-numeric columns.

Run from the repo root:
    pip install -r requirements.txt pytest
    pytest
"""

from pathlib import Path

import pandas as pd
import pytest

DATA_DIR = Path(__file__).resolve().parent.parent / "datasets"
PASS_GRADE = 70


@pytest.fixture(scope="module")
def students():
    return pd.read_csv(DATA_DIR / "students_dataset.csv")


@pytest.fixture(scope="module")
def schools():
    return pd.read_csv(DATA_DIR / "schools_dataset.csv")


@pytest.fixture(scope="module")
def full_data(students, schools):
    return pd.merge(students, schools, how="left", on="Name_School")


def test_scale(students, schools):
    assert len(schools) == 15
    assert (schools["Type_School"] == "Private").sum() == 8
    assert (schools["Type_School"] == "Public").sum() == 7
    assert len(students) == 39160
    assert int(schools["Annual_Budget"].sum()) == 24649428


def test_merge_shape(full_data):
    # left merge must not duplicate rows and adds the 4 school columns
    assert full_data.shape == (39160, 11)


def test_overall_averages(full_data):
    assert round(full_data["Writing_Grade"].mean(), 2) == 81.88
    assert round(full_data["Math_Grade"].mean(), 2) == 78.98


def test_approval_counts(full_data):
    total = len(full_data)
    writing = (full_data["Writing_Grade"] >= PASS_GRADE).sum()
    math = (full_data["Math_Grade"] >= PASS_GRADE).sum()
    both = (
        (full_data["Writing_Grade"] >= PASS_GRADE)
        & (full_data["Math_Grade"] >= PASS_GRADE)
    ).sum()
    assert int(writing) == 33600
    assert int(math) == 29360
    assert int(both) == 25518
    assert round(writing / total * 100, 2) == 85.80
    assert round(math / total * 100, 2) == 74.97
    assert round(both / total * 100, 2) == 65.16


def test_column_selected_groupby_runs(full_data):
    # This is the form the notebook uses. It must work on current pandas.
    result = full_data.groupby("Name_School")["Math_Grade"].mean()
    assert len(result) == 15
    assert result.notna().all()


def test_private_beats_public_overall_approval(full_data, schools):
    # The notebook reports the mean of per-school approval rates (each school
    # weighted equally), not the student-level pooled rate. This reproduces the
    # 90.43% / 53.67% figures in the README and df_performance_type_school.
    students_per_school = full_data["Name_School"].value_counts()
    approved = full_data[
        (full_data["Writing_Grade"] >= PASS_GRADE)
        & (full_data["Math_Grade"] >= PASS_GRADE)
    ]
    rate_per_school = (
        approved.groupby("Name_School")["Name_Student"].count()
        / students_per_school
        * 100
    )
    school_type = schools.set_index("Name_School")["Type_School"]
    by_type = (
        pd.DataFrame({"rate": rate_per_school, "type": school_type})
        .groupby("type")["rate"]
        .mean()
    )
    assert round(by_type["Private"], 2) == 90.43
    assert round(by_type["Public"], 2) == 53.67


def test_school_o_enrollment_mismatch(students, schools):
    # Documented data-quality note: School O reports 1635 enrolled but only
    # 1625 student records exist. This test pins that known discrepancy so a
    # silent data change is noticed.
    enrolled = int(
        schools.loc[schools["Name_School"] == "School O", "Stundents_Number"].iloc[0]
    )
    records = int((students["Name_School"] == "School O").sum())
    assert enrolled == 1635
    assert records == 1625
