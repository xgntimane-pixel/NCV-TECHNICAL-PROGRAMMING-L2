
def amount_due(facility_code, hours):
  
    if facility_code == "squa":
        rate = 13.00
    elif facility_code == "swim":
        rate = 12.00
    elif facility_code == "gym":
        rate = 11.00
    elif facility_code == "wei":
        rate = 8.00


    amount = rate * hours
    return amount


def final_amount_due(amount):

    final_amount = amount + (amount * 0.14)
    return final_amount


def display(name, final_amount):

    print("\n----- PAYMENT DETAILS -----")
    print("Customer Name:", name)
    print("Final Amount Payable: R{:.2f}".format(final_amount))


def process_payment():
 
    name = input("Enter customer name: ")
    facility_code = input("Enter facility code (squa, swim, gym, wei): ")
    hours = float(input("Enter number of hours: "))


    amount = amount_due(facility_code, hours)


    final_amount = final_amount_due(amount)


    display(name, final_amount)



process_payment()
