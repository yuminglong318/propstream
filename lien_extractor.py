import asyncio  
from playwright.async_api import async_playwright  

async def login(page):   
    # Go to the login page  
    await page.goto("https://login.propstream.com")  
    
    # Fill in the login details  
    await page.fill('input[name="username"]', "Izabela@off-market.io")  
    await page.fill('input[name="password"]', "Soas216096!")  
    
    # Click the login button  
    await page.click('button[type="submit"]')  

    # Wait for and click the "Proceed" button if it appears  
    try:  
        proceed_button_selector = 'text="Proceed"'  
        await page.wait_for_selector(proceed_button_selector, timeout=10000)   
        await page.click(proceed_button_selector)  
        print("Clicked the 'Proceed' button to resolve session conflict.")  
    except Exception as e:  
        print(f"Proceed button issue: {e}")  

    await page.wait_for_load_state("networkidle")  
    input_selector = 'input[aria-autocomplete="list"]'  
    await page.fill(input_selector, "33432")  
    
    await page.wait_for_timeout(1000)  # Wait briefly for suggestions  
    await page.wait_for_load_state("networkidle")   
    
    # # Click the search button  
    # search_button_selector = '.src-app-Search-Header-style__NEcxl__iconSearch'  
    # await page.click(search_button_selector)  
    
    suggestion_selector = '#react-autowhatever-1--item-0'  
    await page.wait_for_selector(suggestion_selector)  

    # Click the suggestion  
    await page.click(suggestion_selector)  

    await page.click('text=Filter')  
    await page.wait_for_load_state("networkidle")   

    accordion_header_selector = 'text=Lien/Bankruptcy/Divorce Status' 
    await page.locator(accordion_header_selector).wait_for(state='visible')  
    # Attempt to click the accordion header  
    try:  
        await page.click(accordion_header_selector)  
        print("Accordion header clicked successfully.")  
    except Exception as e:  
        print(f"Error clicking accordion header: {e}")  

    # await asyncio.sleep(120)  # Wait for 120 seconds asynchronously  
    
    input_selector = 'input[name="lienRecordingDateMin"]'  

    # Wait for the input field to be visible  
    await page.wait_for_selector(input_selector)  

    # Click on the input to focus it if necessary  
    await page.click(input_selector)  

    # Clear the field before typing  
    await page.fill(input_selector, '')  

    # Type in the new date value  
    await page.type(input_selector, "01/01/01")  

    # Verify that the value has been set correctly (optional debugging step)  
    assert await page.get_attribute(input_selector, 'value') == "01/01/01"  


    print("Search initiated.")  

    await page.wait_for_load_state("networkidle")  

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

async def main():  
    async with async_playwright() as pw:  
        browser = await pw.chromium.launch(headless=False)  # Set to True for headless mode  
        page = await browser.new_page()  
        await login(page)  
        
        all_ids = []  # List to collect all IDs  
        while True:  
            current_ids = await extract_ids(page)  
            all_ids.extend(current_ids)  
            
            # Break the loop if navigation to the next page isn't possible  
            if not await click_next_button(page):  
                break  
        
        odd_index_ids = [id for i, id in enumerate(all_ids) if i % 2 != 0]  

        # Join the filtered IDs into a single string with newline separation  
        ids_to_write = '\n'.join(odd_index_ids) + '\n'  

        # Write all the IDs to the file in one operation  
        with open("lien_id.txt", "w") as file:
            file.write(ids_to_write)  
        
        print("All IDs have been saved to lien_id.txt.")  

        await browser.close()  

asyncio.run(main())