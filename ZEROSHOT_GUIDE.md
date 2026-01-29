# Zero-Shot Classification with BART

## What is Zero-Shot Learning?

**Zero-shot learning** means the model can classify items into categories it has **never been explicitly trained on**.

### Traditional ML:
```
Training: Show 1000 examples of "Electronics"
Testing: Classify new electronics
```

### Zero-Shot:
```
Training: None!
Testing: Just tell the model "Electronics" exists, and it classifies
```

---

## What is BART?

**BART** = **B**idirectional and **A**uto**R**egressive **T**ransformers

### How BART Works:

1. **Encoder** (like BERT):
   - Reads text in both directions
   - Understands context deeply

2. **Decoder** (like GPT):
   - Generates text
   - Fixes corrupted inputs

3. **Pretraining**:
   - Text is corrupted (words deleted, shuffled, masked)
   - BART learns to recover original text
   - Result: Excellent at understanding AND generating

### BART-Large-MNLI:
- Trained on **Natural Language Inference** (MNLI dataset)
- Learns to understand if text matches a hypothesis
- Perfect for zero-shot classification!

---

## How Zero-Shot Classification Works

### Process:

```python
product = "iPhone 15 Pro Max 256GB"
labels = ["Electronics", "Fashion", "Furniture"]

# Model internally creates hypotheses:
# 1. "This product is about Electronics"
# 2. "This product is about Fashion"  
# 3. "This product is about Furniture"

# Then calculates confidence for each:
# Electronics: 98.5%
# Fashion: 1.2%
# Furniture: 0.3%
```

---

## Advantages of Zero-Shot

### ✅ Pros:

1. **No Training Required**
   - Works immediately
   - No need for labeled data
   - No GPU/training time needed

2. **Flexible Categories**
   - Add/remove categories anytime
   - Just change the labels list
   - No retraining

3. **Multilingual**
   - Works with different languages
   - Same model, multiple use cases

4. **Contextual Understanding**
   - Understands product descriptions
   - Not just keyword matching
   - Considers full context

### ❌ Cons:

1. **Slower Than Keywords**
   - Each product takes ~1-2 seconds
   - Keyword matching is instant

2. **Model Size**
   - BART-large is ~1.6GB
   - Requires decent RAM

3. **Confidence Can Vary**
   - Some products get low confidence
   - May need manual review

---

## Implementation in This Project

### Files Created:

1. **zeroshot_classification.py**
   - Single product demo
   - Shows confidence scores
   - Top 3 predictions

2. **zeroshot_batch_classification.py**
   - Processes CSV files
   - Progress bar (tqdm)
   - Saves results

---

## Example Use Cases

### Product Categorization:
```python
product = "Nike Air Max 270 Running Shoes"
labels = ["Electronics", "Fashion", "Sports"]

# Result: Sports (95% confidence)
```

### Sentiment Analysis:
```python
review = "This product is absolutely amazing!"
labels = ["positive", "negative", "neutral"]

# Result: positive (99% confidence)
```

### Topic Classification:
```python
article = "iPhone 15 launches with USB-C..."
labels = ["Technology", "Politics", "Sports"]

# Result: Technology (97% confidence)
```

---

## Categories Defined

### Our 20 Categories:

1. **Electricals_Power_Backup** - UPS, batteries, inverters
2. **Home_Appliances** - Washing machines, AC, vacuum cleaners
3. **Kitchen_Appliances** - Mixer, blender, microwave
4. **Furniture** - Tables, chairs, sofas
5. **Home_Storage_Organization** - Containers, racks
6. **Computers_Tablets** - Laptops, tablets, desktops
7. **Mobile_Accessories** - Cases, chargers, earphones
8. **Wearables** - Smartwatches, fitness bands
9. **TV_Audio_Entertainment** - TVs, speakers, soundbars
10. **Networking_Devices** - Routers, modems, WiFi
11. **Toys_Kids** - Games, educational toys
12. **Gardening_Outdoor** - Plants, tools, decor
13. **Kitchen_Dining** - Utensils, cookware
14. **Mens_Clothing** - Shirts, pants, suits
15. **Footwear** - Shoes, sandals, boots
16. **Beauty_Personal_Care** - Cosmetics, skincare
17. **Security_Surveillance** - Cameras, alarms
18. **Office_Printer_Supplies** - Printers, paper, ink
19. **Software** - Applications, games
20. **Fashion_Accessories** - Bags, wallets, watches

---

## Running the Scripts

### Install Dependencies:
```powershell
.\env\Scripts\Activate
pip install transformers torch tqdm
```

### Run Single Product Demo:
```powershell
python zeroshot_classification.py
```

### Run Batch Processing:
```powershell
python zeroshot_batch_classification.py
```

---

## Customization

### Change Categories:
```python
labels = [
    "Your_Category_1",
    "Your_Category_2",
    "Your_Category_3"
]
```

### Change Dataset:
```python
df = pd.read_csv("datasets/your_file.csv")
product_col = "Your_Product_Column"
```

### Process All Products:
```python
# Remove .head(20) to process all
df_sample = df  # Process entire dataset
```

---

## Performance Comparison

| Method | Speed | Accuracy | Setup |
|--------|-------|----------|-------|
| **Keyword Matching** | ⚡ Instant | 70% | Easy |
| **Zero-Shot (BART)** | 🐢 1-2 sec/product | 85-90% | Medium |
| **Fine-tuned Model** | 🚀 Fast | 95%+ | Hard |

---

## Best Practices

### 1. Use Descriptive Category Names
❌ Bad: "cat1", "cat2", "misc"
✅ Good: "Electronics", "Fashion", "Home_Appliances"

### 2. Keep Categories Distinct
❌ Bad: "Electronics" + "Mobile Electronics"
✅ Good: "Computers" + "Mobile_Accessories"

### 3. Test Before Batch Processing
- Run on 10-20 products first
- Check confidence scores
- Adjust categories if needed

### 4. Set Confidence Threshold
```python
if confidence > 0.7:
    category = predicted
else:
    category = "Needs_Manual_Review"
```

---

## Troubleshooting

### Model Takes Forever to Load?
- First time downloads ~1.6GB model
- Subsequent runs use cached model
- Cache location: `~/.cache/huggingface/`

### Out of Memory Error?
- Use `device=-1` (CPU mode)
- Process smaller batches
- Close other applications

### Low Confidence Scores?
- Product names too vague
- Categories not descriptive enough
- Need more context (use descriptions)

---

## Next Steps

1. ✅ Run single product demo
2. ✅ Test on 20 products
3. ✅ Compare with keyword matching
4. ✅ Process full dataset
5. ✅ Analyze confidence scores
6. ✅ Create hybrid approach (keywords + zero-shot)

---

## Resources

- **BART Paper**: https://arxiv.org/abs/1910.13461
- **Hugging Face Model**: https://huggingface.co/facebook/bart-large-mnli
- **Transformers Docs**: https://huggingface.co/docs/transformers/
- **Zero-Shot Guide**: https://joeddav.github.io/blog/2020/05/29/ZSL.html
