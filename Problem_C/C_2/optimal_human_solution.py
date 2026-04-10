def get_revenue_by_category(records):
    result = {}
    for record in records:
        cat = record["category"]
        revenue = record["unit_price"] * record["quantity"]
        if cat not in result:
            result[cat] = {"total_revenue": 0}
        result[cat]["total_revenue"] += revenue

    for cat in result:
        result[cat]["total_revenue"] = round(result[cat]["total_revenue"], 2)

    return result