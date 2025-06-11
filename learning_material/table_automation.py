# Example 1: Basic printTable function
def printTable(data, widths):
    for row in data:
        formatted_row = []
        for i, item in enumerate(row):
            formatted_row.append(str(item).rjust(widths[i]))
        print(' | '.join(formatted_row))

# Test data
sales_data = [
    ['Name', 'Sales', 'Bonus'],
    ['Alice', 1250, 125],
    ['Bob', 890, 89],
    ['Charlie', 2340, 234]
]

print("Right-aligned table:")
printTable(sales_data, [8, 6, 5])

print("\n" + "="*30 + "\n")

# Example 2: Demonstrating rjust, ljust, center
text = "Python"
print("Original:", repr(text))
print("Right (10):", repr(text.rjust(10)))
print("Left (10):", repr(text.ljust(10)))
print("Center (10):", repr(text.center(10)))

print("\nWith custom padding:")
print("Right (10, '-'):", repr(text.rjust(10, '-')))
print("Left (10, '.'):", repr(text.ljust(10, '.')))
print("Center (10, '*'):", repr(text.center(10, '*')))

print("\n" + "="*30 + "\n")

# Example 3: Strip custom padding
messy_data = "***Python***"
print("Original:", repr(messy_data))
print("strip('*'):", repr(messy_data.strip('*')))
print("lstrip('*'):", repr(messy_data.lstrip('*')))
print("rstrip('*'):", repr(messy_data.rstrip('*')))

print("\n" + "="*30 + "\n")

# Example 4: Complete table with padding cleanup
def printFormattedTable(raw_data, col_widths):
    print("Processing table data:")
    
    for row in raw_data:
        clean_row = []
        formatted_row = []
        
        for i, item in enumerate(row):
            # Clean the data
            clean_item = str(item).strip()
            clean_row.append(clean_item)
            
            # Format with right alignment
            formatted_item = clean_item.rjust(col_widths[i])
            formatted_row.append(formatted_item)
        
        print(f"Clean: {clean_row}")
        print(f"Table: {' | '.join(formatted_row)}")
        print()

# Messy data with extra spaces
messy_table = [
    [' Product ', ' Price ', ' Stock '],
    ['  Laptop  ', ' $899 ', '  15  '],
    [' Mouse', '$25  ', ' 50'],
    ['Keyboard ', ' $75', '8   ']
]

print("Formatted table with cleanup:")
printFormattedTable(messy_table, [10, 8, 6])