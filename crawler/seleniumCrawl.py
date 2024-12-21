from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    print("[DEBUG] Setting up WebDriver")  # 드라이버 초기화 시작
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    )
    service = Service(ChromeDriverManager().install())

    try:
        driver = webdriver.Chrome(service=service, options=options)
        print("[DEBUG] WebDriver setup successful")  # 드라이버 초기화 성공
        return driver
    except Exception as e:
        print(f"[DEBUG] WebDriver setup failed: {str(e)}")  # 드라이버 초기화 실패
        raise


def fetch_meta_data(driver, url):
    print(f"[DEBUG] Navigating to URL: {url}")  # 이동할 URL 출력
    driver.get(url)

    try:
        product_name = driver.execute_script(
            "return document.querySelector('meta[property=\"og:title\"]')?.getAttribute('content')"
        )
        print(f"[DEBUG] Product name: {product_name}")  # 제품 이름 확인

        product_image = driver.execute_script(
            "return document.querySelector('meta[property=\"og:image\"]')?.getAttribute('content')"
        )
        print(f"[DEBUG] Product image URL: {product_image}")  # 제품 이미지 URL 확인

        product_price = driver.execute_script(
            "return document.querySelector('meta[property=\"product:price:amount\"]')?.getAttribute('content')"
        )
        print(f"[DEBUG] Product price: {product_price}")  # 제품 가격 확인

        return {
            "product_name": product_name or "Unknown Product",
            "product_price": product_price or "0",
            "product_image": product_image or None,
        }
    except Exception as e:
        print(f"[DEBUG] Error fetching data: {str(e)}")  # 크롤링 중 발생한 오류 출력
        return {"error": f"Error fetching data: {str(e)}"}
    finally:
        driver.quit()
        print("[DEBUG] Driver quit successfully")  # 드라이버 종료 확인



def fetch_product_data(url):
    print(f"[DEBUG] Starting fetch_product_data with URL: {url}")  # 함수 호출 확인
    driver = setup_driver()

    try:
        return fetch_meta_data(driver, url)
    except Exception as e:
        print(f"[DEBUG] Unexpected error in fetch_product_data: {str(e)}")  # 예상치 못한 예외 출력
        return {"error": f"Unexpected error: {str(e)}"}
    finally:
        driver.quit()
        print("[DEBUG] WebDriver closed in fetch_product_data")  # 드라이버 종료 확인

