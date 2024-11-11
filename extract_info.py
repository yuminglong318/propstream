import asyncio  
import ast  
import csv  
import os
import random  

from playwright.async_api import async_playwright  
from colorama import init, Fore

# Initialize colorama and header of csv
init(autoreset=True) 
current_header = []

def save_values_to_csv_without_lien(num, id, sale_date, sale_amount, list1, list2, file_path='divorce.csv'):  
    if sale_date == "" and sale_amount == "" and list1 == [] and list2 == [] :
        raise ValueError("Both sale_date and sale_amount must be provided")

    # Declare lists and all_keys of table headers
    list1_keys = ["Status Date", "Price", "Days on Market", "Listing ID", "Listing Type"]  
    list2_keys = ["listingDate", "status", "amount", "pricePerSquareFoot", "daysOnMarket", "agentName", "brokerageName", "mlsNumber"]

    all_keys = ['No', 'id', 'sale_date', 'sale_amount'] + list1_keys + list2_keys

    file_exists = os.path.exists(file_path)    

    # Write the header only if the file doesn't exist or new keys are detected
    with open(file_path, mode='w' if not file_exists else 'a', newline='') as file:  
        writer = csv.DictWriter(file, fieldnames = all_keys) 
        if not file_exists or not file_exists and all_keys:  
            writer.writeheader()  
  
        # Prepare the first row with static values and elements from list1  
        first_row = {key: '' for key in all_keys}  
        first_row['No'] = num  
        first_row['id'] = id  
        first_row['sale_date'] = sale_date  
        first_row['sale_amount'] = sale_amount 
        
        if list1:
            first_row["Status Date"] = list1[0]
            first_row["Price"] = list1[1]
            first_row["Days on Market"] = list1[2]
            first_row["Listing ID"] = list1[3]
            first_row["Listing Type"] = list1[4] 
        
        # Write initial static data and make placeholders for dynamic parts  
        
        writer.writerow(first_row)
        for i in range(len(list2)):  
            row = {key: '' for key in all_keys}  
            # Use data from list2 if available  
            if i < len(list2):  
                row.update(list2[i])  

            writer.writerow(row)

def save_values_to_csv(num, id, sale_date, sale_amount, list1, list2, list3, file_path='divorce.csv'):  
    # Declare lists and all_keys of table headers
    list1_keys = ["Status Date", "Price", "Days on Market", "Listing ID", "Listing Type"]  
    list2_keys = ["listingDate", "status", "amount", "pricePerSquareFoot", "daysOnMarket", "agentName", "brokerageName", "mlsNumber"]

    dynamic_keys = set()  
    list3_keys = {key for d in list3 for key in d.keys()} if list3 else set()  
    dynamic_keys.update(list3_keys)
    list3_keys = list(dynamic_keys)

    all_keys = ['No', 'id', 'sale_date', 'sale_amount'] + list1_keys + list2_keys + list3_keys

    # Import current header if it exists
    current_header = []
    file_exists = os.path.exists("current header.txt")
    if file_exists:
        with open('current header.txt', 'r') as file:  
            content = file.read().strip()  # Read and strip to remove any surrounding whitespace or newline  
            try:  
                current_header = ast.literal_eval(content)  
            except (ValueError, SyntaxError) as e:  
                print(f"Error converting file content to list: {e}")  

    # Read existing headers if file exists to update them with new keys for current header  
    file_exists = os.path.exists(file_path)    
    if file_exists:  
        with open(file_path, mode='r', newline='') as file:  
            existing_headers = next(csv.reader(file))  
            all_keys = list(dict.fromkeys(existing_headers + current_header + all_keys)) 
    
    for key in all_keys:
        if key not in current_header:
            current_header.append(key)
            
    with open('current header.txt', 'w') as file:  
        file.write(str(current_header))  

    # Write the header only if the file doesn't exist or new keys are detected
    with open(file_path, mode='w' if not file_exists else 'a', newline='') as file:  
        writer = csv.DictWriter(file, fieldnames = current_header) 
        if not file_exists or not file_exists and dynamic_keys:  
            writer.writeheader()  
 
        # Prepare the first row with static values and elements from list1  
        first_row = {key: '' for key in current_header}  
        first_row['No'] = num  
        first_row['id'] = id  
        first_row['sale_date'] = sale_date  
        first_row['sale_amount'] = sale_amount 
        
        if list1:
            first_row["Status Date"] = list1[0]
            first_row["Price"] = list1[1]
            first_row["Days on Market"] = list1[2]
            first_row["Listing ID"] = list1[3]
            first_row["Listing Type"] = list1[4] 
        
        # Write initial static data and make placeholders for dynamic parts  
        writer.writerow(first_row)

        # Determine the maximum length of list2 and list3 to iterate through  
        max_length = max(len(list2), len(list3))  

        for i in range(max_length):  
            row = {key: '' for key in current_header}  
            # Use data from list2 if available  
            if i < len(list2):  
                row.update(list2[i])  

            # Use data from list3 if available  
            if i < len(list3):  
                row.update(list3[i])  

            writer.writerow(row)  

