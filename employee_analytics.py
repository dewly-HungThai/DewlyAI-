import numpy as np
import pandas as pd


class EmployeeAnalytics:
    def __init__(self, file_path: str = None, df: pd.DataFrame = None):
        self.file_path = file_path
        self.df = df

    #  1. LOAD 
    def load_data(self) -> None:
        self.df = pd.read_csv(self.file_path)
        print(f"[LOAD] {len(self.df)} rows x {len(self.df.columns)} columns")
        print(f"Columns: {list(self.df.columns)}\n")

    #  2. CLEAN 
    def clean_data(self) -> None:
        print("[CLEAN] Missing values (before):")
        print(self.df.isnull().sum().to_string(), "\n")

        before = len(self.df)
        self.df.drop_duplicates(inplace=True)
        print(f"Dropped {before - len(self.df)} duplicate rows")

        for col in self.df.columns:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                self.df[col] = self.df[col].fillna(self.df[col].mean())
            else:
                self.df[col] = self.df[col].fillna("Unknown")

        print("\n[CLEAN] Missing values (after):")
        print(self.df.isnull().sum().to_string(), "\n")

    #  3. FILTER 
    def filter_data(self, col: str, operator: str, value) -> pd.DataFrame:
        ops = {
            "==": self.df[col] == value,
            "!=": self.df[col] != value,
            ">":  self.df[col] > value,
            "<":  self.df[col] < value,
            ">=": self.df[col] >= value,
            "<=": self.df[col] <= value,
        }
        if operator not in ops:
            raise ValueError(f"Invalid operator. Choose from: {list(ops.keys())}")

        result = self.df[ops[operator]].copy()
        print(f"[FILTER] {col} {operator} {value!r} → {len(result)} rows\n")
        return result

    #  4. DEPARTMENT STATISTICS (NumPy) ─
    def department_stats(self, dept_col: str = "Company") -> pd.DataFrame:
        records = []
        for dept, group in self.df.groupby(dept_col):
            salary = group["Salary"].dropna().to_numpy()
            age    = group["Age"].dropna().to_numpy()
            records.append({
                "Department":    dept,
                "Headcount":     len(group),
                "Avg_Salary":    round(np.mean(salary), 2),
                "Median_Salary": round(np.median(salary), 2),
                "Std_Salary":    round(np.std(salary), 2),
                "Min_Salary":    round(np.min(salary), 2),
                "Max_Salary":    round(np.max(salary), 2),
                "Avg_Age":       round(np.mean(age), 1),
            })

        stats_df = pd.DataFrame(records).sort_values("Avg_Salary", ascending=False)
        print("[DEPT STATS]")
        print(stats_df.to_string(index=False), "\n")
        return stats_df

    #  5. EXPORT REPORT (CSV) 
    def export_report(self, output_path: str = "employee_report.csv",
                      dept_col: str = "Department") -> None:
        dept_stats = self.department_stats(dept_col=dept_col)

        overall = {
            "Department":    "-- OVERALL --",
            "Headcount":     len(self.df),
            "Avg_Salary":    round(self.df["Salary"].mean(), 2),
            "Median_Salary": round(self.df["Salary"].median(), 2),
            "Std_Salary":    round(self.df["Salary"].std(), 2),
            "Min_Salary":    round(self.df["Salary"].min(), 2),
            "Max_Salary":    round(self.df["Salary"].max(), 2),
            "Avg_Age":       round(self.df["Age"].mean(), 1),
        }
        report = pd.concat(
            [dept_stats, pd.DataFrame([overall])],
            ignore_index=True
        )
        report.to_csv(output_path, index=False)
        print(f"[EXPORT] Report saved → {output_path}\n")


if __name__ == "__main__":
    tool = EmployeeAnalytics("/Users/hungthai/Desktop/DewlyAI/employees.csv")

    tool.load_data()
    tool.clean_data()

    # Filter examples
    engineering  = tool.filter_data("Department", "==", "Engineering")
    senior_staff = tool.filter_data("Age", ">=", 35)
    high_earners = tool.filter_data("Salary", ">", 2500)

    # Department statistics
    tool.department_stats(dept_col="Department")

    # Statistics on filtered subset (senior staff only)
    print("[SENIOR STAFF — dept breakdown]")
    senior_tool = EmployeeAnalytics(df=senior_staff)
    senior_tool.department_stats(dept_col="Department")

    # Export full report to CSV
    tool.export_report("employee_report.csv", dept_col="Department")
