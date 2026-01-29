# Postman Testing Guide for APIs

## What is Postman?

**Postman** is a tool for testing APIs without writing code. It's like a playground for API requests.

🔗 **Download**: https://www.postman.com/downloads/

---

## Why Use Postman?

1. ✅ **Visual Testing** - See requests and responses clearly
2. ✅ **No Code Required** - Test APIs before writing Python code
3. ✅ **Save Collections** - Organize and reuse API calls
4. ✅ **Environment Variables** - Manage API keys easily
5. ✅ **Collaboration** - Share collections with team

---

## Testing APIs in Postman

### 1. GitHub API (GET Request)

**URL**: `https://api.github.com/users/octocat`

**Method**: `GET`

**Steps**:
1. Open Postman
2. Create new request
3. Set method to `GET`
4. Enter URL: `https://api.github.com/users/octocat`
5. Click "Send"

**Expected Response** (200 OK):
```json
{
  "login": "octocat",
  "name": "The Octocat",
  "public_repos": 8,
  "followers": 9000
}
```

---

### 2. Weather API (GET with Parameters)

**URL**: `https://api.open-meteo.com/v1/forecast`

**Method**: `GET`

**Query Parameters**:
| Key | Value |
|-----|-------|
| latitude | 28.6139 |
| longitude | 77.2090 |
| current_weather | true |
| forecast_days | 1 |

**Steps**:
1. Create new GET request
2. Enter base URL: `https://api.open-meteo.com/v1/forecast`
3. Go to "Params" tab
4. Add parameters (key-value pairs)
5. Click "Send"

**Expected Response** (200 OK):
```json
{
  "current_weather": {
    "temperature": 25.5,
    "windspeed": 12.3,
    "winddirection": 180,
    "weathercode": 0,
    "time": "2025-12-16T10:00"
  }
}
```

---

### 3. Reddit API (GET with Query)

**URL**: `https://www.reddit.com/search.json`

**Method**: `GET`

**Query Parameters**:
| Key | Value |
|-----|-------|
| q | iPhone 15 |
| limit | 10 |
| sort | relevance |

**Headers** (Important!):
| Key | Value |
|-----|-------|
| User-Agent | Mozilla/5.0 (Windows NT 10.0; Win64; x64) |

**Steps**:
1. Create new GET request
2. Enter URL: `https://www.reddit.com/search.json`
3. Add query parameters
4. Go to "Headers" tab
5. Add User-Agent header
6. Click "Send"

---

### 4. NewsAPI (Requires API Key)

**URL**: `https://newsapi.org/v2/everything`

**Method**: `GET`

**Query Parameters**:
| Key | Value |
|-----|-------|
| q | iPhone 15 |
| apiKey | YOUR_API_KEY |
| from | 2025-12-09 |
| to | 2025-12-16 |
| language | en |
| sortBy | relevancy |

**Steps**:
1. Register at: https://newsapi.org/register
2. Copy API key
3. Create new GET request
4. Enter URL: `https://newsapi.org/v2/everything`
5. Add parameters (including apiKey)
6. Click "Send"

**Expected Response** (200 OK):
```json
{
  "status": "ok",
  "totalResults": 1234,
  "articles": [
    {
      "source": {"name": "TechCrunch"},
      "title": "iPhone 15 Review: Best Phone of 2024",
      "description": "Comprehensive review...",
      "url": "https://...",
      "publishedAt": "2025-12-15T10:30:00Z"
    }
  ]
}
```

---

### 5. RapidAPI Example

**URL**: `https://real-time-amazon-data.p.rapidapi.com/search`

**Method**: `GET`

**Query Parameters**:
| Key | Value |
|-----|-------|
| query | iPhone 15 |
| page | 1 |
| country | IN |

**Headers** (Required!):
| Key | Value |
|-----|-------|
| X-RapidAPI-Key | YOUR_RAPIDAPI_KEY |
| X-RapidAPI-Host | real-time-amazon-data.p.rapidapi.com |

