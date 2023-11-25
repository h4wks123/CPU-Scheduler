from prettytable import PrettyTable

# Example data
referenceString = [1, 2, 3, 4]

# Create a PrettyTable
table = PrettyTable()

# Add columns to the table
column_names = ["Time"] + [f"{num}" for num in referenceString]
table.field_names = column_names

# Print the table
print(table)
