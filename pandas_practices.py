import pandas as pd
import numpy as np



def load_data(filepath="employee.csv"):
    df = pd.read_csv(filepath)
    print("=== Load Data ===")
    print(df.head())
    print(df.info())
    print(df.describe(), "\n")
    return df


def save_data(df: pd.DataFrame, filepath="employee_cleaned.csv"):
    df.to_csv(filepath, index=False)
    print(f"Saved to {filepath}\n")



def filter_salary(df: pd.DataFrame, threshold: float):
    result = df[df["Salary"] > threshold]
    print(f"=== Filter Salary > {threshold} ===")
    print(result[["Company", "Age", "Salary"]].head(10), "\n")
    return result


def filter_combined(df: pd.DataFrame):
    result = df[(df["Company"] == "TCS") & (df["Salary"] > 5000) & (df["Gender"] == 1)]
    print("=== Combined Filter (TCS, Salary>5000, Female) ===")
    print(result[["Company", "Age", "Salary", "Gender"]], "\n")
    return result


def groupby_department(df: pd.DataFrame):
    result = df.groupby("Company")["Salary"].agg(
        count="count",
        mean="mean",
        median="median",
        max="max",
    ).round(2)
    print("=== Groupby Company → Salary Stats ===")
    print(result, "\n")
    return result


def tax_rate(salary):
    if pd.isna(salary):
        return np.nan
    if salary <= 3000:
        return 0.10
    if salary <= 6000:
        return 0.15
    return 0.20


def demo_apply(df: pd.DataFrame):
    df = df.copy()
    df["tax_rate"]      = df["Salary"].apply(tax_rate)
    df["salary_after_tax"] = df.apply(
        lambda row: row["Salary"] * (1 - row["tax_rate"])
        if not pd.isna(row["Salary"]) else np.nan,
        axis=1,
    ).round(2)

    print("=== Apply: Salary After Tax ===")
    print(df[["Company", "Salary", "tax_rate", "salary_after_tax"]].dropna().head(10), "\n")
    return df


def handle_missing(df: pd.DataFrame):
    print("=== Missing Values (before) ===")
    print(df.isnull().sum(), "\n")

    # Delete Company null 
    df = df[df["Company"].notna()].copy()

    # Replace Age by median of flowing Company
    df["Age"] = df.groupby("Company")["Age"].transform(
        lambda x: x.fillna(x.mean().round())
    )

    # Replace Salary by median of flowing Company
    df["Salary"] = df.groupby("Company")["Salary"].transform(
        lambda x: x.fillna(x.median())
    )

    # Replace Place to "Unknown"
    df["Place"] = df["Place"].fillna("Unknown")

    print("=== Missing Values (after) ===")
    print(df.isnull().sum(), "\n")
    return df


def sort_by_salary(df: pd.DataFrame):
    result = df.sort_values("Salary", ascending=False)
    print("=== Sort Salary Descending ===")
    print(result[["Company", "Age", "Salary"]].head(10), "\n")
    return result


def add_salary_after_tax(df: pd.DataFrame):
    df = df.copy()
    df["salary_after_tax"] = df["Salary"].apply(
        lambda s: round(s * (1 - tax_rate(s)), 2) if not pd.isna(s) else np.nan
    )
    print("=== New Column: salary_after_tax ===")
    print(df[["Company", "Salary", "salary_after_tax"]].head(10), "\n")
    return df




if __name__ == "__main__":

    #Load data
    df = load_data("employee.csv")


    #Handle missing values
    df = handle_missing(df)

    #Filtering
    filter_salary(df, threshold=5000)

    #Groupby department → average salary
    groupby_department(df)

    #Apply + new column
    df = demo_apply(df)

    #Sort salary descending
    sort_by_salary(df)

    #Save cleaned data
    save_data(df)
