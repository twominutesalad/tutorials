from expiringdict import ExpiringDict # The expiringdict lib is developed by mailgun
import time

cache = ExpiringDict(max_len=100, max_age_seconds=10)

cache["key"] = "value"

print("Adding a key value pair...")
print(cache.get("key"))
print("Waiting 10s for expiry. Python should return \"None\".")

time.sleep(5)
cache["key1"] = "value1"
time.sleep(5)

print(cache.get("key"))

if cache.get("key") == None:
	print("Key value pair expired.")
	#print(cache.get("key1"))


keystr = "key"

if keystr in cache:
	print("True")