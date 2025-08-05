"""
카페24 상품목록에서 상품 다운로드
https://manwonyori.cafe24.com/disp/admin/shop1/product/productmanage
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
    print("=== 카페24 상품목록 다운로드 ===")
    
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
        
        # 상품관리 페이지로 이동
        print("상품관리 페이지로 이동...")
        driver.get("https://manwonyori.cafe24.com/disp/admin/shop1/product/productmanage")
        time.sleep(3)
        
        # 팝업 닫기
        for i in range(3):
            try:
                close_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'close')] | //span[text()='×']")
                close_btn.click()
                time.sleep(0.3)
            except:
                break
        
        print(f"현재 URL: {driver.current_url}")
        
        # P00000IB 상품 검색
        print("P00000IB 상품 검색...")
        try:
            # 검색 필드 찾기
            search_fields = [
                "//input[@name='keyword']",
                "//input[@name='search_keyword']",
                "//input[@name='product_code']",
                "//input[@placeholder='상품코드']",
                "//input[@placeholder='검색어']",
                "//input[@type='text'][1]"
            ]
            
            search_field = None
            for field_xpath in search_fields:
                try:
                    search_field = driver.find_element(By.XPATH, field_xpath)
                    if search_field.is_displayed():
                        search_field.clear()
                        search_field.send_keys("P00000IB")
                        print("검색어 입력: P00000IB")
                        break
                except:
                    continue
            
            # 검색 버튼 클릭
            search_buttons = [
                "//button[contains(., '검색')]",
                "//input[@value='검색']",
                "//button[@type='submit']",
                "//input[@type='submit']"
            ]
            
            for btn_xpath in search_buttons:
                try:
                    search_btn = driver.find_element(By.XPATH, btn_xpath)
                    if search_btn.is_displayed():
                        search_btn.click()
                        print("검색 실행")
                        break
                except:
                    continue
            
            time.sleep(3)
        except:
            print("검색 실패, 전체 목록에서 진행")
        
        # 다운로드 버튼 찾기
        print("다운로드 옵션 찾는 중...")
        download_options = [
            "//a[contains(., '엑셀 다운로드')]",
            "//button[contains(., '엑셀 다운로드')]",
            "//a[contains(., 'Excel')]",
            "//button[contains(., 'Excel')]",
            "//a[contains(., '다운로드')]",
            "//button[contains(., '다운로드')]",
            "//input[@value='엑셀 다운로드']",
            "//input[@value='다운로드']",
            "//img[@alt='엑셀 다운로드']",
            "//span[contains(., '엑셀')]"
        ]
        
        download_clicked = False
        for option_xpath in download_options:
            try:
                elements = driver.find_elements(By.XPATH, option_xpath)
                for element in elements:
                    if element.is_displayed():
                        print(f"다운로드 옵션 발견: {element.text or element.get_attribute('value') or '버튼'}")
                        element.click()
                        download_clicked = True
                        print("다운로드 시작...")
                        break
                if download_clicked:
                    break
            except:
                continue
        
        if not download_clicked:
            print("다운로드 버튼을 찾을 수 없습니다")
            print("페이지에서 수동으로 확인이 필요합니다")
        
        # 다운로드 대기
        time.sleep(5)
        
        # 다운로드된 파일 확인
        files = os.listdir(download_path)
        excel_files = [f for f in files if f.endswith(('.csv', '.xls', '.xlsx'))]
        
        if excel_files:
            print("\n다운로드된 파일:")
            for file in excel_files:
                file_path = os.path.join(download_path, file)
                size = os.path.getsize(file_path) / 1024  # KB
                print(f"  - {file} ({size:.1f} KB)")
                
                # 최신 파일 찾기
                if file.endswith('.csv'):
                    latest_file = max([os.path.join(download_path, f) for f in excel_files if f.endswith('.csv')], key=os.path.getctime)
                    print(f"\n최신 CSV 파일: {os.path.basename(latest_file)}")
                    
                    # CSV 내용 일부 확인
                    try:
                        with open(latest_file, 'r', encoding='utf-8-sig') as f:
                            lines = f.readlines()[:5]
                            print("\nCSV 파일 미리보기:")
                            for i, line in enumerate(lines):
                                if i == 0:
                                    print(f"헤더: {line.strip()}")
                                else:
                                    print(f"데이터 {i}: {line.strip()}")
                    except Exception as e:
                        print(f"파일 읽기 오류: {e}")
        else:
            print("다운로드된 파일이 없습니다")
        
        print("\n작업 완료! 10초 후 종료...")
        time.sleep(10)
        
    except Exception as e:
        print(f"오류: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(10)
    
    finally:
        driver.quit()
        print("브라우저 종료")

if __name__ == "__main__":
    main()