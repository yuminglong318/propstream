import asyncio  
import random
import ast  
import csv  
import os

from playwright.async_api import async_playwright  
from colorama import init, Fore

async def simulate_user_interaction(page):  
    # Simulating mouse movement  
    await page.mouse.move(200, 300)  
    await asyncio.sleep(random.uniform(0.1, 0.3))  
    await page.mouse.move(700, 600)  

    # Random waiting to mimic reading or thinking time  
    await asyncio.sleep(random.uniform(2, 5))  

async def manipulate_request(route):  
    request = route.request  
    headers = {  
        **request.headers,  
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",  
    }  
    await route.continue_(headers=headers)  
    
async def login(page):   
    # Go to the login page  
    await page.goto("https://login.propstream.com")  
    await page.wait_for_load_state("networkidle", timeout = 30000) 
    
    # Fill in the login details  
    await page.fill('input[name="username"]', "tc3181997@gmail.com") 
    await asyncio.sleep(random.uniform(1, 1.5))  
    await page.fill('input[name="password"]', "M@nunited0")  
    
    # Click the login button  
    await page.click('button[type="submit"]')  
    await page.wait_for_load_state("networkidle", timeout = 30000)  

    print("Passed login")
    # Wait for and click the "Proceed" button if it appears  
    try:  
        proceed_button_selector = 'text="Proceed"'  
        await page.wait_for_selector(proceed_button_selector, timeout=5000)   
        await page.click(proceed_button_selector)  
        print("Clicked the 'Proceed' button to resolve session conflict.")  
    except Exception as e:  
        print(f"Proceed button issue: {e}")  
    print("Passed proceed button")

async def go_search_page(page, id, detail_type):
    await page.goto("https://app.propstream.com/search")
    await page.wait_for_load_state("networkidle", timeout = 30000)   
    input_selector = 'input[aria-autocomplete="list"]'  
    await page.fill(input_selector, f"{id}")  
    await asyncio.sleep(random.uniform(5, 10))  
        
    # # Click the search button  
    # search_button_selector = '.src-app-Search-Header-style__NEcxl__iconSearch'  
    # await page.click(search_button_selector)  
    
    suggestion_selector = '#react-autowhatever-1--item-0'  
    await page.wait_for_selector(suggestion_selector)  

    # Click the suggestion  
    await page.click(suggestion_selector)  
    await page.wait_for_load_state("networkidle", timeout = 30000)  
    await asyncio.sleep(random.uniform(1, 1.5))  

    await page.click('text=Filter')  
    await page.wait_for_load_state("networkidle", timeout = 30000)    

    accordion_header_selector = 'text=Lien/Bankruptcy/Divorce Status' 
    await page.locator(accordion_header_selector).wait_for(state='visible')  
    # Attempt to click the accordion header  
    try:  
        await page.click(accordion_header_selector)  
        print("Accordion header clicked successfully.")  
    except Exception as e:  
        print(f"Error clicking accordion header: {e}")  
    await page.wait_for_load_state("networkidle", timeout = 30000)  
    
    input_selector = f'input[name="{detail_type}RecordingDateMin"]'  

    # Wait for the input field to be visible  
    await page.wait_for_selector(input_selector)  

    # Click on the input to focus it if necessary  
    await page.click(input_selector)  
    await page.wait_for_load_state("networkidle", timeout = 30000)  

    # Clear the field before typing  
    await page.fill(input_selector, '')  

    # Type in the new date value  
    await page.type(input_selector, "01/01/01")  

    # Verify that the value has been set correctly (optional debugging step)  
    assert await page.get_attribute(input_selector, 'value') == "01/01/01"  


    print("Search initiated.")  

    await page.wait_for_load_state("networkidle", timeout = 30000)   

async def extract_ids(page):  
    ids = []  
    try:  
        await page.wait_for_selector('.src-app-Search-Results-style__Dq3VN__item')  
        search_result_items = await page.query_selector_all('.src-app-Search-Results-style__Dq3VN__item a')  
        
        for item in search_result_items:  
            href = await item.get_attribute('href')  
            if href:  
                item_id = href.split('/')[-1]  
                ids.append(item_id)  
        
        if not ids:  
            print("No IDs found on this page.")  

    except Exception as e:  
        print(f"Error during ID extraction: {e}")  

    return ids  

async def click_next_button(page):  
    next_button_selector = 'button:has(span:has-text("Next"))'  
    try:  
        await page.wait_for_selector(next_button_selector, timeout=5000)  # Add timeout  
        await page.click(next_button_selector)  
        print("Clicked the 'Next' button.")  
        await page.wait_for_load_state('domcontentloaded')  # Wait for domcontentloaded state to ensure new page  
        return True  # To indicate the page load succeeded  
    except Exception as e:  
        print(f"Failed to click the 'Next' button or button not found: {e}")  
        return False  # To indicate the pagination cannot continue  

    await asyncio.sleep(random.uniform(2, 3))  

async def get_ids_one_zipcode(page, id, detail_type):
    await go_search_page(page, id, detail_type)
    
    all_ids = []  # List to collect all IDs  
    while True:  
        current_page_ids = []
        current_page_ids = await extract_ids(page)  
        all_ids.extend(current_page_ids)  
        
        # Break the loop if navigation to the next page isn't possible  
        if not await click_next_button(page):  
            break  
    
    odd_index_ids = [id for i, id in enumerate(all_ids) if i % 2 != 0]  

    # Join the filtered IDs into a single string with newline separation  
    ids_to_write = '\n'.join(odd_index_ids) + '\n'  

    # Write all the IDs to the file in one operation  
    with open(f"{id}_{detail_type}_id.txt", "w") as file:  
        file.write(ids_to_write)  
    
    print("All IDs have been saved to id.txt.")  

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
        ids = [33480, 33109, 33139, 33156, 33496, 33431, 33301, 33304, 33316, 33308] 
        detail_type = "divorce"
        for id in ids:
            await get_ids_one_zipcode(page, id, detail_type)
            print(Fore.RED + f"Extracted all ids for {id}" + Fore.RESET)
             
        await browser.close()  

asyncio.run(main())