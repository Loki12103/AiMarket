import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

print("=" * 60)
print("DATA CLEANING PIPELINE")
print("=" * 60)
print()

print("Step 1: Downloading NLTK stopwords...")
nltk.download("stopwords", quiet=True)
stop_words = set(stopwords.words("english"))
print(f" Loaded {len(stop_words)} stopwords")
print(f"Sample stopwords: {list(stop_words)[:10]}")
print()

print("Step 2: Loading Amazon dataset...")
try:
    df = pd.read_excel("datasets/Amazon DataSheet - Pradeep.xlsx")
    print(f" Loaded dataset with {len(df)} rows and {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)}")
    print()
except FileNotFoundError:
    print(" Error: 'datasets/Amazon DataSheet - Pradeep.xlsx' not found!")
    print("Please place the Amazon dataset Excel file in the datasets folder.")
    print()
    exit()


print("Step 3: Removing duplicate rows...")
initial_count = len(df)
df = df.drop_duplicates()
removed_duplicates = initial_count - len(df)
print(f" Removed {removed_duplicates} duplicate rows")
print(f"Remaining rows: {len(df)}")
print()

print("Step 4: Converting text to lowercase...")
text_columns = df.select_dtypes(include=["object"]).columns
for col in text_columns:
    df[col] = df[col].astype(str).str.lower()
print(f" Converted {len(text_columns)} text columns to lowercase")
print()


print("Step 5: Removing punctuation...")
def remove_punctuation(text):
    if isinstance(text, str):
        return re.sub(r"[^\w\s]", "", text)
    return text

for col in text_columns:
    df[col] = df[col].apply(remove_punctuation)
print(f" Removed punctuation from all text columns")
print()


print("Step 6: Removing stopwords...")
def remove_stopwords(text):
    if isinstance(text, str):
        return " ".join(
            [word for word in text.split() if word not in stop_words]
        )
    return text

for col in text_columns:
    df[col] = df[col].apply(remove_stopwords)
print(f" Removed stopwords from all text columns")
print()


print("Step 7: Removing extra spaces...")
for col in text_columns:
    df[col] = df[col].str.replace(r"\s+", " ", regex=True).str.strip()
print(f" Normalized whitespace in all text columns")
print()


print("Step 8: Saving cleaned dataset...")
output_file = "datasets/amazon_dataset_cleaned.csv"
df.to_csv(output_file, index=False)
print(f" Saved cleaned data to '{output_file}'")
print()


print("=" * 60)
print("CLEANING COMPLETED SUCCESSFULLY! ✅")
print("=" * 60)
print(f"Final dataset: {len(df)} rows × {len(df.columns)} columns")
print()
print("Sample of cleaned data (first 3 rows):")
print("-" * 60)
print(df.head(3))
print()
print("=" * 60)
