# API Data Collection Guide

## 📋 Quick Links

- **[Postman Testing Guide](POSTMAN_GUIDE.md)** - Test APIs visually before coding
- **[NewsAPI Setup](news_api.py)** - Get product news from 50,000+ sources
- **[Mixed Reviews Collector](mixed_reviews_collector.py)** - Collect both positive & negative reviews

---

## What is an API?

**API = Application Programming Interface**

Think of it like a **restaurant**:
- **You (User)** → Request food
- **Waiter (API)** → Takes request to kitchen
- **Kitchen (Server)** → Prepares food (data)
- **Waiter (API)** → Delivers it back to you

APIs allow two software systems to communicate with each other without exposing the backend.

---

## HTTP Methods

| Method | Purpose | Example |
|--------|---------|---------|
| **GET** | Fetch data | Get weather info, get user profile |
| **POST** | Send/Create data | Submit form, create new user |
| **PUT** | Update data | Update student record |
| **DELETE** | Remove data | Delete account |

---

## API Call Structure

```
https://api.example.com/data?city=Delhi&units=metric
```

- **Base URL**: `https://api.example.com`
- **Endpoint**: `/data` (specific resource)
- **Parameters**: `?city=Delhi&units=metric` (extra info)

---

## API Response Format

Usually in **JSON** format:

```json
{
  "city": "Delhi",
  "temperature": "30°C",
  "condition": "Sunny"
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| **200** | ✅ Success |
| **400** | ❌ Bad Request |
| **401** | ❌ Unauthorized (need API key) |
| **404** | ❌ Not Found |
| **500** | ❌ Server Error |

---

## Examples in This Project

### 1. **GitHub API** (GET Request)
**File**: `github_api.py`

Fetches user information from GitHub:
```python
url = "https://api.github.com/users/octocat"
response = requests.get(url)
data = response.json()
```

**No API key required** ✅

---

### 2. **Weather API** (GET with Parameters)
**File**: `weather_api.py`

Fetches weather data from Open-Meteo:
```python
params = {
    "latitude": 28.6139,
    "longitude": 77.2090,
    "current_weather": True
}
response = requests.get(base_url, params=params)
```

**No API key required** ✅

---

### 3. **Reddit API** (Product Discussions)
**File**: `reddit_api.py`

Scrapes product discussions from Reddit:
```python
url = "https://www.reddit.com/search.json"
params = {"q": "iPhone 15", "limit": 50}
response = requests.get(url, params=params)
```

**No API key required** ✅

---

### 4. **NewsAPI** (Product News)
**File**: `news_api.py`

Fetches news articles about products:
```python
params = {
    "q": "iPhone 15 review",
    "from": "2025-12-09",
    "apiKey": NEWS_API_KEY
}
response = requests.get(base_url, params=params)
```

**Requires FREE API key** from [newsapi.org](https://newsapi.org/register) (500 requests/day)

---

### 5. **Mixed Reviews Collector**
**File**: `mixed_reviews_collector.py`

Collects reviews from multiple sources (positive + negative):
```python
reddit_reviews = fetch_mixed_reviews_reddit("iPhone 15", limit=50)
bestbuy_reviews = fetch_best_buy_reviews("iPhone 15")
twitter_reviews = fetch_twitter_mentions("iPhone 15")
```

**Mix of free and demo APIs**

---

### 6. **RapidAPI** (Amazon Products)
**File**: `rapid_api_example.py`

Shows how to use RapidAPI for Amazon data:
```python
headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
}
response = requests.get(url, headers=headers, params=querystring)
```

**Requires API key** (free tier available at [rapidapi.com](https://rapidapi.com/))

---

## Running the Examples

### 1. Install dependencies:
```powershell
.\env\Scripts\Activate
pip install requests
```

### 2. Add API keys to .env (if using NewsAPI):
```
NEWS_API_KEY=your_key_here
```

### 3. Run any example:
```powershell
# No API key required:
python api_examples/github_api.py
python api_examples/weather_api.py
python api_examples/reddit_api.py
python api_examples/mixed_reviews_collector.py

# Requires free API key:
python api_examples/news_api.py

# Demo/guide only:
python api_examples/rapid_api_example.py
```

---

## Data Collection Methods

| Method | Pros | Cons | Use Case |
|--------|------|------|----------|
| **Kaggle** | Ready datasets, clean | Limited, static | Quick prototypes |
| **APIs** | Real-time, structured | Rate limits | Live dashboards |
| **Scraping** | Any website | Legal issues, blocks | No API available |
| **Manual** | Full control | Time-consuming | Small datasets |

---

## Best Practices

1. ✅ **Always check status code** before parsing
2. ✅ **Handle errors gracefully** (try-except blocks)
3. ✅ **Respect rate limits** (don't spam APIs)
4. ✅ **Save raw data** (JSON) before cleaning
5. ✅ **Use User-Agent** headers for web scraping
6. ✅ **Cache responses** to avoid repeated calls

---

## Popular Free APIs

| API | URL | Use Case |
|-----|-----|----------|
| **GitHub** | api.github.com | Developer data |
| **Open-Meteo** | api.open-meteo.com | Weather forecasts |
| **Reddit** | reddit.com/search.json | Social discussions |
| **NewsAPI** | newsapi.org | News articles |
| **JSONPlaceholder** | jsonplaceholder.typicode.com | Testing/demos |

---

## Next Steps - Homework ✅

### Phase 1: Testing (Use Postman)
1. ✅ Download Postman from https://postman.com
2. ✅ Test GitHub API (no key)
3. ✅ Test Weather API (no key)
4. ✅ Test Reddit API (no key)
5. ✅ Register for NewsAPI and test with key
6. ✅ Save responses as examples

### Phase 2: Python Implementation
1. ✅ Run all example scripts
2. ✅ Modify search queries for your products
3. ✅ Collect data with mixed reviews (positive + negative)
4. ✅ Combine API data with Kaggle datasets
5. ✅ Clean data using `data_cleaning.py`
6. ✅ Analyze sentiment using `sentiment_analysis.py`

### Phase 3: Find More APIs
1. ✅ Browse RapidAPI hub for product APIs
2. ✅ Test at least 3 new APIs in Postman
3. ✅ Create Python scripts for best ones
4. ✅ Document rate limits and requirements

---

## Resources

- **RapidAPI**: https://rapidapi.com/
- **Reddit API**: https://www.reddit.com/dev/api/
- **Requests Docs**: https://requests.readthedocs.io/
- **HTTP Status Codes**: https://httpstatuses.com/
