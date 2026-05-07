"""
============================================
WebDriver Fixture Module
============================================
Supports:
- Chrome local execution
- Selenium Grid execution
- Parallel execution
- Headless mode
- Jenkins compatibility
"""

import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utils.logger import get_logger
from utils.config_reader import get_browser_config

logger = get_logger(__name__)


# ============================================
# EXECUTION SETTINGS
# ============================================

# False = Local execution
# True  = Selenium Grid execution
USE_GRID = True

# Selenium Grid URL
GRID_URL = "http://localhost:4444/wd/hub"


# ============================================
# DRIVER FACTORY
# ============================================

def create_driver(browser_name: str = None, headless: bool = None):

    config = get_browser_config()

    browser = (browser_name or config.get("name", "chrome")).lower()

    is_headless = (
        headless if headless is not None
        else config.get("headless", False)
    )

    window_size = config.get("window_size", "1920,1080")

    implicit_wait = config.get("implicit_wait", 10)

    page_load_timeout = config.get("page_load_timeout", 30)

    logger.info("=" * 60)
    logger.info(f"Creating {browser.upper()} driver")
    logger.info(f"Headless Mode: {is_headless}")
    logger.info(f"Selenium Grid: {USE_GRID}")
    logger.info("=" * 60)

    # ============================================
    # CHROME
    # ============================================

    if browser == "chrome":

        options = webdriver.ChromeOptions()

        # Browser Options
        options.add_argument("--start-maximized")

        options.add_argument(f"--window-size={window_size}")

        options.add_argument("--disable-notifications")

        options.add_argument("--disable-popup-blocking")

        options.add_argument("--disable-dev-shm-usage")

        options.add_argument("--no-sandbox")

        options.add_argument("--disable-gpu")

        options.add_argument("--remote-allow-origins=*")

        options.add_experimental_option(
            "excludeSwitches",
            ["enable-logging"]
        )

        # Headless
        if is_headless:
            options.add_argument("--headless=new")

        # ============================================
        # SELENIUM GRID EXECUTION
        # ============================================

        if USE_GRID:

            logger.info("Running on Selenium Grid")

            driver = webdriver.Remote(
                command_executor=GRID_URL,
                options=options
            )

        # ============================================
        # LOCAL EXECUTION
        # ============================================

        else:

            logger.info("Running on Local Chrome")

            driver_path = ChromeDriverManager().install()

            if not driver_path.lower().endswith("chromedriver.exe"):

                candidate = os.path.join(
                    os.path.dirname(driver_path),
                    "chromedriver.exe"
                )

                if os.path.exists(candidate):
                    driver_path = candidate

            driver = webdriver.Chrome(
                service=ChromeService(driver_path),
                options=options
            )

    # ============================================
    # EDGE
    # ============================================

    elif browser == "edge":

        options = webdriver.EdgeOptions()

        options.add_argument(f"--window-size={window_size}")

        if is_headless:
            options.add_argument("--headless=new")

        driver = webdriver.Edge(
            service=EdgeService(
                EdgeChromiumDriverManager().install()
            ),
            options=options
        )

    # ============================================
    # INVALID BROWSER
    # ============================================

    else:

        raise ValueError(
            f"Unsupported browser: {browser}"
        )

    # ============================================
    # DRIVER CONFIGURATION
    # ============================================

    driver.implicitly_wait(implicit_wait)

    driver.set_page_load_timeout(page_load_timeout)

    logger.info(f"{browser.upper()} driver created successfully")

    return driver
