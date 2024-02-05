from decimal import Decimal
from data_engine_api.models import CustomerRevenue
from customer.models import Customer
from data_collector.models import Invoice


# Advance is the amount we are loaning the customer per invoice
def advance(invoice_value, haircut_percent):
    haircut_amount = invoice_value * haircut_percent *  Decimal(0.01)
    advance_amount = invoice_value - haircut_amount
    return Decimal(advance_amount)

# Expected fee is the fee to withdraw the money applied on the advance
def expected_fee(advance_amount, daily_fee_percent):
    # TODO: Add expected payment duration to formula?
    expected_fee = advance_amount * daily_fee_percent * Decimal(0.01)
    return Decimal(expected_fee)

# Function that receives a list of invoices and calculates the total values.
def sum_values_for_invoices(invoices):
    total_value = 0
    total_advance = 0
    total_fee = 0

    for invoice in invoices:
        total_value += invoice.value
        invoice_advance = advance(invoice.value, invoice.haircut_percent)
        total_advance += invoice_advance
        total_fee += expected_fee(invoice_advance, invoice.daily_fee_percent)
    return total_value, total_advance, total_fee


def total_calculation():
    customers = Customer.objects.all()
    for customer in customers:
        customer_total_calculation(customer)
    return

def customer_total_calculation(customer):
    invoices = Invoice.objects.filter(customer=customer)

    # We get a list of all the different revenue sources that the customer has
    revenue_sources = list(invoices.values_list('revenue_source', flat=True).distinct())
    customer_revenues = []
    for revenue_source in revenue_sources:
        # We calculate the total values per revenue source for this customer
        customer_source_revenue = source_customer_total_calculation(customer, invoices, revenue_source)
        customer_revenues.append(customer_source_revenue)
    
    if customer_revenues:
        # We create/update the Customer Revenue on batch to optimize db query calls.
        CustomerRevenue.objects.bulk_create(customer_revenues, 
                                            update_conflicts=True,
                                            unique_fields=['customer', 'revenue_source'],
                                            update_fields=['value', 'advance', 'expected_fee'])
    return

def source_customer_total_calculation(customer, invoices, revenue_source):
    invoices = invoices.filter(revenue_source=revenue_source)

    total_value, total_advance, total_fee = sum_values_for_invoices(invoices)

    customer_source_revenue = CustomerRevenue(
        customer=customer,
        revenue_source=revenue_source,
        value=total_value,
        advance=total_advance,
        expected_fee=total_fee
    )
    return customer_source_revenue
    