def save_values_to_csv_with_divorce(num, id, sale_date, sale_amount, list1, list2, list3, file_path='divorce.csv'):  
    # Declare lists and all_keys of table headers
    list1_keys = ["Status Date", "Price", "Days on Market", "Listing ID", "Listing Type"]  
    list2_keys = ["listingDate", "status", "amount", "pricePerSquareFoot", "daysOnMarket", "agentName", "brokerageName", "mlsNumber"]

    dynamic_keys = set()  
    list3_keys = {key for d in list3 for key in d.keys()} if list3 else set()  
    dynamic_keys.update(list3_keys)
    list3_keys = list(dynamic_keys)

    all_keys = ['No', 'id', 'sale_date', 'sale_amount'] + list1_keys + list2_keys + list3_keys

    # Import divorce_current_header if it exists
    divorce_current_header = []
    file_exists = os.path.exists("divorce_current_header.txt")
    if file_exists:
        with open('divorce_current_header.txt', 'r') as file:  
            content = file.read().strip()  # Read and strip to remove any surrounding whitespace or newline  
            try:  
                divorce_current_header = ast.literal_eval(content)  
            except (ValueError, SyntaxError) as e:  
                print(f"Error converting file content to list: {e}")  

    # Read existing headers if file exists to update them with new keys for current header  
    file_exists = os.path.exists(file_path)    
    if file_exists:  
        with open(file_path, mode='r', newline='') as file:  
            existing_headers = next(csv.reader(file))  
            all_keys = list(dict.fromkeys(existing_headers + divorce_current_header + all_keys)) 
    
    for key in all_keys:
        if key not in divorce_current_header:
            divorce_current_header.append(key)
            
    with open('divorce_current_header.txt', 'w') as file:  
        file.write(str(divorce_current_header))  

    # Write the header only if the file doesn't exist or new keys are detected
    with open(file_path, mode='w' if not file_exists else 'a', newline='') as file:  
        writer = csv.DictWriter(file, fieldnames = divorce_current_header) 
        if not file_exists or not file_exists and dynamic_keys:  
            writer.writeheader()  
 
        # Prepare the first row with static values and elements from list1  
        first_row = {key: '' for key in divorce_current_header}  
        first_row['No'] = num  
        first_row['id'] = id  
        first_row['sale_date'] = sale_date  
        first_row['sale_amount'] = sale_amount 
        
        if list1:
            first_row["Status Date"] = list1[0]
            first_row["Price"] = list1[1]
            first_row["Days on Market"] = list1[2]
            first_row["Listing ID"] = list1[3]
            first_row["Listing Type"] = list1[4] 
        
        # Write initial static data and make placeholders for dynamic parts  
        writer.writerow(first_row)

        # Determine the maximum length of list2 and list3 to iterate through  
        max_length = max(len(list2), len(list3))  

        for i in range(max_length):  
            row = {key: '' for key in divorce_current_header}  
            # Use data from list2 if available  
            if i < len(list2):  
                row.update(list2[i])  

            # Use data from list3 if available  
            if i < len(list3):  
                row.update(list3[i])  

            writer.writerow(row)  

async def manipulate_request(route):  
    request = route.request  
    headers = {  
        **request.headers,  
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",  
    }  
    await route.continue_(headers=headers)  

async def simulate_user_interaction(page):  
    # Simulating mouse movement  
    await page.mouse.move(200, 300)  
    await asyncio.sleep(random.uniform(0.1, 0.3))  
    await page.mouse.move(700, 600)  

    # Random waiting to mimic reading or thinking time  
    await asyncio.sleep(random.uniform(2, 5))  

