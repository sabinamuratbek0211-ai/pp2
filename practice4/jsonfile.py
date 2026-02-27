import json


with open(r"C:\Users\sabin\OneDrive\Pictures\Documents\pp2_2026\practice4\sample-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

interfaces = data.get("imdata", [])


print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':20} {'Speed':6} {'MTU':6}")
print("-" * 80)


for item in interfaces[:3]:
    attrs = item["l1PhysIf"]["attributes"]
    dn = attrs.get("dn", "")
    descr = attrs.get("descr", "")
    speed = attrs.get("speed", "")
    mtu = attrs.get("mtu", "")

    print(f"{dn:50} {descr:20} {speed:6} {mtu:6}")