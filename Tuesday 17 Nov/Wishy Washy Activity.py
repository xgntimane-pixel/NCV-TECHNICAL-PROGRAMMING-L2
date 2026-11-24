import random

def generate_minutes():
    """Generate and return a random integer between 30 and 180 (inclusive)."""
    return random.randint(30, 180)

def calc_amount(machine_type, minutes):
    """
    Calculate the amount before VAT.
    Amount before VAT = Initial cost + (Hourly rate × Hours used)
    Fractional hours are charged proportionally.
    """
    hours = minutes / 60

    if machine_type.upper() == "A":
        initial = 50.00
        hourly = 30.00
    elif machine_type.upper() == "B":
        initial = 62.50
        hourly = 36.25
    else:  
        initial = 74.87
        hourly = 40.50

    amount = initial + (hourly * hours)
    return amount

def calc_total_amount(amount):
    """
    Calculate VAT (14%) and total payable.
    Returns both the VAT amount and the total payable.
    """
    vat = amount * 0.14
    total = amount + vat
    return vat, total

def display_summary(payments):
    """
    Display the daily summary statistics from the list of total payments.
    """
    if not payments:
        print("No payments to summarise.")
        return

    num_customers = len(payments)
    total_combined = sum(payments)
    average = total_combined / num_customers
    highest = max(payments)
    lowest = min(payments)

    print("\n" + "=" * 40)
    print("DAILY SUMMARY")
    print("=" * 40)
    print(f"Number of customers processed : {num_customers}")
    print(f"Combined amount payable       : R{total_combined:.2f}")
    print(f"Average payment per customer  : R{average:.2f}")
    print(f"Highest payment               : R{highest:.2f}")
    print(f"Lowest payment                : R{lowest:.2f}")
    print("=" * 40)

def process_payments():
    """
    Main function that processes customer payments.
    """
    num_customers = int(input("Enter the number of customers to process: "))
    payments = []

    for i in range(num_customers):
        print(f"\n--- Customer {i + 1} ---")
        name = input("Enter customer's name: ")
        machine_type = input("Enter machine type (A, B or C): ")

        minutes = generate_minutes()
        amount_before_vat = calc_amount(machine_type, minutes)
        vat, total_payable = calc_total_amount(amount_before_vat)

        payments.append(total_payable)

       
        print("\n---------- INVOICE ----------")
        print(f"Customer Name     : {name}")
        print(f"Machine Type      : {machine_type.upper()}")
        print(f"Minutes Used      : {minutes}")
        print(f"Amount before VAT : R{amount_before_vat:.2f}")
        print(f"VAT Amount        : R{vat:.2f}")
        print(f"Total Payable     : R{total_payable:.2f}")
        print("-----------------------------")

    
    display_summary(payments)


process_payments()