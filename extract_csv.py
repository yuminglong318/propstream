import json
import pandas as pd  
import numpy as np  

from datetime import datetime  

def convert_datetime_to_string(data):  
    if isinstance(data, dict):  
        return {k: convert_datetime_to_string(v) for k, v in data.items()}  
    elif isinstance(data, list):  
        return [convert_datetime_to_string(element) for element in data]  
    elif isinstance(data, datetime):  
        return data.isoformat()  
    else:  
        return data  


def get_bankruptcy_json():  
    df = pd.read_excel('bankruptcy_total.xlsx')  

    # Iterate over the rows of the DataFrame  
    id_num = 1
    bankruptcy_list = []

    for row_index in range(len(df) - 1):  # Stop before last index to prevent out-of-bounds access  

        current_row_index = row_index
        current_row = df.iloc[current_row_index]  
        current_row_list = current_row.tolist()
        clean_list = ["" if isinstance(x, (float, int)) and np.isnan(x) else x for x in current_row_list]  
        current_row_list = clean_list
        
        if current_row_list[0] == "":
            continue 
        
        order1 = [
            "No", "id", "sale_date", "sale_amount"
        ]
        order2 = [
            "Status Date", "Price", "Days on Market", "Listing ID", "Listing Type"
        ]
        order3 = [
            "listingDate", "status", "amount", "pricePerSquareFoot", "daysOnMarket", "agentName", "brokerageName", "mlsNumber",
        ]
        order4 = [
            "Asset Involved", "Case Number", "Chapter", "County Name", "Dismissal Date", "Meeting Date / Time", "Original Chapter", "Document Type", "Conversion Date", "Recording Date"
        ]
        order5 = [
            "Debtor Alias 1 Name", "Debtor Alias 2 Name", "Debtor Alias 3 Name", "Attorney Address", "Attorney Name", "Spouse Name", "Spouse Address", "Souse Alias 1 Name", "Attorney Firm Name", "Judge Name", "Trustee Address", "Debtor Name", "Self Represented", "Discharge Date"
        ]
        order6 = [
            "Meeting Address", "Court Address"
        ]

        if id_num == int(current_row_list[0]):
            id_num += 1
            
            next_row = df.iloc[current_row_index + 1]
            next_row_list = next_row.tolist()
            clean_list = ["" if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
            next_row_list = clean_list
            
            current_dict = {}
            current_dict["MLS Details"] = {}
            current_dict["MLS Details"]["MLS History1"] = {}
            current_dict["Bankruptcy Details"] = {"Bankruptcy Information1": {}, "Parties Involved1": {}, "Bankruptcy Location1": {}}  
            
            # print("current_row_list - ", current_row_list)
            # print("next_row_list - ", next_row_list)

            for i in range(0, 9):
                if i < 4:
                    current_dict[order1[i]] = current_row_list[i] if not pd.isna(current_row_list[i]) else ""
                    # print(f"current_dict[{order1[i]}] - {current_dict[order1[i]]}")
                elif i < 9:
                    current_dict["MLS Details"][order2[i-9]] = current_row_list[i] if not pd.isna(current_row_list[i]) else ""
                    # print(f"current_dict['MLS Details'][{order2[i-9]}] - {current_dict['MLS Details'][order2[i-9]]}")
            
            mls_history_num = 1
            while True:
                empty_mlshistory = True
                current_dict["MLS Details"][f"MLS History{mls_history_num}"] = {}
                for i in range(9, 17):
                    current_dict["MLS Details"][f"MLS History{mls_history_num}"][order3[i-9]] = ""
                    if next_row_list[i] != "":
                        empty_mlshistory = False
                        current_dict["MLS Details"][f"MLS History{mls_history_num}"][order3[i-9]] = next_row_list[i]
                        # print(f"current_dict['MLS Details']['MLS History{mls_history_num}'][{order3[i-9]}] - {current_dict['MLS Details'][f'MLS History{mls_history_num}'][order3[i-9]]}")            
                mls_history_num += 1
                
                if empty_mlshistory == True:
                    if mls_history_num != 2:
                        del current_dict["MLS Details"][f"MLS History{mls_history_num - 1}"] 
                    break
                
                next_row = df.iloc[current_row_index + mls_history_num]
                next_row_list = next_row.tolist()
                clean_list = ["" if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
                next_row_list = clean_list
            
            bankruptcy_information_num = 1
            next_row = df.iloc[current_row_index + bankruptcy_information_num]
            next_row_list = next_row.tolist()
            clean_list = ["" if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
            next_row_list = clean_list
            
            while True:
                empty_bankruptcy_information = True
                current_dict["Bankruptcy Details"][f"Bankruptcy Information{bankruptcy_information_num}"] = {}
                for i in range(17, 27):
                    current_dict["Bankruptcy Details"][f"Bankruptcy Information{bankruptcy_information_num}"][order4[i-17]] = ""
                    if next_row_list[i] != "":
                        empty_bankruptcy_information = False
                        current_dict["Bankruptcy Details"][f"Bankruptcy Information{bankruptcy_information_num}"][order4[i-17]] = next_row_list[i]
                        # print(f"current_dict['bankruptcy Details']['bankruptcy Information{bankruptcy_information_num}'][{order4[i-17]}] - {current_dict['bankruptcy Details'][f'bankruptcy Information{bankruptcy_information_num}'][order4[i-17]]}")            
                bankruptcy_information_num += 1
                
                if empty_bankruptcy_information == True:
                    if bankruptcy_information_num != 2:
                        del current_dict["Bankruptcy Details"][f"Bankruptcy Information{bankruptcy_information_num - 1}"] 
                    break
                
                next_row = df.iloc[current_row_index + bankruptcy_information_num]
                next_row_list = next_row.tolist()
                clean_list = ["" if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
                next_row_list = clean_list
            
            parties_involved_num = 1
            next_row = df.iloc[current_row_index + parties_involved_num]
            next_row_list = next_row.tolist()
            clean_list = ["" if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
            next_row_list = clean_list
            
            while True:
                empty_party_information = True
                current_dict["Bankruptcy Details"][f"Parties Involved{parties_involved_num}"] = {}
                for i in range(27, 41):
                    current_dict["Bankruptcy Details"][f"Parties Involved{parties_involved_num}"][order5[i-27]] = ""
                    if next_row_list[i] != "":
                        empty_party_information = False
                        current_dict["Bankruptcy Details"][f"Parties Involved{parties_involved_num}"][order5[i-27]] =  next_row_list[i]
                        # print(f"current_dict['bankruptcy Details']['Recording Information{parties_involved_num}'][{order5[i-27]}] - {current_dict['bankruptcy Details'][f'Recording Information{parties_involved_num}'][order5[i-27]]}")            
                parties_involved_num += 1
                
                if empty_party_information == True:
                    if parties_involved_num != 2:
                        del current_dict["Bankruptcy Details"][f"Parties Involved{parties_involved_num - 1}"]
                    break
                
                next_row = df.iloc[current_row_index + parties_involved_num]
                next_row_list = next_row.tolist()
                clean_list = ["" if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
                next_row_list = clean_list

            location_information_num = 1
            next_row = df.iloc[current_row_index + location_information_num]
            next_row_list = next_row.tolist()
            clean_list = ["" if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
            next_row_list = clean_list
            
            while True:
                empty_location_information = True
                current_dict["Bankruptcy Details"][f"Bankruptcy Location{location_information_num}"] = {}
                for i in range(41, 43):
                    current_dict["Bankruptcy Details"][f"Bankruptcy Location{location_information_num}"][order6[i-41]] = ""
                    if next_row_list[i] != "":
                        empty_location_information = False
                        current_dict["Bankruptcy Details"][f"Bankruptcy Location{location_information_num}"][order6[i-41]] =  next_row_list[i]
                        # print(f"current_dict['bankruptcy Details']['Bankruptcy Location{location_information_num}'][{order6[i-41]}] - {current_dict['bankruptcy Details'][f'Bankruptcy Location{location_information_num}'][order6[i-41]]}")            
                location_information_num += 1
                
                if empty_location_information == True:
                    if location_information_num != 2:
                        del current_dict["Bankruptcy Details"][f"Bankruptcy Location{location_information_num - 1}"]
                    break
                
                next_row = df.iloc[current_row_index + location_information_num]
                next_row_list = next_row.tolist()
                clean_list = ["" if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
                next_row_list = clean_list

            current_dict["No"] = id_num
            bankruptcy_list += [current_dict]

    # File path where you want to save your JSON  
    file_path = 'propstream_bankruptcy.json'  # You can change this to your desired file path  
    bankruptcy_dict = {"bankruptcy": bankruptcy_list}
    bankruptcy_dict = convert_datetime_to_string(bankruptcy_dict)  

    # Writing list to a JSON file  
    with open(file_path, 'w') as file:  
        json.dump(bankruptcy_dict, file, indent=4)  # Use indent=4 for pretty-printing  

def get_lien_json():  
    df = pd.read_excel('lien_total.xlsx')  

    # Iterate over the rows of the DataFrame  
    id_num = 1 
    lien_list = []

    for row_index in range(len(df) - 1):  # Stop before last index to prevent out-of-bounds access  

        current_row_index = row_index
        current_row = df.iloc[current_row_index]  
        current_row_list = current_row.tolist()
        clean_list = [0 if isinstance(x, (float, int)) and np.isnan(x) else x for x in current_row_list]  
        current_row_list = clean_list
        
        if int(current_row_list[0]) == 0:
            continue 
        
        order1 = [
            "No", "id", "sale_date", "sale_amount"
        ]
        order2 = [
            "Status Date", "Price", "Days on Market", "Listing ID", "Listing Type"
        ]
        order3 = [
            "listingDate", "status", "amount", "pricePerSquareFoot", "daysOnMarket", "agentName", "brokerageName", "mlsNumber",
        ]
        order4 = [
            "Lien Amount", "Document Type", "Tax Type", "Refiling Last Day", "Federal Tax Area", "Installment Judgment", "Stay Ordered", "Judgment Entry Date", "Abstract Issue Date", "Interest Rate", "Back Support Amount", "Tax Period Max", "Tax Period Min", 
        ]
        order5 = [
            "Document Number", "Book / Page", "Recording Date", "Filing City, State", "Tax Date", "Court Case Number"
        ]
        order6 = [
            "Plaintiff 1", "Plaintiff 2", "Debtor Name", "Creditor Name", "Issuing Agency", "Foreign Address", "Foreign Country", "Tax Number", "Additional Judgment Debtors", "TaxPayer ID", "Creditor Contact Name"
        ]
        order7 = ["Original Book / Page", "Original Recording Date", "Original Document Number"]
        
        if id_num == int(current_row_list[0]):
            if id_num == 2509:
                break
            id_num += 1
            
            next_row = df.iloc[current_row_index + 1]
            next_row_list = next_row.tolist()
            clean_list = [0 if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
            next_row_list = clean_list
            
            current_dict = {}
            current_dict["MLS Details"] = {}
            current_dict["MLS Details"]["MLS History1"] = {}
            current_dict["Lien Details"] = {"Lien Information1": {}, "Recording Information1": {}, "Parties Involved1": {}, "Original lien Information": {}}  
            
            # print("current_row_list - ", current_row_list)
            # print("next_row_list - ", next_row_list)

            for i in range(0, 9):
                if i < 4:
                    current_dict[order1[i]] = current_row_list[i] if not pd.isna(current_row_list[i]) else ""
                    # print(f"current_dict[{order1[i]}] - {current_dict[order1[i]]}")
                elif i < 9:
                    current_dict["MLS Details"][order2[i-9]] = current_row_list[i] if not pd.isna(current_row_list[i]) else ""
                    # print(f"current_dict['MLS Details'][{order2[i-9]}] - {current_dict['MLS Details'][order2[i-9]]}")
            
            mls_history_num = 1
            while True:
                empty_mlshistory = True
                current_dict["MLS Details"][f"MLS History{mls_history_num}"] = {}
                for i in range(9, 17):
                    current_dict["MLS Details"][f"MLS History{mls_history_num}"][order3[i-9]] = ""
                    if next_row_list[i] != 0:
                        empty_mlshistory = False
                        current_dict["MLS Details"][f"MLS History{mls_history_num}"][order3[i-9]] = next_row_list[i]
                        # print(f"current_dict['MLS Details']['MLS History{mls_history_num}'][{order3[i-9]}] - {current_dict['MLS Details'][f'MLS History{mls_history_num}'][order3[i-9]]}")            
                mls_history_num += 1
                
                if empty_mlshistory == True:
                    if mls_history_num != 2:
                        del current_dict["MLS Details"][f"MLS History{mls_history_num - 1}"] 
                    break
                
                next_row = df.iloc[current_row_index + mls_history_num]
                next_row_list = next_row.tolist()
                clean_list = [0 if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
                next_row_list = clean_list
            
            lien_information_num = 1
            next_row = df.iloc[current_row_index + lien_information_num]
            next_row_list = next_row.tolist()
            clean_list = [0 if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
            next_row_list = clean_list
            
            while True:
                empty_lien_information = True
                current_dict["Lien Details"][f"Lien Information{lien_information_num}"] = {}
                for i in range(17, 30):
                    current_dict["Lien Details"][f"Lien Information{lien_information_num}"][order4[i-17]] = ""
                    if next_row_list[i] != 0:
                        empty_lien_information = False
                        current_dict["Lien Details"][f"Lien Information{lien_information_num}"][order4[i-17]] =  next_row_list[i]
                        # print(f"current_dict['Lien Details']['Lien Information{lien_information_num}'][{order4[i-17]}] - {current_dict['Lien Details'][f'Lien Information{lien_information_num}'][order4[i-17]]}")            
                lien_information_num += 1
                
                if empty_lien_information == True:
                    if lien_information_num != 2:
                        del current_dict["Lien Details"][f"Lien Information{lien_information_num - 1}"] 
                    break
                
                next_row = df.iloc[current_row_index + lien_information_num]
                next_row_list = next_row.tolist()
                clean_list = [0 if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
                next_row_list = clean_list
            
            recording_information_num = 1
            next_row = df.iloc[current_row_index + recording_information_num]
            next_row_list = next_row.tolist()
            clean_list = [0 if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
            next_row_list = clean_list
            
            while True:
                empty_recording_information = True
                current_dict["Lien Details"][f"Recording Information{recording_information_num}"] = {}
                for i in range(30, 36):
                    current_dict["Lien Details"][f"Recording Information{recording_information_num}"][order5[i-30]] = ""
                    if next_row_list[i] != 0:
                        empty_recording_information = False
                        current_dict["Lien Details"][f"Recording Information{recording_information_num}"][order5[i-30]] =  next_row_list[i]
                        # print(f"current_dict['Lien Details']['Recording Information{recording_information_num}'][{order5[i-30]}] - {current_dict['Lien Details'][f'Recording Information{recording_information_num}'][order5[i-30]]}")            
                recording_information_num += 1
                
                if empty_recording_information == True:
                    if recording_information_num != 2:
                        del current_dict["Lien Details"][f"Recording Information{recording_information_num - 1}"]
                    break
                
                next_row = df.iloc[current_row_index + recording_information_num]
                next_row_list = next_row.tolist()
                clean_list = [0 if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
                next_row_list = clean_list

            party_information_num = 1
            next_row = df.iloc[current_row_index + party_information_num]
            next_row_list = next_row.tolist()
            clean_list = [0 if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
            next_row_list = clean_list
            
            while True:
                empty_party_information = True
                current_dict["Lien Details"][f"Parties Involived{party_information_num}"] = {}
                for i in range(36, 47):
                    current_dict["Lien Details"][f"Parties Involived{party_information_num}"][order6[i-36]] = ""
                    if next_row_list[i] != 0:
                        empty_party_information = False
                        current_dict["Lien Details"][f"Parties Involived{party_information_num}"][order6[i-36]] =  next_row_list[i]
                        # print(f"current_dict['Lien Details']['Parties Involived{party_information_num}'][{order6[i-36]}] - {current_dict['Lien Details'][f'Parties Involived{party_information_num}'][order6[i-36]]}")            
                party_information_num += 1
                
                if empty_party_information == True:
                    if party_information_num != 2:
                        del current_dict["Lien Details"][f"Parties Involived{party_information_num - 1}"]
                    break
                
                next_row = df.iloc[current_row_index + party_information_num]
                next_row_list = next_row.tolist()
                clean_list = [0 if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
                next_row_list = clean_list
            
            original_lien_information_num = 1
            next_row = df.iloc[current_row_index + original_lien_information_num]
            next_row_list = next_row.tolist()
            clean_list = [0 if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
            next_row_list = clean_list
            
            while True:
                empty_original_lien_information = True
                current_dict["Lien Details"][f"Original Lien Information{original_lien_information_num}"] = {}
                for i in range(47, 50):
                    current_dict["Lien Details"][f"Original Lien Information{original_lien_information_num}"][order7[i-47]] = ""
                    if next_row_list[i] != 0:
                        empty_original_lien_information = False
                        current_dict["Lien Details"][f"Original Lien Information{original_lien_information_num}"][order7[i-47]] =  next_row_list[i]
                        # print(f"current_dict['Lien Details']['Original Lien Information{original_lien_information_num}'][{order7[i-47]}] - {current_dict['Lien Details'][f'Original Lien Information{original_lien_information_num}'][order7[i-47]]}")            
                original_lien_information_num += 1
                
                if empty_original_lien_information == True:
                    if original_lien_information_num != 2:
                        del current_dict["Lien Details"][f"Original Lien Information{original_lien_information_num - 1}"]
                    break
                
                next_row = df.iloc[current_row_index + original_lien_information_num]
                next_row_list = next_row.tolist()
                clean_list = [0 if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
                next_row_list = clean_list

            current_dict["No"] = id_num
            lien_list += [current_dict]

    # File path where you want to save your JSON  
    file_path = 'propstream_lien.json'  # You can change this to your desired file path  
    lien_dict = {"lien": lien_list}
    lien_dict = convert_datetime_to_string(lien_dict)  

    # Writing list to a JSON file  
    with open(file_path, 'w') as file:  
        json.dump(lien_dict, file, indent=4)  # Use indent=4 for pretty-printing  

def get_divorce_json():
    df = pd.read_excel('divorce_total.xlsx') 

    # Iterate over the rows of the DataFrame  
    id_num = 1 
    divorce_list = []
    for row_index in range(len(df) - 1):  # Stop before last index to prevent out-of-bounds access  
        current_row_index = row_index
        current_row = df.iloc[current_row_index]  
        current_row_list = current_row.tolist()
        clean_list = [0 if isinstance(x, (float, int)) and np.isnan(x) else x for x in current_row_list]  
        current_row_list = clean_list
        
        if int(current_row_list[0]) == 0:
            continue 
        
        order1 = [
            "No", "id", "sale_date", "sale_amount"
        ]
        order2 = [
            "Status Date", "Price", "Days on Market", "Listing ID", "Listing Type"
        ]
        order3 = [
            "listingDate", "status", "amount", "pricePerSquareFoot", "daysOnMarket", "agentName", "brokerageName", "mlsNumber",
        ]
        order4 = [
            "Document Number", "Recording Date", "Court Case Number", "Recording Book / Page", "Judgment Entry Date"
        ]
        order5 = [
            "Petitioner Name", "Respondent Name"
        ]
    
        if id_num == int(current_row_list[0]):
            id_num += 1

            next_row = df.iloc[current_row_index + 1]
            next_row_list = next_row.tolist()
            clean_list = [0 if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
            next_row_list = clean_list
            
            current_dict = {}
            current_dict["MLS Details"] = {}
            current_dict["MLS Details"]["MLS History1"] = {}
            current_dict["Divorce Details"] = {"Divorce Information1": {}, "Parties Involved1": {}}

            for i in range(0, 9):
                if i < 4:
                    current_dict[order1[i]] = current_row_list[i] if not pd.isna(current_row_list[i]) else ""
                    # print(f"current_dict[{order1[i]}] - {current_dict[order1[i]]}")
                elif i < 9:
                    current_dict["MLS Details"][order2[i-9]] = current_row_list[i] if not pd.isna(current_row_list[i]) else ""
                    # print(f"current_dict['MLS Details'][{order2[i-9]}] - {current_dict['MLS Details'][order2[i-9]]}")

            mls_history_num = 1
            while True:
                empty_mlshistory = True
                current_dict["MLS Details"][f"MLS History{mls_history_num}"] = {}
                for i in range(9, 17):
                    current_dict["MLS Details"][f"MLS History{mls_history_num}"][order3[i-9]] = ""
                    if next_row_list[i] != 0:
                        empty_mlshistory = False
                        current_dict["MLS Details"][f"MLS History{mls_history_num}"][order3[i-9]] = next_row_list[i]
                        # print(f"current_dict['MLS Details']['MLS History{mls_history_num}'][{order3[i-9]}] - {current_dict['MLS Details'][f'MLS History{mls_history_num}'][order3[i-9]]}")            
                mls_history_num += 1
                
                if empty_mlshistory == True:
                    if mls_history_num != 2:
                        del current_dict["MLS Details"][f"MLS History{mls_history_num - 1}"] 
                    break
                
                print("mls_history_num", mls_history_num)
                print("current_row_index", current_row_index)
                try:
                    next_row = df.iloc[current_row_index + mls_history_num]
                    next_row_list = next_row.tolist()
                    clean_list = [0 if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
                    next_row_list = clean_list
                except:
                    break
            
            divorce_information_num = 1
            
            next_row = df.iloc[current_row_index + divorce_information_num]
            next_row_list = next_row.tolist()
            clean_list = [0 if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
            next_row_list = clean_list
            
            while True:
                empty_divorce_information = True
                current_dict["Divorce Details"][f"Divorce Information{divorce_information_num}"] = {}
                for i in range(17, 22):
                    current_dict["Divorce Details"][f"Divorce Information{divorce_information_num}"][order4[i-17]] = ""
                    if next_row_list[i] != 0:
                        empty_divorce_information = False
                        current_dict["Divorce Details"][f"Divorce Information{divorce_information_num}"][order4[i-17]] =  next_row_list[i]
                        # print(f"current_dict['Divorce Details']['Divorce Information{divorce_information_num}'][{order4[i-17]}] - {current_dict['Divorce Details'][f'Divorce Information{divorce_information_num}'][order4[i-17]]}")            
                divorce_information_num += 1
                
                if empty_divorce_information == True:
                    if divorce_information_num != 2:
                        del current_dict["Divorce Details"][f"Divorce Information{divorce_information_num - 1}"]
                    break
                
                next_row = df.iloc[current_row_index + divorce_information_num]
                next_row_list = next_row.tolist()
                clean_list = [0 if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
                next_row_list = clean_list

            next_row = df.iloc[current_row_index + 1]
            next_row_list = next_row.tolist()
            clean_list = [0 if isinstance(x, (float, int)) and np.isnan(x) else x for x in next_row_list] 
            next_row_list = clean_list

            current_dict["Divorce Details"]["Parties Involved1"] = {}
            for i in range(22, 24):
                current_dict["Divorce Details"]["Parties Involved1"][order5[i-22]] = next_row_list[i] if not pd.isna(next_row_list[i]) else ""
                # print(f"current_dict['Divorce Details']['Parties Involved1'][{order5[i-22]}] - {current_dict['Divorce Details']['Parties Involved1'][order5[i-22]]}")

            current_dict["No"] = id_num
            divorce_list += [current_dict]

    # File path where you want to save your JSON  
    file_path = 'propstream_divorce.json'  # You can change this to your desired file path  
    divorce_dict = {"divorce": divorce_list}
    divorce_dict = convert_datetime_to_string(divorce_dict)  

    # Writing list to a JSON file  
    with open(file_path, 'w') as file:  
        json.dump(divorce_dict, file, indent=4)  # Use indent=4 for pretty-printing
# // get_lien_json()  
get_bankruptcy_json()