"""
Zero-Shot Classification on CSV Dataset
----------------------------------------
Classify all products from a CSV file using BART model
Processes large datasets efficiently
"""

from transformers import pipeline
import pandas as pd
from tqdm import tqdm
import time

print("=" * 60)
print("ZERO-SHOT CLASSIFICATION - BATCH PROCESSING")
print("=" * 60)
print()

# -----------------------------
# Load Model
# -----------------------------
print("Loading BART model...")
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=-1  # Use CPU (set to 0 for GPU if available)
)
print("✅ Model loaded!")
print()

# -----------------------------
# Define Categories
# -----------------------------
labels = [
    "Electronics",
    "Home Appliances",
    "Kitchen Appliances",
    "Furniture",
    "Computers & Tablets",
    "Mobile & Accessories",
    "Wearables",
    "TV & Audio",
    "Fashion & Clothing",
    "Footwear",
    "Beauty & Personal Care",
    "Toys & Kids",
    "Sports & Fitness",
    "Books & Stationery",
    "Grocery & Food",
    "Health & Wellness"
]

print(f"Categories: {len(labels)}")
print()

# -----------------------------
# Load Dataset
# -----------------------------
print("Loading dataset...")
try:
    # Try loading Amazon dataset
    df = pd.read_csv("datasets/amazon_dataset_cleaned.csv")
    product_col = "Product Name"
    print(f"✅ Loaded Amazon dataset: {len(df)} products")
except FileNotFoundError:
    try:
        # Try Flipkart dataset
        df = pd.read_csv("datasets/flipkart_product.csv", encoding="latin1")
        # Find product column
        for col in df.columns:
            if 'product' in col.lower() or 'name' in col.lower():
                product_col = col
                break
        print(f"✅ Loaded Flipkart dataset: {len(df)} products")
    except FileNotFoundError:
        print("❌ No dataset found!")
        print("Place amazon_dataset_cleaned.csv or flipkart_product.csv in datasets/ folder")
        exit()

print(f"Using column: '{product_col}'")
print()

# -----------------------------
# Sample for Testing (Process first 20)
# -----------------------------
print("Processing first 20 products for demonstration...")
print("(To process all, remove the .head(20) line in the code)")
print()

df_sample = df.head(20)

# -----------------------------
# Classify Products
# -----------------------------
results = []

print("Classifying products...")
print("-" * 60)

for idx, row in tqdm(df_sample.iterrows(), total=len(df_sample)):
    product_name = str(row[product_col])
    
    # Skip empty products
    if not product_name or product_name == "nan":
        continue
    
    try:
        result = classifier(product_name, labels)
        
        results.append({
            "product_name": product_name,
            "predicted_category": result["labels"][0],
            "confidence": round(result["scores"][0], 4),
            "second_best": result["labels"][1],
            "second_confidence": round(result["scores"][1], 4),
            "third_best": result["labels"][2],
            "third_confidence": round(result["scores"][2], 4)
        })
        
    except Exception as e:
        print(f"Error processing: {product_name[:50]} - {e}")
        continue
    
    time.sleep(0.1)  # Small delay

print()
print("✅ Classification completed!")
print()

# -----------------------------
# Save Results
# -----------------------------
df_results = pd.DataFrame(results)

output_file = "datasets/zeroshot_batch_results.csv"
df_results.to_csv(output_file, index=False)
print(f"✅ Saved to: {output_file}")
print()

# -----------------------------
# Analysis
# -----------------------------
print("=" * 60)
print("RESULTS SUMMARY")
print("=" * 60)
print(f"Total products classified: {len(df_results)}")
print()

print("Category Distribution:")
print("-" * 60)
print(df_results['predicted_category'].value_counts())
print()

print("Confidence Statistics:")
print("-" * 60)
print(f"Average: {df_results['confidence'].mean():.2%}")
print(f"Median: {df_results['confidence'].median():.2%}")
print(f"Min: {df_results['confidence'].min():.2%}")
print(f"Max: {df_results['confidence'].max():.2%}")
print()

# Low confidence predictions
low_conf = df_results[df_results['confidence'] < 0.5]
if not low_conf.empty:
    print("⚠️ Low Confidence Predictions (< 50%):")
    print("-" * 60)
    for idx, row in low_conf.iterrows():
        print(f"- {row['product_name'][:50]}")
        print(f"  Category: {row['predicted_category']} ({row['confidence']:.2%})")
    print()

# High confidence predictions
high_conf = df_results[df_results['confidence'] > 0.9]
print(f"✅ High Confidence Predictions (> 90%): {len(high_conf)}")
print()

# Sample results
print("=" * 60)
print("SAMPLE CLASSIFICATIONS")
print("=" * 60)
for idx, row in df_results.head(10).iterrows():
    print(f"\n{idx+1}. {row['product_name'][:60]}")
    print(f"   → {row['predicted_category']} ({row['confidence']:.2%})")
    print(f"   2nd: {row['second_best']} ({row['second_confidence']:.2%})")

print()
print("=" * 60)
