#!/usr/bin/env python3
"""price_check.py — monthly estimate for the pilot's resources from the Azure Retail Prices API (australiaeast, USD)."""
import json, urllib.request, urllib.parse
BASE = "https://prices.azure.com/api/retail/prices?$filter="
def q(flt):
    url = BASE + urllib.parse.quote(flt)
    with urllib.request.urlopen(url, timeout=30) as r: return json.load(r)["Items"], url
def show(title, flt, pick):
    items, url = q(flt)
    hits = [i for i in items if pick(i)]
    print(f"\n## {title}\n  source: {url}\n  matched {len(hits)} of {len(items)} items")
    for i in hits[:6]:
        monthly = i["retailPrice"] * 730 if i["unitOfMeasure"] == "1 Hour" else None
        print(f"  {i['productName']} | {i['skuName']} | {i['meterName']} | {i['retailPrice']} USD / {i['unitOfMeasure']}" + (f" | x730 = {monthly:.2f} USD/month" if monthly else ""))
show("App Service Linux B1 (plan wednesday-dashboard-plan)",
     "armRegionName eq 'australiaeast' and serviceName eq 'Azure App Service' and skuName eq 'B1' and priceType eq 'Consumption'",
     lambda i: "Linux" in i["productName"] and "Basic" in i["productName"])
show("Table storage LRS (wedndash storage account)",
     "armRegionName eq 'australiaeast' and serviceName eq 'Storage' and productName eq 'Tables' and priceType eq 'Consumption'",
     lambda i: i["skuName"] == "Standard LRS" and "Data Stored" in i["meterName"])
show("Table storage LRS transactions",
     "armRegionName eq 'australiaeast' and serviceName eq 'Storage' and productName eq 'Tables' and priceType eq 'Consumption'",
     lambda i: i["skuName"] == "Standard LRS" and "Operations" in i["meterName"])
