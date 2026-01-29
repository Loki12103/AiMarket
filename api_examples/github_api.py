"""
GitHub API - GET Request Example
---------------------------------
Fetches user information from GitHub using public API
"""

import requests
import json

print("=" * 60)
print("GITHUB API - GET REQUEST")
print("=" * 60)
print()

# GitHub API endpoint
url = "https://api.github.com/users/octocat"

print(f"Fetching data from: {url}")
print()

# Make GET request
response = requests.get(url)

# Check status code
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print("✅ Success!")
else:
    print("❌ Failed!")
print()

# Parse JSON response
data = response.json()

# Display key information
print("=" * 60)
print("USER INFORMATION")
print("=" * 60)
print(f"Username: {data.get('login')}")
print(f"Name: {data.get('name')}")
print(f"Bio: {data.get('bio')}")
print(f"Public Repos: {data.get('public_repos')}")
print(f"Followers: {data.get('followers')}")
print(f"Following: {data.get('following')}")
print(f"Location: {data.get('location')}")
print(f"Created: {data.get('created_at')}")
print()

# Save full response to JSON file
output_file = "datasets/github_user_data.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print(f"✅ Full data saved to: {output_file}")
print()
