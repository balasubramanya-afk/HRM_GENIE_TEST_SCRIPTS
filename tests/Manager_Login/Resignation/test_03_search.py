import random
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_resignation

def test_team_resignation_search(page):
    # ==========================================
    # PART 1: Login and Navigate to Resignation
    # ==========================================
    # We use role="Manager" for the manager login module
    login_and_navigate_to_resignation(page, role="Manager")
    page.wait_for_timeout(3000)
    
    # 2. Click on "Team Resignation" tab
    page.get_by_role("button", name="Team Resignation").click()
    page.wait_for_timeout(2000)
    
    # Check if there are any records first
    empty_state = page.locator("text=No records found")
    if empty_state.count() > 0:
        print("No records found in the Team Resignation table. Cannot test dynamic search. Skipping...")
        _screenshot(page, "test_03_team_search_empty")
        return
        
    # Give the table a moment to fully render
    page.wait_for_timeout(2000)
    
    # Scrape all rows to find existing IDs and Names
    rows = page.locator("tbody tr")
    count = rows.count()
    
    data_list = []
    for i in range(count):
        row = rows.nth(i)
        emp_id = row.locator("td").nth(0).inner_text().strip()
        
        # We try to get the p tag, but if it doesn't exist, we fallback to just the inner_text
        name_cell = row.locator("td").nth(1)
        if name_cell.locator("p").count() > 0:
            emp_name = name_cell.locator("p").first.inner_text().strip()
        else:
            emp_name = name_cell.inner_text().strip()
            
        data_list.append({"id": emp_id, "name": emp_name})
        
    assert len(data_list) > 0, "No rows found in the table!"

    # Pick 1 random row to test
    sampled_data = random.sample(data_list, min(1, len(data_list)))
    emp = sampled_data[0]
    
    # Dynamic search data: 1 ID and 1 Name
    search_data = [
        {"query": emp["id"], "expected": emp["name"]},
        {"query": emp["name"], "expected": emp["id"]}
    ]
    
    search_input = page.get_by_placeholder("Search by name or ID")
    reset_button = page.get_by_text("Reset Filters")
    
    for i, item in enumerate(search_data):
        query = item["query"]
        expected_text = item["expected"]
        
        # Search for the query
        search_input.click()
        search_input.fill(query)
        search_input.press("Enter")
        page.wait_for_timeout(2000) # Wait for API response/filtering
        
        # Verify the expected data appears in the filtered results
        expect(page.get_by_text(expected_text).first).to_be_visible()
        expect(page.get_by_text(query).first).to_be_visible()
        
        # Take screenshot at the time it searched
        _screenshot(page, f"test_03_team_search_{i+1}")
        
        # Only click Reset Filters if it's NOT the last search
        if i < len(search_data) - 1:
            reset_button.click()
            page.wait_for_timeout(2000) # Wait for table to reload
            
            # Clear search input for the next iteration if it is not cleared automatically
            search_input.fill("")