async def login(page):   
    # Go to the login page  
    await page.goto("https://login.propstream.com")
    await page.wait_for_load_state("networkidle", timeout = 30000)  
    await asyncio.sleep(random.uniform(1, 1.5))  

    # Fill in the login details  
    await page.fill('input[name="username"]', "thorinthorin@gmail.com") 
    await asyncio.sleep(random.uniform(1, 1.5))   
    await page.fill('input[name="password"]', "Wbmr*7*kpJWP*K4") 
    await asyncio.sleep(random.uniform(1, 1.5))  
    
    # Click the login button  
    await page.click('button[type="submit"]')  
    await page.wait_for_load_state("networkidle", timeout = 60000)  

    # Wait for and click the "Proceed" button if it appears  
    try:  
        proceed_button_selector = 'text="Proceed"'  
        await page.wait_for_selector(proceed_button_selector, timeout=5000)   
        await page.click(proceed_button_selector)  
        print("Clicked the 'Proceed' button to resolve session conflict.")  
    except Exception as e:  
        print(f"Proceed button issue: {e}")  

    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(1)

async def get_basic_info(page):
    sale_date = sale_amount = ""
    try:
        sale_date = await page.text_content("div:has-text('Sale Date') + div", timeout = 3000)  
    except Exception as e:
        print(f"Error occured while getting sale_date - {e}")

    try:
        sale_amount = await page.text_content("div:has-text('Sale Amount') + div", timeout = 3000)  
    except Exception as e:
        print(f"Error occured while getting sale_amount - {e}")

    await page.wait_for_load_state("networkidle")  
    await asyncio.sleep(1)
    return sale_date, sale_amount

async def get_mls_list(page):
    property_list, mls_history_list = [], []
    try:
        await page.click("li:has-text('MLS Details')")      
        await page.wait_for_load_state("networkidle")  
        await asyncio.sleep(1)
        try:
            details = {}
            labels = await page.query_selector_all('.src-components-GroupInfo-style__FpyDf__label')  
            values = await page.query_selector_all('.src-components-GroupInfo-style__sbtoP__value')  

            for label, value in zip(labels, values):  
                label_text = (await label.inner_text()).strip()  
                value_text = (await value.inner_text()).strip()   
                details[label_text] = value_text

            property_list = [  
                details.get("Status Date"),   
                details.get("Price"),
                details.get("Days on Market"),
                details.get("Listing ID"),   
                details.get("Listing Type")  
            ]
        except Exception as e:
            print(f"Error occured while getting property_list - {e}")

        try:
            # Find all rows in the table  
            rows = await page.query_selector_all('.ag-row')  

            for row in rows:  
                # Extract data from each cell  
                cells = await row.query_selector_all('.ag-cell .ag-cell-value')  

                # Collect data from cells if available  
                if len(cells) >= 8:  
                    row_data = {  
                        "listingDate": await cells[0].text_content(),  
                        "status": await cells[1].text_content(),  
                        "amount": await cells[2].text_content(),  
                        "pricePerSquareFoot": await cells[3].text_content(),  
                        "daysOnMarket": await cells[4].text_content(),  
                        "agentName": await cells[5].text_content(),  
                        "brokerageName": await cells[6].text_content(),  
                        "mlsNumber": await cells[7].text_content()  
                    }  
                    mls_history_list.append(row_data)                    
        except Exception as e:
            print(f"Error occured while getting mls_history - {e}")
    except Exception as e:
        pass
    
    await page.wait_for_load_state("networkidle", timeout = 30000)  
    return property_list, mls_history_list
    
async def get_lien_list(page):  
    lien_list = []  
    try:  
        await page.click("li:has-text('Lien Details')")      
        await page.wait_for_load_state("networkidle", timeout = 10000)  
        await asyncio.sleep(1)

        # Find all lien sections within the selected tab panel  
        lien_sections = await page.query_selector_all('.src-app-Property-Detail-style__E5HV8__page:not(.src-app-Property-Detail-style__E5HV8__page .src-app-Property-Detail-style__E5HV8__page)')  
        print(len(lien_sections))  
        lien_info_case1 = {}
        for panel in lien_sections:  
            # Initialize a dictionary for each lien  
            lien_info = {}  

            # Find all rows within a section  
            lien_details = await panel.query_selector_all('.src-app-Property-Detail-style__JNLud__row')  

            for detail in lien_details:  
                # Locate each label and value within the row  
                label_elements = await detail.query_selector_all('.src-components-GroupInfo-style__FpyDf__label')  
                value_elements = await detail.query_selector_all('.src-components-GroupInfo-style__sbtoP__value > div')  

                # Assign label-value pairs to the dictionary  
                for label_element, value_element in zip(label_elements, value_elements):  
                    label = await label_element.inner_text() if label_element else ""  
                    value = await value_element.inner_text() if value_element else ""  
                    lien_info[label.strip()] = value.strip()  
                    lien_info_case1[label.strip()] = value.strip()  

            # Add each lien's dictionary to the list  
            lien_list.append(lien_info)  

            if len(lien_sections) == 3:
                lien_list = []
                lien_list.append(lien_info_case1)

            print(Fore.BLUE + f"Extracted info successfully!!!" + Fore.RESET)

    except Exception as e:  
        print(f"Exception has occurred while getting lien_list: {e}")  

    await page.wait_for_load_state("networkidle", timeout = 10000)  
    for lien in lien_list:
        print(lien)
    return lien_list  

