"""PRACTICAL 2: RETAIL SALES - Excel file (requires openpyxl)."""
from openpyxl import load_workbook

# ============================================================
# SECTION 1: CHECK A SINGLE EXCEL ROW
# ============================================================
def check_sale(sale_id, product_id, category, quantity, price, stock):
    if sale_id is None or product_id is None or category is None:
        return "Missing sale ID, product ID or category"
    if str(sale_id).strip() == "" or str(product_id).strip() == "" or str(category).strip() == "":
        return "Empty sale ID, product ID or category"
    if type(quantity) is not int or quantity <= 0:
        return "Quantity must be a positive whole number"
    if (type(price) is not int and type(price) is not float) or price < 0:
        return "Price must be zero or greater"
    if (type(stock) is not int and type(stock) is not float) or stock < 0:
        return "Stock cannot be negative"
    return ""


# ============================================================
# SECTION 2: SORT SALES MANUALLY BY REVENUE (HIGHEST FIRST)
# ============================================================
def sort_sales(sales):
    i = 0
    while i < len(sales):
        highest = i
        j = i + 1
        while j < len(sales):
            if sales[j]["revenue"] > sales[highest]["revenue"]:
                highest = j
            j += 1
        sales[i], sales[highest] = sales[highest], sales[i]
        i += 1


# ============================================================
# SECTION 3: OPEN THE EXCEL WORKBOOK
# ============================================================
def main():
    try:
        workbook = load_workbook("retail_sales.xlsx", read_only=True, data_only=True)
    except FileNotFoundError:
        print("ERROR: Put retail_sales.xlsx in this program's folder.")
        return
    if "Sales" not in workbook.sheetnames:
        print("ERROR: The workbook must contain a Sales worksheet.")
        workbook.close()
        return
    sheet = workbook["Sales"]

    # ========================================================
    # SECTION 4: READ EACH ROW AND VALIDATE THE VALUES
    # ========================================================
    sales = []
    errors = []
    category_totals = {}  # Category name -> total revenue
    low_stock = []
    row_number = 0
    for cells in sheet.iter_rows(values_only=True):
        row_number += 1
        if row_number == 1:  # First row contains headings.
            continue
        sale_id, product_id, category, quantity, price, stock = cells
        reason = check_sale(sale_id, product_id, category, quantity, price, stock)
        if reason != "":
            errors.append("Row " + str(row_number) + ": " + reason)
            continue
        revenue = quantity * price
        sales.append({"sale": sale_id, "product": product_id,
                      "category": category, "revenue": revenue})
        if category not in category_totals:
            category_totals[category] = 0
        category_totals[category] += revenue
        if stock < 10:
            low_stock.append({"product": product_id, "stock": stock})
    workbook.close()

    # ========================================================
    # SECTION 5: SORT THE SALES AND COUNT THE RECORDS
    # ========================================================
    sort_sales(sales)
    valid_count = 0
    for sale in sales:
        valid_count += 1
    invalid_count = 0
    for error in errors:
        invalid_count += 1
    low_count = 0
    for item in low_stock:
        low_count += 1

    # ========================================================
    # SECTION 6: SAVE A REPORT AND ERROR LOG
    # ========================================================
    with open("retail_report.txt", "w", encoding="utf-8") as report:
        report.write("RETAIL SALES REPORT\n")
        report.write(f"Valid: {valid_count} | Rejected: {invalid_count}\n\n")
        report.write("REVENUE BY CATEGORY\n")
        for category in category_totals:
            report.write(f"{category}: R{category_totals[category]:.2f}\n")
        report.write("\nTOP 10 SALES\n")
        count = 0
        for sale in sales:
            if count == 10:
                break
            count += 1
            report.write(f'{count}. {sale["sale"]} / {sale["product"]}: '
                         f'R{sale["revenue"]:.2f}\n')
        report.write(f"\nLow-stock transactions (stock below 10): {low_count}\n")
    with open("retail_errors.log", "w", encoding="utf-8") as error_file:
        for error in errors:
            error_file.write(error + "\n")

    # ========================================================
    # SECTION 7: DISPLAY THE RESULTS
    # ========================================================
    print("RETAIL SALES PROCESSOR")
    print("Accepted:", valid_count, "Rejected:", invalid_count)
    print("Low-stock transactions:", low_count)
    print("Files created: retail_report.txt, retail_errors.log")


# ============================================================
# SECTION 8: START THE PROGRAM
# ============================================================
if __name__ == "__main__":
    main()
