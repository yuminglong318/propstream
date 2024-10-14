import pandas as pd  

# Define the data as a list of dictionaries  
data = [  
    {  
        "Date": "02/01/2024",  
        "Status": "Sold",  
        "Price": "$2,150,000",  
        "Price/sqft": "$1,181.97",  
        "Days on Market": 56,  
        "Agent": "Ina Bloom",  
        "Agency": "Compass Florida Llc",  
        "MLS Number": "R10945365"  
    },  
    {  
        "Date": "12/28/2023",  
        "Status": "Pending",  
        "Price": "$2,299,000",  
        "Price/sqft": "$1,263.88",  
        "Days on Market": 1,  
        "Agent": "Ina Bloom",  
        "Agency": "Compass Florida Llc",  
        "MLS Number": "R10945365"  
    },  
    {  
        "Date": "01/06/2024",  
        "Status": "Pulled Off Market",  
        "Price": "$2,299,000",  
        "Price/sqft": "$1,263.88",  
        "Days on Market": 12,  
        "Agent": "Ina Bloom",  
        "Agency": "Compass Florida Llc",  
        "MLS Number": "RX-10945365"  
    },  
    {  
        "Date": "12/26/2023",  
        "Status": "Active - New Listing",  
        "Price": "$2,299,000",  
        "Price/sqft": "$1,263.88",  
        "Days on Market": 1,  
        "Agent": "Ina Bloom",  
        "Agency": "Compass Florida Llc",  
        "MLS Number": "RX-10945365"  
    },  
    {  
        "Date": "09/18/2024",  
        "Status": "Active - Price Adjustment",  
        "Price": "$2,500,000",  
        "Price/sqft": "$1,374.38",  
        "Days on Market": 2,  
        "Agent": "Serhant",  
        "Agency": "Serhant",  
        "MLS Number": "RX-11021704"  
    },  
    {  
        "Date": "09/17/2024",  
        "Status": "Coming Soon",  
        "Price": "$2,500,000",  
        "Price/sqft": "$1,374.38",  
        "Days on Market": 1,  
        "Agent": "Nicholas M Gonzalez",  
        "Agency": "Serhant",  
        "MLS Number": "RX-11021704"  
    },  
]  

# Convert the list of dictionaries into a pandas DataFrame  
df = pd.DataFrame(data)  

# Save the DataFrame to a CSV file  
df.to_csv('real_estate_data.csv', index=False)  

print("CSV file saved as 'real_estate_data.csv'")