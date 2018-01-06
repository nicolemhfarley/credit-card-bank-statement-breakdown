''' Program to categorize and break down expenses from credit card or bank statement.  Also visualize that breakdown in a graph '''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# load in CC statement as CSV file
df = pd.read_csv('credit_statement.csv')

# sum expenditures

net_spent = round(float(df.Debit.sum() - df.Credit.sum()), 2)
total_debit = round(float(df.Debit.sum()), 2)

def percent_by_category(expense_type):
# calculate percent of total expenditures by category
	percent = round(((expense_type/total_debit) * 100), 2)
	return percent

print("There are %i transactions in this statement." % df.Status.count()) 
print("Total expenditures from this statement equal $%r" % total_debit)

# create list/pattern/filter to select for grocery purchases 
groc_list = ['FRYS', 'WHOLE', 'COSTCO']

#### OR get list of grocery vendors from the user:
#groc_list = []
#groceries = input("Where do you shop for groceries?:")
#groceries = groceries.split()

#for i in groceries:
#	i = i.upper()	
#	groc_list.append(i)
 
groc_pattern = '|'.join(groc_list)

# count the number of grocery purchases, total spent, and percent of total spent

groc_count = df.Description.str.contains(groc_pattern).sum()
groc_bill = float(df.Debit[df['Description'].str.contains(groc_pattern)].sum())
groc_bill = round(groc_bill, 2)

print("You made %s grocery purchases totaling $%r." % (groc_count, groc_bill)) 
percent_groc = percent_by_category(groc_bill)
print("%r percent of your expenditures when to groceries. " % percent_groc)

# select only Amazon purchases

amazon_bill = float(df.Debit[df.Description.str.contains('AMAZON')].sum())
percent_amazon = percent_by_category(amazon_bill)
print("You spent $%r on Amazon.com which accounts for %r percent of total expenditures." % (amazon_bill, percent_amazon))

# using a different method than for groceries: calculate healthcare related costs

df['health'] = np.where(((df['Description'].str.contains('CVS') | df['Description'].str.contains('COBRA'))), df['Debit'], 0)
healthcare = round(df.health.sum(), 2)
print("You spent $" + str(healthcare) + " on healthcare.")
percent_health = percent_by_category(healthcare)

# Alphabetize df by Description column to group similar expenditures

df.sort_values(['Description', 'Debit'], ascending=[True, True], inplace=True)

other_bills = round(total_debit - amazon_bill - groc_bill - healthcare, 2)
print("Your other bills total $" + str(other_bills) + ".")
percent_other = percent_by_category(other_bills)

# create a pie chart to break down expenses by category

bills = {'groceries': groc_bill, 'Amazon.com': amazon_bill, 'health care': healthcare, 'other': other_bills}

print("Here is a visual breakdown of your expenditures for this month:")
_ = plt.pie([float(v) for v in bills.values()], labels=[k for k in bills.keys()], autopct=None, colors=None)
plt.show()




















