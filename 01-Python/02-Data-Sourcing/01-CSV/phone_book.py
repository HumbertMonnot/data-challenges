import csv

with open('data/phone_book.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        last_name = row['last_name']
        phone_number = row['phone_number']
        print(f"{last_name.capitalize()} : {phone_number}") 

