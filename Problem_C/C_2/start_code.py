from collections import defaultdict
from datetime import datetime
import math
import numpy as np

def get_revenue_by_category(records):
    """Process sales records and return total revenue per category."""

    # Step 1: Validate records using list comprehension
    required_keys = {"transaction_id", "date", "category", "unit_price", "quantity", "customer_id", "region", "payment_method"}
    valid_records = [
        record for record in records
        if required_keys.issubset(record) and record["unit_price"] is not None and record["quantity"] is not None
    ]

    # Step 2: Group by category and compute stats
    category_data = defaultdict(lambda: {
        "revenues": [],
        "prices": [],
        "quantities": [],
        "customers": set(),
        "regions": set(),
    })

    for record in valid_records:
        cat = record["category"]
        revenue = record["unit_price"] * record["quantity"]

        category_data[cat]["revenues"].append(revenue)
        category_data[cat]["prices"].append(record["unit_price"])
        category_data[cat]["quantities"].append(record["quantity"])
        category_data[cat]["customers"].add(record["customer_id"])
        category_data[cat]["regions"].add(record["region"])

    # Step 3: Compute detailed statistics per category
    result = {}
    for cat, data in category_data.items():
        revenues = np.array(data["revenues"], dtype=np.float64)
        prices = np.array(data["prices"], dtype=np.float64)
        quantities = np.array(data["quantities"], dtype=np.float64)

        total_revenue = revenues.sum()
        avg_price = prices.mean()
        avg_quantity = quantities.mean()
        std_rev = revenues.std()
        median_rev = np.median(revenues)
        unique_customers = len(data["customers"])
        region_count = len(data["regions"])

        result[cat] = {
            "total_revenue": round(total_revenue, 2),
            "average_price": round(avg_price, 2),
            "average_quantity": round(avg_quantity, 2),
            "std_dev_revenue": round(std_rev, 2),
            "median_revenue": round(median_rev, 2),
            "unique_customers": unique_customers,
            "region_count": region_count,
        }

    return result