async def get_divorce_list(page):  
    divorce_list = []  
    try:  
        await page.click("li:has-text('Divorce Details')")      
        await page.wait_for_load_state("networkidle", timeout = 10000)  
        await asyncio.sleep(1)

        # Find all divorce sections within the selected tab panel  
        divorce_sections = await page.query_selector_all('.src-app-Property-Detail-style__E5HV8__page:not(.src-app-Property-Detail-style__E5HV8__page .src-app-Property-Detail-style__E5HV8__page)')  
        print(len(divorce_sections))  
        divorce_info_case1 = {}
        for panel in divorce_sections:  
            # Initialize a dictionary for each divorce  
            divorce_info = {}  

            # Find all rows within a section  
            divorce_details = await panel.query_selector_all('.src-app-Property-Detail-style__JNLud__row')  

            for detail in divorce_details:  
                # Locate each label and value within the row  
                label_elements = await detail.query_selector_all('.src-components-GroupInfo-style__FpyDf__label')  
                value_elements = await detail.query_selector_all('.src-components-GroupInfo-style__sbtoP__value > div')  

                # Assign label-value pairs to the dictionary  
                for label_element, value_element in zip(label_elements, value_elements):  
                    label = await label_element.inner_text() if label_element else ""  
                    value = await value_element.inner_text() if value_element else ""  
                    divorce_info[label.strip()] = value.strip()  
                    divorce_info_case1[label.strip()] = value.strip()  

            # Add each divorce's dictionary to the list  
            divorce_list.append(divorce_info)  

            if len(divorce_sections) == 3:
                divorce_list = []
                divorce_list.append(divorce_info_case1)

            print(Fore.BLUE + f"Extracted info successfully!!!" + Fore.RESET)

    except Exception as e:  
        print(f"Exception has occurred while getting divorce_list: {e}")  

    await page.wait_for_load_state("networkidle", timeout = 10000)  
    for divorce in divorce_list:
        print(divorce)
    return divorce_list  

async def get_bankruptcy_list(page):  
    bankruptcy_list = []  
    try:  
        await page.click("li:has-text('Bankruptcy Details')")      
        await page.wait_for_load_state("networkidle", timeout = 10000)  
        await asyncio.sleep(1)

        # Find all bankruptcy sections within the selected tab panel  
        bankruptcy_sections = await page.query_selector_all('.src-app-Property-Detail-style__E5HV8__page:not(.src-app-Property-Detail-style__E5HV8__page .src-app-Property-Detail-style__E5HV8__page)')  
        print(len(bankruptcy_sections))  
        bankruptcy_info_case1 = {}
        for panel in bankruptcy_sections:  
            # Initialize a dictionary for each bankruptcy  
            bankruptcy_info = {}  

            # Find all rows within a section  
            bankruptcy_details = await panel.query_selector_all('.src-app-Property-Detail-style__JNLud__row')  

            for detail in bankruptcy_details:  
                # Locate each label and value within the row  
                label_elements = await detail.query_selector_all('.src-components-GroupInfo-style__FpyDf__label')  
                value_elements = await detail.query_selector_all('.src-components-GroupInfo-style__sbtoP__value > div')  

                # Assign label-value pairs to the dictionary  
                for label_element, value_element in zip(label_elements, value_elements):  
                    label = await label_element.inner_text() if label_element else ""  
                    value = await value_element.inner_text() if value_element else ""  
                    bankruptcy_info[label.strip()] = value.strip()  
                    bankruptcy_info_case1[label.strip()] = value.strip()  

            # Add each bankruptcy's dictionary to the list  
            bankruptcy_list.append(bankruptcy_info)  

            if len(bankruptcy_sections) == 3:
                bankruptcy_list = []
                bankruptcy_list.append(bankruptcy_info_case1)

            print(Fore.BLUE + f"Extracted info successfully!!!" + Fore.RESET)

    except Exception as e:  
        print(f"Exception has occurred while getting bankruptcy_list: {e}")  

    await page.wait_for_load_state("networkidle", timeout = 10000)  
    for bankruptcy in bankruptcy_list:
        print(bankruptcy)
    return bankruptcy_list 

