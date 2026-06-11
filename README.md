# Education Analysis

School performance analysis with Python (Pandas) and Power BI.

A network of schools wanted to understand its market: how students perform, how much is spent per student, and which factors actually move Math and Writing results. This repo answers those questions from two mock datasets (15 schools, 39,160 student records) using Pandas, and presents the same story in a Power BI dashboard.

[Executive Report (PDF)](https://github.com/Caio-Felice-Cunha/Education-Analysis/blob/main/Executive%20Report%20Education%20Analysis.pdf) /
[Notebook](https://github.com/Caio-Felice-Cunha/Education-Analysis/blob/main/Education%20Analysis.ipynb) /
[Power BI Dashboard](https://app.powerbi.com/view?r=eyJrIjoiZTdiMGZmMTItZDZlYi00ZTAxLTkyYTctYWNlNGJkNmU2MTRhIiwidCI6IjA4OTM0YTNmLWFkNmUtNDgzZS1hNjhlLTUxYWI3OTI1YmFiNyJ9)

<img align="center" src=https://user-images.githubusercontent.com/111542025/227356726-ebd8f5ae-a255-4200-afed-caf36053001b.jpg>

## Business Problem

The school network wanted to better understand its market: student performance, spending per school, and which indicators lead to better Math and Writing results. The assumption is that the schools sit in slightly different but culturally similar regions, so comparisons across them are meaningful.

Data source: provided by the Data Science Academy, generated with the Realistic Data Generator at Mockaroo (https://www.mockaroo.com/). It is mock data, not real student records.

## Data at a Glance

* 15 schools (8 private, 7 public)
* 39,160 student records
* $24,649,428 total annual budget
* Passing grade for both subjects: 70

## How to Run

```bash
git clone https://github.com/Caio-Felice-Cunha/Education-Analysis
cd Education-Analysis
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook "Education Analysis.ipynb"
```

Then run the cells top to bottom. The notebook reads the two CSVs in `datasets/` and writes a summary workbook to `datasets/df_summary_school_performance.xlsx`. Verified end to end on Python 3.13 with pandas 3.0.3.

A small test suite in `tests/` recomputes the headline metrics from the raw CSVs, so a future pandas upgrade or data change that breaks the pipeline is caught:

```bash
pip install pytest
pytest
```

## Results

All numbers below come straight from the notebook outputs and the Executive Report. Nothing here is estimated.

**Overall averages**

* Average Writing grade: 81.88
* Average Math grade: 78.98

**Approval (passing grade 70)**

* Writing: 33,600 students approved (85.80%)
* Math: 29,360 approved (74.97%)
* Both subjects: 25,518 approved (65.16%)

**Private vs public**

| Type | Avg Writing | Avg Math | % Overall Approved |
|---|---|---|---|
| Private | 83.89 | 83.48 | 90.43% |
| Public | 80.97 | 76.96 | 53.67% |

**Spending per student vs performance (the key finding)**

Higher spend per student lines up with lower overall approval, not higher. The relationship is inverse.

| Spend per student | % Overall Approved |
|---|---|
| Under $585 | 90.37% |
| $585 to $630 | 81.42% |
| $630 to $645 | 62.84% |
| $645 to $680 | 53.53% |

**School size**

| Size | % Overall Approved |
|---|---|
| Small (under 1,000) | 89.88% |
| Midsize (1,000 to 2,000) | 90.61% |
| Large (2,000 to 5,000) | 58.29% |

The top 5 schools by overall approval are all private (School G 91.33% down to School J 90.54%). The bottom 5 are all public (School L 52.99% up to School M 53.54%).

## Conclusion

Budget alone does not explain results. Public schools carry much larger total budgets, but that is driven by enrollment, not by generous per-student funding. Per-student spend is actually comparable across types (roughly $578 to $655), and the schools that spend the most per student post the lowest approval rates. The real gap is between private and public: about 37 percentage points in overall approval (90.43% vs 53.67%) at similar per-student spend. So money per student is not the differentiator here. The size and type of the school track far more closely with outcomes.

## Solution Strategy

The analysis uses the Python Pandas library plus a set of summary sub-tables.

* Step 1: load the data and check its quality.
* Step 2: select the data needed to answer each business question.
* Step 3: analyze with Pandas and build summary tables.

## Data Quality Note

School O reports an enrollment of 1,635 in `schools_dataset.csv` but only 1,625 student records exist in `students_dataset.csv` (10 records short). Because per-student budget is computed from record counts, School O shows $641.93 per student instead of the $638.00 you get from `Annual_Budget / Stundents_Number`. This does not change any conclusion above, but it is worth knowing when comparing School O to the rest. (The `Stundents_Number` spelling is the column header as provided in the source data.)

## Notes on This Version

This is the 2nd version. Compared to the previous one it adds the Power BI dashboard and the executive report. The notebook was later updated to run on pandas 2.0 and later (column-selected groupby aggregations) and to drop two unused imports.

`datasets/df_summary_school_performance.xlsx` is a generated output of the notebook (the per-school summary table), kept here as a downloadable result.

## Disclaimer

A good part of this project was built during the Data Science Academy "Big Data Real-Time Analytics with Python and Spark" course (part of the Data Scientist training).
