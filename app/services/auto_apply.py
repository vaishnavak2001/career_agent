"""
Auto-Apply Service using Playwright
Handles form filling and submission automation
"""
from playwright.async_api import async_playwright
from typing import Dict, List
import asyncio

class AutoApplyService:
    def __init__(self):
        self.headless = True
    
    async def submit_application(self, job_url: str, form_data: Dict, files: Dict = None) -> Dict:
        """
        Submit a job application via browser automation.
        
        Args:
            job_url: URL of the job application page
            form_data: Dictionary of form field names/values
            files: Dictionary of file upload fields and paths
            
        Returns:
            {status: str, confirmation: str, screenshot: str|None}
        """
        result = {
            "status": "pending",
            "confirmation": "",
            "screenshot": None,
            "error": None
        }
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            page = await browser.new_page()
            
            try:
                # Navigate to job posting
                await page.goto(job_url, timeout=30000)
                
                # Wait for page to load
                await page.wait_for_load_state('networkidle', timeout=10000)
                
                # Look for apply button
                apply_button_selectors = [
                    'button:has-text("Apply")',
                    'a:has-text("Apply")',
                    'button:has-text("Submit Application")',
                    '[data-testid="apply-button"]'
                ]
                
                apply_button = None
                for selector in apply_button_selectors:
                    try:
                        apply_button = await page.wait_for_selector(selector, timeout=3000)
                        if apply_button:
                            break
                    except:
                        continue
                
                if not apply_button:
                    result["status"] = "failed"
                    result["error"] = "Could not find apply button"
                    return result
                
                # Click apply button
                await apply_button.click()
                await page.wait_for_load_state('networkidle', timeout=10000)
                
                # Fill form fields
                for field_name, field_value in form_data.items():
                    try:
                        # Try different input selectors
                        input_selectors = [
                            f'input[name="{field_name}"]',
                            f'input[id="{field_name}"]',
                            f'textarea[name="{field_name}"]',
                        ]
                        
                        for selector in input_selectors:
                            try:
                                await page.fill(selector, str(field_value), timeout=2000)
                                break
                            except:
                                continue
                    except Exception as e:
                        print(f"Could not fill field {field_name}: {e}")
                
                # Handle file uploads
                if files:
                    for field_name, file_path in files.items():
                        try:
                            file_input = await page.query_selector(f'input[type="file"][name="{field_name}"]')
                            if file_input:
                                await file_input.set_input_files(file_path)
                        except Exception as e:
                            print(f"Could not upload file for {field_name}: {e}")
                
                # Take screenshot before submission (for verification)
                screenshot_path = f"screenshots/before_submit_{hash(job_url)}.png"
                await page.screenshot(path=screenshot_path)
                result["screenshot"] = screenshot_path
                
                # SANDBOX MODE: Don't actually submit
                result["status"] = "sandbox_mode"
                result["confirmation"] = "Application prepared but not submitted (sandbox mode enabled)"
                
                # If live mode was enabled, we would:
                # submit_button = await page.wait_for_selector('button[type="submit"]')
                # await submit_button.click()
                # await page.wait_for_load_state('networkidle')
                # confirmation_text = await page.text_content('.confirmation-message')
                # result["confirmation"] = confirmation_text
                
            except Exception as e:
                result["status"] = "failed"
                result["error"] = str(e)
            finally:
                await browser.close()
        
        return result

auto_apply_service = AutoApplyService()