async def save_property_to_group(page):
    await page.click('.src-app-Property-Detail-style__LF8c8__buttons >> text="Save"')  

    await page.wait_for_load_state("networkidle", timeout = 30000)
    await page.click('.src-components-base-Button-style__SbPpX__button-blue.src-components-base-Button-style__KOYXx__large.btn.btn-primary')  

    await page.wait_for_load_state("networkidle", timeout = 30000)  
    await asyncio.sleep(1)

async def extract_info(page, num, id):  
    
    await page.goto(f'https://app.propstream.com/search/{id}')

    await page.wait_for_load_state("networkidle", timeout = 10000) 
    await asyncio.sleep(1)

    sale_date, sale_amount = await get_basic_info(page)
    await asyncio.sleep(random.uniform(1, 1.5))  
    property_list, mls_history_list = await get_mls_list(page)    
    # await asyncio.sleep(random.uniform(1, 1.5))  
    # lien_list = await get_lien_list(page)
    # await asyncio.sleep(random.uniform(1, 1.5))  
    # bankruptcy_list = await get_bankruptcy_list(page)
    await asyncio.sleep(random.uniform(1, 1.5))  
    divorce_list = await get_divorce_list(page)  
    # await asyncio.sleep(1)
    # bankruptcy_list = await get_bankruptcy_list(page)

    # print(property_list
    # print(divorce_list)
    # print(bankruptcy_list)
    # save_values_to_csv_without_lien(num, id, sale_date, sale_amount, property_list, mls_history_list)    
    # await asyncio.sleep(1)
    save_values_to_csv_with_divorce(num, id, sale_date, sale_amount, property_list, mls_history_list, divorce_list)
    print(Fore.RED + f"Extracted info for ID {id} - {num}" + Fore.RESET)
    print("_________________________________________________________")
    await page.wait_for_load_state("networkidle", timeout = 30000) 

async def main():  
    async with async_playwright() as pw:  
        browser = await pw.chromium.launch(headless=False, args=[  
            '--disable-blink-features=AutomationControlled',  # Helps to avoid detection  
        ])  
        
        context = await browser.new_context(  
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",  # Common User-Agent  
            viewport={'width': random.randint(1000, 1920), 'height': random.randint(700, 1080)}  # Random realistic viewport size  
        )  
        page = await context.new_page()  

        # Intercepting requests can simulate more human-like requests  
        await context.route('**/*', lambda route: asyncio.ensure_future(manipulate_request(route)))  

        await page.goto('https://your-website.com')  

        # Simulate realistic mouse movements  
        await simulate_user_interaction(page)  
        await login(page)  
        await asyncio.sleep(1)

        with open('ID/divorce_total.txt', 'r') as f:  
            # Read the content of the file  
            line = f.read().strip()  

            # Remove square brackets and single quotes, then splnum =it by comma  
            cleaned_line = line.strip('[]')  # Remove the outer brackets  
            cleaned_line = cleaned_line.replace("'", "")  # Remove single quotes  

            # Split the string by commas to form a list of IDs  
            ids = [id.strip() for id in cleaned_line.split(',')]  
            num = 150
            # Initialize num if it's not already set elsewhere  
            for id in ids:  
                num += 1
                retry_count = 0  # Track retry attempts for each id  
                success = False  # Track success status for each id  
                while retry_count < 2 and not success:  # Limit retries to avoid infinite loop  
                    try:  
                        await extract_info(page, num, id)  
                        success = True  # Mark as successful if no exception happens  
                        if (num % 50 == 0):
                            print(Fore.GREEN +  "Trying to group" + Fore.RESET)
                            try:
                                await save_property_to_group(page)
                                print(Fore.GREEN +  "Successfully saved to group" + Fore.RESET)
                            except Exception as e:  
                                print(Fore.GREEN +  f"Exception has occurred while Saving to Group: {e}."+ Fore.RESET)
                    except Exception as e:  
                        print(f"Exception has occurred while extracting info: {e}. Retrying the same ID.")  
                        retry_count += 1  
                        await browser.close()  
                        browser = await pw.chromium.launch(headless=False)  
                        page = await browser.new_page()  
                        await login(page)  
                        
                if not success:  
                    print(f"Failed to extract info for ID {id} after {retry_count} attempts.")

                if (num % 50 == 0):
                    raise

        await browser.close()

asyncio.run(main())