**Steps**:
1. Sign up at: https://rapidapi.com/
2. Subscribe to "Real-Time Amazon Data" API
3. Copy API key
4. In Postman, create new GET request
5. Enter URL
6. Add query parameters
7. Go to "Headers" tab
8. Add both RapidAPI headers
9. Click "Send"

---

## Common HTTP Status Codes

| Code | Meaning | What to Do |
|------|---------|------------|
| **200** | ✅ Success | Request worked! |
| **400** | ❌ Bad Request | Check your parameters |
| **401** | ❌ Unauthorized | Check API key |
| **403** | ❌ Forbidden | No access permission |
| **404** | ❌ Not Found | Wrong URL/endpoint |
| **429** | ⚠️ Too Many Requests | Hit rate limit, wait |
| **500** | ❌ Server Error | API server problem |

---

## Postman Collections for This Project

### Import Ready-to-Use Collections

I've prepared these API tests for you:

1. **GitHub API Collection**
   - Get user info
   - Get repositories
   - Search users

2. **Weather API Collection**
   - Current weather
   - Hourly forecast
   - Multiple cities

3. **Reddit API Collection**
   - Search posts
   - Product discussions
   - Top posts

4. **News API Collection**
   - Everything endpoint
   - Top headlines
   - Sources

---

## Best Practices

### 1. **Use Environment Variables**
Store API keys in Postman environment, not in request:
```
{{NEWS_API_KEY}}
{{RAPIDAPI_KEY}}
```

### 2. **Organize Collections**
Group related requests:
```
📁 Product Review APIs
  ├─ Reddit Search
  ├─ News Articles
  └─ Amazon Products
```

### 3. **Test Before Coding**
Always test API in Postman first, then write Python code.

### 4. **Save Responses**
Save example responses for reference when writing parsers.

### 5. **Check Rate Limits**
Most free APIs have limits:
- GitHub: 60 requests/hour (unauthenticated)
- NewsAPI: 500 requests/day (free tier)
- Reddit: No official limit (be respectful)

---

## Converting Postman to Python

After testing in Postman:

1. Click "Code" button (right side)
2. Select "Python - Requests"
3. Copy generated code
4. Paste into your Python file

**Example**:
```python
import requests

url = "https://api.github.com/users/octocat"
response = requests.get(url)
print(response.json())
```

---

## Homework Checklist

- [ ] Download and install Postman
- [ ] Test GitHub API (no key needed)
- [ ] Test Weather API (no key needed)
- [ ] Test Reddit API (no key needed)
- [ ] Register for NewsAPI and test with your key
- [ ] Create a collection for "Product Review APIs"
- [ ] Save example responses for each API
- [ ] Convert one Postman request to Python code

---

## Useful APIs for Product Reviews

| API | Free? | Rate Limit | Best For |
|-----|-------|------------|----------|
| **Reddit** | ✅ Yes | ~60/min | Real user opinions |
| **NewsAPI** | ✅ Free tier | 500/day | Product news |
| **Twitter API** | ⚠️ Limited | Varies | Real-time buzz |
| **Best Buy** | ❌ Requires approval | - | Product reviews |
| **Amazon (RapidAPI)** | ⚠️ Paid | Varies | Product data |
| **Yelp** | ✅ Free tier | 500/day | Business reviews |

---

## Troubleshooting

### Problem: CORS Error
**Solution**: CORS doesn't affect Postman or Python, only browsers. Ignore it.

### Problem: 401 Unauthorized
**Solution**: Check if API key is correct and in right place (header vs param).

### Problem: 429 Too Many Requests
**Solution**: Wait a few minutes. Add delays in your code: `time.sleep(1)`

### Problem: Empty Response
**Solution**: Check if parameters are spelled correctly. Try example from docs.

---

## Next Steps

1. Test all APIs in Postman first
2. Once working, convert to Python
3. Collect data from multiple sources
4. Save to CSV files in `datasets/` folder
5. Clean data using `data_cleaning.py`
6. Analyze with `sentiment_analysis.py`

---

## Resources

- **Postman Learning**: https://learning.postman.com/
- **HTTP Status Codes**: https://httpstatuses.com/
- **API List**: https://github.com/public-apis/public-apis
- **RapidAPI Hub**: https://rapidapi.com/hub
