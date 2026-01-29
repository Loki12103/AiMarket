import pandas as pd
from transformers import pipeline
import torch
import re

# -----------------------------
# Load CSV
# -----------------------------
df = pd.read_csv("flipkart_product_reduced.csv").head(100)  # remove head() later

# -----------------------------
# Clean product name function
# -----------------------------
def clean_product_name(text):
    text = str(text).lower()
    text = re.sub(r"\d+", " ", text)              # remove numbers
    text = re.sub(r"[^a-zA-Z\s]", " ", text)       # remove special chars
    text = re.sub(r"\s+", " ", text).strip()      # remove extra spaces
    return text

df["clean_product"] = df["product"].apply(clean_product_name)

# -----------------------------
# Split Flipkart / non-Flipkart
# -----------------------------
df_flipkart = df[df["source"].str.lower() == "flipkart"].copy()
df_non_flipkart = df[df["source"].str.lower() != "flipkart"].copy()

# -----------------------------
# Zero-shot classifier (GPU if available)
# -----------------------------
device = 0 if torch.cuda.is_available() else -1
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=device,
)

labels = [
    "Electricals_Power_Backup",
    "Kitchen_Appliances",
    "Furniture",
    "Home_Storage_Organization",
    "Computers_Tablets",
    "Mobile_Accessories",
    "Wearables",
    "TV_Audio_Entertainment",
    "Networking_Devices",
    "Toys_Kids",
    "Gardening_Outdoor",
    "Kitchen_Dining",
    "Mens_Clothing",
    "Footwear",
    "Beauty_Personal_Care",
    "Security_Surveillance",
    "Office_Printer_Supplies",
    "Software",
    "Fashion_Accessories",
    "Sports and fitness",
    "Home_Appliances",
    "Health_Care",
    "Home Furnishings",
    "Grocery",
    "Tools"
]

# -----------------------------
# Deduplicate Flipkart products (use cleaned name)
# -----------------------------
unique_products = (
    df_flipkart[["product", "clean_product"]]
    .dropna()
    .drop_duplicates(subset="clean_product")
    .to_dict("records")
)

# -----------------------------
# Rule-based keyword override
# -----------------------------
def keyword_override(clean_name):
    if ("juicer" in clean_name or "mixer" in clean_name or "grinder" in clean_name or
        "heater" in clean_name or "dishwasher" in clean_name or "chimneyblack" in clean_name or
        "purifier" in clean_name or "otg" in clean_name or "ml" in clean_name or "cooking" in clean_name):
        return "Kitchen_Appliances"
    
    if "charger" in clean_name or "cable" in clean_name or "cover" in clean_name:
        return "Mobile_Accessories"
    
    if "toy" in clean_name or "kids" in clean_name:
        return "Toys_Kids"
    
    if ("cooler" in clean_name or "fan" in clean_name or "air" in clean_name or
        "refrigerator" in clean_name or "sewing" in clean_name):
        return "Home_Appliances"
    
    if (re.search(r"\b\d+(\.\d+)?\s*(w|kw|watt|watts)\b", clean_name) or "streaming" in clean_name or
        "speaker" in clean_name or "led" in clean_name or "intel" in clean_name or "ryzen" in clean_name or
        "home theatre" in clean_name or "core" in clean_name):
        return "Electronics"
    
    if "analog watch" in clean_name or "digital watch" in clean_name:
        return "Fashion"
    
    if ("bedsheet" in clean_name or "door mat" in clean_name or "curtain" in clean_name or
        "blanket" in clean_name or "cushion" in clean_name or "clock" in clean_name):
        return "Home Furnishings"
    
    if "cycle" in clean_name or "fitness" in clean_name or "gym" in clean_name:
        return "Sports and fitness"
    
    if "cutter" in clean_name or "soldering" in clean_name or "tools" in clean_name:
        return "Tools"
    
    if "seed" in clean_name:
        return "Gardening_Outdoor"
    
    if "ballon" in clean_name or "decoration" in clean_name:
        return "Party_Accessories"
    
    if "wardrobe" in clean_name:
        return "Furniture"
    
    return None

# -----------------------------
# Batch classify
# -----------------------------
batch_size = 16
pred_rows = []

for i in range(0, len(unique_products), batch_size):
    batch = unique_products[i : i + batch_size]
    texts = [item["clean_product"] for item in batch]
    results = classifier(texts, labels)
    
    if isinstance(results, dict):
        results = [results]
    
    for item, res in zip(batch, results):
        override_category = keyword_override(item["clean_product"])
        final_category = override_category if override_category else res["labels"][0]
        final_confidence = 1.0 if override_category else round(float(res["scores"][0]), 3)
        
        pred_rows.append({
            "product": item["product"],
            "category": final_category,
            "category_confidence": final_confidence,
        })

pred_df = pd.DataFrame(pred_rows)

# -----------------------------
# Merge predictions back
# -----------------------------
df_flipkart = df_flipkart.drop(columns=["category"], errors="ignore")
df_flipkart = df_flipkart.merge(
    pred_df,
    on="product",
    how="left",
)

# -----------------------------
# Non-Flipkart rows
# -----------------------------
df_non_flipkart["predicted_category"] = None
df_non_flipkart["category_confidence"] = None

# -----------------------------
# Combine & Save
# -----------------------------
df_final = pd.concat([df_flipkart, df_non_flipkart], ignore_index=True)
df_final.to_csv("category.csv", index=False)
print("✅ Category prediction completed with cleaning + rule-based fixes.")
