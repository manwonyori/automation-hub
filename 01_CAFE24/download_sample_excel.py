"""
카페24 샘플 엑셀 다운로드
정확한 형식 확인용
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def main():
    print("=== 카페24 샘플 엑셀 다운로드 ===")
    
    # 다운로드 폴더 설정
    download_path = "C:\\Users\\8899y\\Documents\\cafe24\\downloads"
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # 다운로드 설정
    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    
    try:
        # 로그인
        driver.get("https://manwonyori.cafe24.com/admin")
        
        # 알림창 처리
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert.accept()
        except:
            pass
        
        # 로그인
        id_field = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='text']"))
        )
        id_field.send_keys("manwonyori")
        
        password_field = driver.find_element(By.XPATH, "//input[@type='password']")
        password_field.send_keys("happy8263!")
        password_field.send_keys(Keys.RETURN)
        
        WebDriverWait(driver, 10).until(
            lambda d: "admin" in d.current_url and "login" not in d.current_url
        )
        print("로그인 완료")
        
        # 엑셀 관리 페이지로 이동
        driver.get("https://manwonyori.cafe24.com/disp/admin/shop1/product/ProductExcelManage")
        time.sleep(2)
        
        # 팝업 닫기
        for i in range(3):
            try:
                close_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'close')] | //span[text()='×']")
                close_btn.click()
                time.sleep(0.3)
            except:
                break
        
        print("샘플 파일 찾는 중...")
        
        # 샘플 다운로드 링크 찾기
        sample_links = [
            "//a[contains(., '샘플')]",
            "//a[contains(., 'sample')]",
            "//a[contains(., '양식')]",
            "//a[contains(., '다운로드')]",
            "//button[contains(., '샘플')]",
            "//button[contains(., '양식')]"
        ]
        
        for link_xpath in sample_links:
            try:
                sample_link = driver.find_element(By.XPATH, link_xpath)
                if sample_link.is_displayed():
                    print(f"샘플 링크 발견: {sample_link.text}")
                    sample_link.click()
                    print("샘플 다운로드 시작")
                    time.sleep(3)
                    break
            except:
                continue
        
        # 또는 엑셀 다운로드 탭으로 이동
        try:
            download_tab = driver.find_element(By.XPATH, "//a[contains(., '엑셀 다운로드')] | //button[contains(., '엑셀 다운로드')]")
            download_tab.click()
            print("엑셀 다운로드 탭 클릭")
            time.sleep(2)
            
            # 상품 데이터 다운로드
            download_btn = driver.find_element(By.XPATH, "//button[contains(., '다운로드')] | //input[@value='다운로드']")
            download_btn.click()
            print("상품 데이터 다운로드 시작")
            time.sleep(5)
        except:
            print("다운로드 옵션을 찾을 수 없습니다")
        
        print(f"다운로드 폴더 확인: {download_path}")
        
        # 다운로드된 파일 확인
        files = os.listdir(download_path)
        if files:
            print("다운로드된 파일:")
            for file in files:
                print(f"  - {file}")
        else:
            print("다운로드된 파일 없음")
        
        print("10초 후 종료...")
        time.sleep(10)
        
    except Exception as e:
        print(f"오류: {e}")
        time.sleep(10)
    
    finally:
        driver.quit()
        print("완료")

if __name__ == "__main__":
    main()