import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class DataAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    # 1. LOAD
    def load_data(self):
        self.df = pd.read_csv(self.file_path)
        print(f"Loaded: {len(self.df)} rows x {len(self.df.columns)} columns")
        print(self.df.dtypes, "\n")

    # 2. CLEAN
    def clean_data(self):
        print("=== Missing Values (before) ===")
        print(self.df.isnull().sum(), "\n")

        #duplicate rows
        before = len(self.df)
        self.df.drop_duplicates(inplace=True)
        print(f"Dropped {before - len(self.df)} duplicate rows\n")

        #missing values
        for col in self.df.columns:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                self.df[col] = self.df[col].fillna(self.df[col].mean())
            else:
                self.df[col] = self.df[col].fillna("Unknown")

        print("=== Missing Values (after) ===")
        print(self.df.isnull().sum(), "\n")

    # 3. FILTER
    def filter_data(self, col: str, operator: str, value) -> pd.DataFrame:
        """
        operator: "==", ">", "<", ">=", "<="
        """
        ops = {
            "==": self.df[col] == value,
            ">":  self.df[col] > value,
            "<":  self.df[col] < value,
            ">=": self.df[col] >= value,
            "<=": self.df[col] <= value,
        }
        if operator not in ops:
            raise ValueError(f"Invalid Operator. Choose: {list(ops.keys())}")

        result = self.df[ops[operator]].copy()
        print(f"Filter '{col} {operator} {value}': {len(result)} rows\n")
        return result

    # 4. GROUPBY─
    def group_data(self, df: pd.DataFrame, group_col: str,
                   agg_col: str, agg_func: str = "mean") -> pd.DataFrame:
        """
        agg_func: "mean", "sum", "count"
        """
        if agg_func not in ("mean", "sum", "count"):
            raise ValueError("agg_func should be: mean, sum, count")

        result = df.groupby(group_col)[agg_col].agg(agg_func).reset_index()
        result.columns = [group_col, f"{agg_func}_{agg_col}"]
        print(f"=== Group by '{group_col}' | {agg_func}({agg_col}) ===")
        print(result, "\n")
        return result

    # 5. NUMPY STATISTICS
    def compute_statistics(self) -> pd.DataFrame:
        numeric_df = self.df.select_dtypes(include=np.number)
        stats = {}
        for col in numeric_df.columns:
            arr = numeric_df[col].dropna().to_numpy()
            stats[col] = {
                "mean":   np.mean(arr),
                "median": np.median(arr),
                "std":    np.std(arr),
                "min":    np.min(arr),
                "max":    np.max(arr),
                "q25":    np.percentile(arr, 25),
                "q75":    np.percentile(arr, 75),
            }
        return pd.DataFrame(stats).round(2)

    # 6. SUMMARY REPORT
    def summary_report(self):
        print("=" * 50)
        print("           SUMMARY REPORT")
        print("=" * 50)
        print(f"Rows    : {len(self.df)}")
        print(f"Columns : {len(self.df.columns)}")
        print(f"\nColumn types:\n{self.df.dtypes}")
        print(f"\nMissing values:\n{self.df.isnull().sum()}")

        print("\n=== Statistics (NumPy) ===")
        stats_df = self.compute_statistics()
        print(stats_df)

        print("\n=== Visualize ===")
        numeric_df = self.df.select_dtypes(include=np.number)
        numeric_df.hist(figsize=(10, 6), bins=15)
        plt.tight_layout()
        plt.show()
        print("=" * 50)


# DEMO
if __name__ == "__main__":
    analyzer = DataAnalyzer("/Users/hungthai/Desktop/DewlyAI/employee.csv")

    analyzer.load_data()
    analyzer.clean_data()

    # Filter: Salary > 5000
    high_salary = analyzer.filter_data("Salary", ">", 5000)

    # Group
    analyzer.group_data(analyzer.df, group_col="Company", agg_col="Salary", agg_func="mean")

    # Group after filter
    analyzer.group_data(high_salary, group_col="Place", agg_col="Salary", agg_func="sum")

    analyzer.summary_report()
