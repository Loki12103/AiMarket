"""
Smart Category Assignment - Hybrid Approach
--------------------------------------------
Uses keyword matching first, then LLM for uncertain cases
"""

import os
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("=" * 60)
print("SMART CATEGORY ASSIGNMENT")
print("=" * 60)
print()

# --------------------------
# METHOD 1: Keyword Matching
# --------------------------
def assign_category_by_keywords(product_name):
    """Fast keyword-based category assignment"""
    product_lower = str(product_name).lower()
    
    # Electronics
    if any(word in product_lower for word in ['phone', 'mobile', 'smartphone', 'iphone', 'samsung', 'oneplus', 'realme', 'xiaomi', 'oppo', 'vivo', 'redmi']):
        return 'Mobile Phones'
    elif any(word in product_lower for word in ['laptop', 'notebook', 'macbook', 'computer', 'pc', 'dell', 'hp', 'lenovo', 'asus']):
        return 'Laptops'
    elif any(word in product_lower for word in ['headphone', 'earphone', 'earbud', 'airpod', 'speaker', 'audio', 'jbl', 'sony', 'boat']):
        return 'Audio'
    elif any(word in product_lower for word in ['tv', 'television', 'monitor', 'display', 'screen']):
        return 'Display'
    elif any(word in product_lower for word in ['camera', 'dslr', 'gopro', 'canon', 'nikon']):
        return 'Camera'
    elif any(word in product_lower for word in ['watch', 'smartwatch', 'fitbit', 'band', 'fitness tracker']):
        return 'Wearables'
    elif any(word in product_lower for word in ['charger', 'cable', 'adapter', 'powerbank', 'usb']):
        return 'Accessories'
    
    # Fashion
    elif any(word in product_lower for word in ['shirt', 't-shirt', 'tshirt', 'top', 'dress', 'jeans', 'pant', 'trouser', 'kurta', 'saree']):
        return 'Clothing'
    elif any(word in product_lower for word in ['shoe', 'shoes', 'sneaker', 'boot', 'sandal', 'slipper', 'footwear', 'nike', 'adidas', 'puma']):
        return 'Footwear'
    elif any(word in product_lower for word in ['bag', 'backpack', 'purse', 'wallet', 'handbag', 'luggage']):
        return 'Bags & Accessories'
    
    # Home & Kitchen
    elif any(word in product_lower for word in ['refrigerator', 'fridge', 'ac', 'washing machine', 'microwave', 'oven', 'mixer', 'grinder', 'toaster']):
        return 'Home Appliances'
    elif any(word in product_lower for word in ['bed', 'sofa', 'chair', 'table', 'furniture', 'mattress', 'pillow', 'cushion']):
        return 'Furniture'
    elif any(word in product_lower for word in ['plate', 'bowl', 'cup', 'glass', 'utensil', 'cookware', 'pan', 'pot']):
        return 'Kitchen & Dining'
    
    # Beauty & Personal Care
    elif any(word in product_lower for word in ['cream', 'lotion', 'perfume', 'shampoo', 'conditioner', 'soap', 'facewash', 'lipstick', 'makeup']):
        return 'Beauty & Personal Care'
    
    # Books & Media
    elif any(word in product_lower for word in ['book', 'novel', 'magazine', 'diary', 'notebook', 'pen', 'pencil']):
        return 'Books & Stationery'
    
    # Sports & Fitness
    elif any(word in product_lower for word in ['gym', 'dumbbell', 'yoga', 'treadmill', 'cycle', 'cricket', 'football', 'sports']):
        return 'Sports & Fitness'
    
    # Toys & Kids
    elif any(word in product_lower for word in ['toy', 'game', 'puzzle', 'doll', 'lego', 'kids', 'baby']):
        return 'Toys & Kids'
    
    else:
        return 'Others'


# --------------------------
# METHOD 2: LLM Classification
# --------------------------
def categorize_with_llm(product_name):
    """Use Gemini for uncertain products"""
    prompt = f"""Classify this product into ONE category: {product_name}

Categories: Mobile Phones, Laptops, Audio, Display, Camera, Wearables, Accessories, Clothing, Footwear, Bags & Accessories, Home Appliances, Furniture, Kitchen & Dining, Beauty & Personal Care, Books & Stationery, Sports & Fitness, Toys & Kids, Grocery, Others

Return only the category name, nothing else."""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.1)
        )
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ LLM Error: {e}")
        return 'Others'


# --------------------------
# METHOD 3: Hybrid Approach
# --------------------------
def smart_categorize(product_name):
    """Try keywords first, use LLM for Others"""
    # Step 1: Try keyword matching
    category = assign_category_by_keywords(product_name)
    
    # Step 2: If uncertain, use LLM
    if category == 'Others' and str(product_name).strip() != '':
        print(f"  🤖 Using LLM for: {product_name}")
        category = categorize_with_llm(product_name)
    
    return category


# --------------------------
# Load and Process Dataset
# --------------------------
print("Loading dataset...")
try:
    df = pd.read_csv("datasets/sentimentdataset_cleaned.csv")
    print(f"✓ Loaded {len(df)} rows")
    print()
except FileNotFoundError:
    print("❌ Error: datasets/sentimentdataset_cleaned.csv not found!")
    print("Run data_cleaning.py first.")
    exit()

# Check if product column exists
product_col = None
for col in df.columns:
    if 'product' in col.lower() or 'name' in col.lower() or 'text' in col.lower():
        product_col = col
        break

if product_col is None:
    print("❌ No product column found in dataset!")
    print(f"Available columns: {list(df.columns)}")
    exit()

print(f"Using column: '{product_col}' for categorization")
print("-" * 60)
print()

# Assign categories
print("Assigning categories...")
print("-" * 60)
df['category'] = df[product_col].apply(smart_categorize)

# Show statistics
print()
print("=" * 60)
print("CATEGORY DISTRIBUTION")
print("=" * 60)
print(df['category'].value_counts())
print()

# Show sample results
print("=" * 60)
print("SAMPLE RESULTS (First 10 rows)")
print("=" * 60)
sample = df[[product_col, 'category']].head(10)
for idx, row in sample.iterrows():
    text_value = str(row[product_col])[:50] if len(str(row[product_col])) > 50 else str(row[product_col])
    print(f"{idx+1}. {text_value:<50} → {row['category']}")
print()

# Save result
output_file = "datasets/sentimentdataset_with_categories.csv"
df.to_csv(output_file, index=False)
print(f"✅ Saved categorized dataset to: {output_file}")
print()
print("=" * 60)
