from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 브라우저 창 없이 실행
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    )
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def fetch_meta_data(driver, url):
    driver.get(url)

    try:
        # JavaScript 코드에서 정확한 구문 사용
        product_name = driver.execute_script(
            "return document.querySelector('meta[property=\"og:title\"]')?.getAttribute('content')"
        ) or "Unknown Product"

        product_image = driver.execute_script(
            "return document.querySelector('meta[property=\"og:image\"]')?.getAttribute('content')"
        )

        product_price = driver.execute_script(
            "return document.querySelector('meta[property=\"product:price:amount\"]')?.getAttribute('content') || '0'"
        )

        return {
            "product_name": product_name,
            "product_price": product_price,
            "product_image": product_image,
        }

    except Exception as e:
        return {"error": f"Error fetching data: {str(e)}"}

    finally:
        driver.quit()


def fetch_product_data(url):
    driver = setup_driver()
    try:
        return fetch_meta_data(driver, url)
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
    finally:
        driver.quit()
