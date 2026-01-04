"""
Alpharxiv browser automation client using Playwright.

Handles:
- Persistent browser session (Google OAuth)
- Sending queries to the assistant
- Extracting responses and paper links
- Session management (new conversations per phase)
"""

import asyncio
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

try:
    from playwright.async_api import async_playwright, Browser, Page, BrowserContext
except ImportError:
    print("Playwright not installed. Run: pip install playwright && playwright install chromium")
    raise


@dataclass
class AlpharxivResponse:
    """Structured response from Alpharxiv."""
    text: str
    papers: list = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    raw_html: str = ""


class AlpharxivClient:
    """Browser automation client for Alpharxiv assistant."""
    
    ALPHARXIV_URL = "https://www.alphaxiv.org/assistant"
    PROFILE_DIR = Path.home() / ".research-verifier" / "browser-profile"
    
    # Multiple selector fallbacks for resilience to UI changes
    # Each entry is a list of selectors to try in order
    SELECTOR_FALLBACKS = {
        "input_box": [
            'textarea[placeholder*="Ask"]',
            'textarea[placeholder*="ask"]',
            'textarea[placeholder*="research"]',
            'textarea[placeholder*="question"]',
            'textarea[placeholder*="Search"]',
            'textarea',  # Last resort: any textarea
            'input[type="text"][placeholder*="Ask"]',
            'input[type="text"][placeholder*="Search"]',
            '[contenteditable="true"]',
        ],
        "send_button": [
            'button[type="submit"]:not([disabled])',
            'button:has(svg):not([disabled])',
            'button[aria-label*="send" i]:not([disabled])',
            'button[aria-label*="submit" i]:not([disabled])',
            'form button:not([disabled])',
        ],
        "response_container": [
            "div.prose",
            "div[class*='message']",
            "div[class*='assistant']",
            "div[class*='response']",
            "div[class*='chat']",
            "div[class*='answer']",
        ],
        "completion_indicator": [
            "button:has-text('Copy')",
            "[aria-label*='Copy']",
            "button:has-text('👍')",
            "button:has-text('👎')",
            "[class*='feedback']",
            "[class*='actions']",
        ],
    }

    # Legacy format for backward compatibility
    SELECTORS = {
        "input_box": 'textarea[placeholder*="Ask"]',
        "send_button": 'button[type="submit"], button:has(svg)',
        "response_container": "div.prose, div[class*='message']",
        "completion_indicator": "button:has-text('Copy'), [aria-label*='Copy']",
        "paper_link": "a[href*='arxiv.org']",
        "paper_pill": "button:has-text('...'), span[class*='truncate']",
    }
    
    def __init__(self, headless: bool = False, debug: bool = False):
        """
        Initialize client.

        Args:
            headless: Run browser in headless mode (False recommended for first login)
            debug: Enable debug mode for selector troubleshooting
        """
        self.headless = headless
        self.debug = debug
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self._playwright = None

        # Ensure profile directory exists
        self.PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    async def _find_element(self, element_type: str, timeout: int = 10000):
        """
        Try multiple selectors to find an element.

        Args:
            element_type: Key in SELECTOR_FALLBACKS (e.g., "input_box")
            timeout: Timeout per selector attempt in ms

        Returns:
            Element handle if found, None otherwise
        """
        selectors = self.SELECTOR_FALLBACKS.get(element_type, [])

        for selector in selectors:
            try:
                element = await self.page.wait_for_selector(
                    selector,
                    timeout=min(timeout, 3000),  # Quick check per selector
                    state="visible"
                )
                if element:
                    if self.debug:
                        print(f"  [DEBUG] Found {element_type} with selector: {selector}")
                    return element
            except Exception:
                continue

        return None

    async def _debug_page_structure(self):
        """Print debug info about the current page structure."""
        if not self.debug:
            return

        print("\n[DEBUG] Page URL:", self.page.url)
        print("[DEBUG] Page title:", await self.page.title())

        # Find all textareas
        textareas = await self.page.query_selector_all("textarea")
        print(f"[DEBUG] Found {len(textareas)} textarea elements:")
        for i, ta in enumerate(textareas):
            placeholder = await ta.get_attribute("placeholder") or "(no placeholder)"
            print(f"  [{i}] placeholder: {placeholder}")

        # Find all inputs
        inputs = await self.page.query_selector_all("input[type='text']")
        print(f"[DEBUG] Found {len(inputs)} text input elements:")
        for i, inp in enumerate(inputs):
            placeholder = await inp.get_attribute("placeholder") or "(no placeholder)"
            print(f"  [{i}] placeholder: {placeholder}")

        # Find all buttons
        buttons = await self.page.query_selector_all("button")
        print(f"[DEBUG] Found {len(buttons)} button elements")
    
    async def _ensure_browser(self):
        """Ensure browser is running with persistent context."""
        if self.context is not None:
            return
        
        self._playwright = await async_playwright().start()
        
        # Use persistent context to maintain Google login
        self.context = await self._playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.PROFILE_DIR),
            headless=self.headless,
            viewport={"width": 1280, "height": 900},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ]
        )
        
        # Get or create page
        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = await self.context.new_page()
    
    async def login_interactive(self):
        """
        Open browser for manual login.
        User logs into Google, then we save the session.
        """
        await self._ensure_browser()

        print("Opening Alpharxiv in browser...")
        print("Please log in with your Google account.")
        print("Press Enter in this terminal when you're logged in and see the assistant chat interface.")

        await self.page.goto(self.ALPHARXIV_URL)

        # Wait for user to complete login
        input("\n→ Press Enter after logging in... ")

        # Debug: show what's on the page
        await self._debug_page_structure()

        # Verify we're logged in by checking for the input box using fallback selectors
        input_box = await self._find_element("input_box", timeout=10000)

        if input_box:
            print("✓ Login verified. Session saved.")
        else:
            print("⚠ Could not find chat input. Possible reasons:")
            print("   1. You may not be logged in yet")
            print("   2. The page hasn't fully loaded")
            print("   3. The website UI has changed")
            print("\n   Try running with debug mode: rv login --debug")
            print("   Or manually verify you can see the chat interface in the browser.")

        await self.close()
    
    async def new_conversation(self):
        """Start a fresh conversation by navigating to the assistant URL."""
        await self._ensure_browser()
        await self.page.goto(self.ALPHARXIV_URL)

        # Wait for page to load
        await asyncio.sleep(2)

        # Debug output if enabled
        await self._debug_page_structure()

        # Try to find the input box with fallback selectors
        input_box = await self._find_element("input_box", timeout=30000)

        if not input_box:
            # Take a screenshot for debugging
            screenshot_path = self.PROFILE_DIR / "debug_screenshot.png"
            await self.page.screenshot(path=str(screenshot_path))
            print(f"\n⚠ Could not find chat input. Screenshot saved to: {screenshot_path}")
            print("This usually means:")
            print("   1. You need to log in first: rv login")
            print("   2. The website UI has changed")
            print("   3. There's a CAPTCHA or verification required")
            raise RuntimeError(
                f"Could not find chat input on {self.ALPHARXIV_URL}. "
                f"Run 'rv login' to authenticate or check {screenshot_path}"
            )

        # Small delay to ensure page is fully loaded
        await asyncio.sleep(1)
    
    async def query(self, question: str, timeout_seconds: int = 120) -> AlpharxivResponse:
        """
        Send a question and wait for response.

        Args:
            question: The question to ask
            timeout_seconds: Max wait time for response (default 120s for long queries)

        Returns:
            AlpharxivResponse with text and extracted papers
        """
        await self._ensure_browser()

        # Ensure we're on the right page
        if "alphaxiv.org" not in self.page.url:
            await self.new_conversation()

        # Find input box using fallback selectors
        input_box = await self._find_element("input_box", timeout=10000)
        if not input_box:
            raise RuntimeError("Could not find input box. Run 'rv login' first.")

        # Record baseline before submission to detect new responses
        baseline_text = await self._get_page_text()
        baseline_len = len(baseline_text)
        baseline_message_count = await self._count_messages()
        if self.debug:
            print(f"  [DEBUG] Baseline before submit: {baseline_len} chars, {baseline_message_count} messages")

        # For contenteditable elements, we need to click first, then type
        await input_box.click()
        await asyncio.sleep(0.1)

        # Clear existing text first
        await self.page.keyboard.press("Control+a")
        await self.page.keyboard.press("Backspace")
        await asyncio.sleep(0.1)

        # Type the question using page.keyboard for reliability
        # Using fill() or type() can be unreliable with contenteditable
        await self.page.keyboard.type(question, delay=2)  # Fast typing

        await asyncio.sleep(0.2)

        if self.debug:
            print(f"  [DEBUG] Typed {len(question)} chars")

        # Submit using Enter key - most reliable for chat interfaces
        await self.page.keyboard.press("Enter")

        if self.debug:
            print("  [DEBUG] Pressed Enter to submit")

        # Wait for response to complete
        print(f"  ⏳ Waiting for response (timeout: {timeout_seconds}s)...")

        # Wait for content to change from baseline, then stabilize
        await self._wait_for_new_response(baseline_len, baseline_message_count, timeout_seconds)

        # Extract response
        return await self._extract_response()

    async def _get_page_text(self) -> str:
        """Get current page text content."""
        try:
            main_content = await self.page.query_selector("main, [role='main'], #__next, .container")
            if main_content:
                return await main_content.inner_text()
            return await self.page.inner_text("body")
        except Exception:
            return ""

    async def _count_messages(self) -> int:
        """Count the number of message elements on the page."""
        try:
            messages = await self.page.query_selector_all("div[class*='prose']")
            return len(messages)
        except Exception:
            return 0

    async def _wait_for_new_response(self, baseline_len: int, baseline_msg_count: int, timeout_seconds: int = 120):
        """Wait for new message to appear and content to stabilize."""
        last_len = baseline_len
        stable_count = 0
        new_message_detected = False
        max_checks = timeout_seconds  # Check every 1 second

        if self.debug:
            print(f"  [DEBUG] Waiting for response (baseline: {baseline_len} chars, {baseline_msg_count} messages)...")

        for check_num in range(max_checks):
            await asyncio.sleep(1)
            try:
                current_len = len(await self._get_page_text())
                current_msg_count = await self._count_messages()

                # Phase 1: Wait for a NEW message element to appear
                if not new_message_detected:
                    if current_msg_count > baseline_msg_count:
                        new_message_detected = True
                        if self.debug:
                            print(f"  [DEBUG] New message appeared: {baseline_msg_count} -> {current_msg_count} messages")
                    elif current_len > baseline_len + 200:
                        # Fallback: significant content growth even without new message element
                        new_message_detected = True
                        if self.debug:
                            print(f"  [DEBUG] Content growth detected: {baseline_len} -> {current_len} chars")
                    elif check_num % 10 == 0 and self.debug:
                        print(f"  [DEBUG] Waiting... {current_len} chars, {current_msg_count} messages")
                    continue

                # Phase 2: Wait for content to stabilize
                if self.debug and check_num % 5 == 0:
                    print(f"  [DEBUG] Stabilizing: {current_len} chars, stable={stable_count}")

                if current_len == last_len:
                    stable_count += 1
                    if stable_count >= 3:  # Stable for 3 seconds
                        if self.debug:
                            print(f"  [DEBUG] Response complete: {current_len} chars, {current_msg_count} messages")
                        return
                else:
                    if self.debug and current_len != last_len:
                        print(f"  [DEBUG] Growing: {last_len} -> {current_len} chars")
                    stable_count = 0

                last_len = current_len

            except Exception as e:
                if self.debug:
                    print(f"  [DEBUG] Error: {e}")
                continue

        if self.debug:
            if not new_message_detected:
                print(f"  [DEBUG] Timeout: No new message detected. Submission may have failed.")
            else:
                print(f"  [DEBUG] Timeout reached, proceeding with extraction")
    
    async def _extract_response(self) -> AlpharxivResponse:
        """Extract the latest response text and paper links."""

        if self.debug:
            print("  [DEBUG] Extracting response...")

        # Try multiple selector strategies to find message containers
        message_selectors = [
            "div[class*='prose']",
            "div[class*='assistant']",
            "div[class*='message']",
            "div[class*='response']",
            "div[class*='markdown']",
            "div[class*='chat'] > div",
            "article",
            "[class*='content'] p",
        ]

        messages = []
        used_selector = None
        for selector in message_selectors:
            messages = await self.page.query_selector_all(selector)
            if messages and len(messages) > 0:
                used_selector = selector
                break

        if self.debug:
            print(f"  [DEBUG] Found {len(messages)} message elements with selector: {used_selector}")

        if not messages:
            # Last resort: get all text from main content
            if self.debug:
                print("  [DEBUG] No message containers found, extracting from main content")
            main = await self.page.query_selector("main, [role='main'], #__next")
            if main:
                text = await main.inner_text()
                return AlpharxivResponse(text=text, papers=[], raw_html="")
            return AlpharxivResponse(text="[No response found]", papers=[])

        # Get the last message (most recent response)
        last_message = messages[-1]

        # Extract text content
        text = await last_message.inner_text()

        if self.debug:
            print(f"  [DEBUG] Extracted {len(text)} chars from last message")
            print(f"  [DEBUG] Preview: {text[:200]}..." if len(text) > 200 else f"  [DEBUG] Content: {text}")

        # Extract paper links - look in the whole page, not just last message
        papers = []
        links = await self.page.query_selector_all("a[href*='arxiv.org'], a[href*='alphaxiv.org/abs']")

        for link in links:
            href = await link.get_attribute("href")
            title = await link.inner_text()

            # Extract arxiv ID from URL
            arxiv_match = re.search(r'(?:arxiv|alphaxiv)\.org/abs/(\d+\.\d+)', href or "")
            arxiv_id = arxiv_match.group(1) if arxiv_match else None

            if arxiv_id:  # Only add if we found a valid ID
                papers.append({
                    "title": title.strip() or f"Paper {arxiv_id}",
                    "url": href,
                    "arxiv_id": arxiv_id,
                })

        if self.debug:
            print(f"  [DEBUG] Found {len(papers)} paper links")

        # Get raw HTML for debugging/archival
        try:
            raw_html = await last_message.inner_html()
        except Exception:
            raw_html = ""

        return AlpharxivResponse(
            text=text,
            papers=papers,
            raw_html=raw_html
        )
    
    async def send_context_recap(self, recap: str):
        """
        Send a context recap as an actionable question.
        Alpharxiv needs a question to respond to, not just context.
        """
        # Convert recap into an actionable question
        context_prompt = f"""I'm researching the following topic. Please help me find relevant papers and summarize the current state of research.

{recap}

Based on this context, what are the most relevant recent papers (from the last 2 years) that I should review? Please provide specific paper recommendations with brief explanations of their relevance."""

        return await self.query(context_prompt)
    
    async def close(self):
        """Close browser gracefully."""
        if self.context:
            await self.context.close()
            self.context = None
            self.page = None
        
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None


# Standalone test
async def test_client():
    """Quick test of the client."""
    client = AlpharxivClient(headless=False)
    
    try:
        # First time: login
        # await client.login_interactive()
        
        # After login: test query
        await client.new_conversation()
        response = await client.query("What are the latest papers on transformer architecture improvements?")
        
        print("\n=== Response ===")
        print(response.text[:500])
        print(f"\n=== Papers ({len(response.papers)}) ===")
        for p in response.papers[:3]:
            print(f"  • {p['title']}: {p['url']}")
            
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(test_client())
