import random


def generate_records(n=500_000):
    random.seed(42)
    categories = ["Electronics", "Clothing", "Food", "Books", "Sports",
                  "Home", "Beauty", "Toys", "Garden", "Auto"]
    regions = ["North", "South", "East", "West", "Central"]
    methods = ["credit", "debit", "cash", "paypal"]

    records = []
    for i in range(n):
        records.append({
            "transaction_id": f"TXN-{i:07d}",
            "date": f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "category": random.choice(categories),
            "unit_price": round(random.uniform(1, 500), 2),
            "quantity": random.randint(1, 20),
            "customer_id": f"CUST-{random.randint(1, 10000):05d}",
            "region": random.choice(regions),
            "payment_method": random.choice(methods),
        })
    return records
