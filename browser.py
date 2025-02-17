import time
import requests
import functools

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from gui import winReponse

def check_server_ready(url, retries=10, delay=1):
    for _ in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            time.sleep(delay)
    return False

@functools.cache
def configure_chrome_options(url):
    chrome_options = Options()
    # chrome_options.add_argument("--auto-open-devtools-for-tabs")  # Remove this line to prevent DevTools from opening
    chrome_options.add_argument("--log-level=3")  # Suppress logs
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-infobars")  # Disable "Chrome is being controlled by automated test software" infobar
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable "Chrome is being controlled by automated test software" infobar
    chrome_options.add_argument(f"--app={url}")  # Open in app mode
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    return chrome_options

def add_loading_overlay(driver):
    driver.execute_script("""
        const createOverlay = (id, zIndex, backgroundColor) => {
            const overlay = document.createElement('div');
            overlay.style.position = 'fixed';
            overlay.style.top = '0';
            overlay.style.left = '0';
            overlay.style.width = '100%';
            overlay.style.height = '100%';
            overlay.style.zIndex = zIndex;
            overlay.style.backgroundColor = backgroundColor;
            overlay.id = id;
            document.body.appendChild(overlay);
        };

        createOverlay('loading-blocker', '9999', 'rgba(0, 0, 0, 0.000000001)');  // Transparent background
        createOverlay('loading-mask', '9998', 'rgba(255, 255, 255, 1)');  // Opaque white background
    """)

def remove_elements(driver):
    driver.execute_script("""
        const elementsToRemove = [
            '.leaflet-control-container',
            '.timeofday.largeclock',
            '.compass_surface.compass_SE.compass',
            '.hitbar',
            '.chatinput',
            '.chat',
            '.markerIcon16x16'
        ];
        elementsToRemove.forEach(selector => {
            const element = document.querySelector(selector);
            if (element) {
                element.remove();
            }
        });
        document.querySelectorAll('img').forEach(img => {
            if (img.src.includes('smp.qwerta.fr') && img.src.endsWith('.png')) {
                img.style.display = 'none';
            }
        });
    """)

def remove_loading_mask(driver):
    driver.execute_script("""
        const mask = document.getElementById('loading-mask');
        if (mask) {
            mask.remove();
        }
    """)

@functools.cache
def serviceChromeDriverManager():
    return Service(ChromeDriverManager().install())

def main(URL, ls):
    """
    if not check_server_ready(URL):
        raise RuntimeError("Il y a un problème avec l'url donner")
    """

    chrome_options = configure_chrome_options(URL)
    service = serviceChromeDriverManager()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(URL)
        add_loading_overlay(driver)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".leaflet-control-container")))
        remove_elements(driver)
        remove_loading_mask(driver)

        position = driver.get_window_position()
        size = driver.get_window_size()
        position["x"] = int(position["x"] + size["width"] * 0.50)
        position["y"] = int(position["y"] + size["height"] * 0.80)

        response = winReponse(ls, position)

    finally:
        driver.quit()
    
    return response

if __name__ == "__main__":
    URL = "https://smp.qwerta.fr/?worldname=world&mapname=surface&zoom=6&x=6&y=64&z=-10"
    ls = ["fromage", "chat", "loup", "rat"]

    main(URL, ls)
