# Async Outline manager sdk

> Thanks for the reverse engineering and docs project:
> https://github.com/jadolg/outline-vpn-api 
> Autor: @[jadolg](https://github.com/jadolg/)

# Example:

```python
from outline_sdk import OutlineClient

# Setup the access with the API URL (Use the one provided to you after the server setup)
client = OutlineClient(
    url="https://127.0.0.1:51083/xlUG4F5BBft4rSrIvDSWuw/",  # <--- `/` is required 
    cert_sha256="4EFF7BB90BCE5D4A172D338DC91B5B9975E197E39E3FA4FC42353763C4E58765"
)

# Get all access URLs on the server
for key in await client.get_keys():
    print(key)

# Create a new key
new_key = await client.create_key()

# Rename it
await client.rename_key(1, "new_key")

# Delete it
await client.delete_key(1)

# Set a monthly data limit for a key (20MB)
await client.add_data_limit(1, 1000 * 1000 * 20)

# Remove the data limit
await client.delete_data_limit(1)
```

