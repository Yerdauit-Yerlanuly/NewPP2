import json

# Load the JSON data from the file
with open("sample.json") as file:
    data = json.load(file)

# Print the table header
print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<7} {'MTU':<7}")
print("-" * 80)

# Loop through the data and extract required fields
for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    dn = attributes["dn"]
    description = attributes["descr"] if attributes["descr"] else ""
    speed = attributes["speed"]
    mtu = attributes["mtu"]
    
    print(f"{dn:<50} {description:<20} {speed:<7} {mtu:<7}")
