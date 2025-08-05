"""
카페24 상품 다운로드 후 가격 수정
1. 현재 상품 데이터 다운로드
2. P00000IB 상품의 가격만 수정
3. 수정된 파일 업로드
"""

import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def main():
    print("=== 카페24 상품 다운로드 및 가격 수정 ===")
    
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
        
        # 1단계: 엑셀 다운로드 탭 클릭
        print("1. 엑셀 다운로드 탭으로 이동...")
        try:
            download_tab = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(., '엑셀 다운로드')] | //button[contains(., '엑셀 다운로드')]"))
            )
            download_tab.click()
            time.sleep(2)
        except:
            print("엑셀 다운로드 탭을 찾을 수 없습니다")
        
        # 기존 파일 삭제
        for file in os.listdir(download_path):
            if file.startswith("product_") and file.endswith(".csv"):
                os.remove(os.path.join(download_path, file))
        
        # 2단계: 상품 다운로드
        print("2. 상품 데이터 다운로드...")
        try:
            # 상품코드 검색 필드 찾기
            search_field = driver.find_element(By.XPATH, "//input[@name='product_code'] | //input[@placeholder='상품코드']")
            search_field.clear()
            search_field.send_keys("P00000IB")
            print("상품코드 입력: P00000IB")
            
            # 검색 버튼 클릭
            search_btn = driver.find_element(By.XPATH, "//button[contains(., '검색')] | //input[@value='검색']")
            search_btn.click()
            time.sleep(2)
        except:
            print("상품 검색 스킵")
        
        # 다운로드 버튼 클릭
        download_btn = driver.find_element(By.XPATH, "//button[contains(., '다운로드')] | //input[@value='다운로드']")
        download_btn.click()
        print("다운로드 시작...")
        time.sleep(5)
        
        # 3단계: 다운로드된 파일 찾기
        files = [f for f in os.listdir(download_path) if f.endswith('.csv')]
        if not files:
            print("다운로드된 파일이 없습니다")
            return
        
        latest_file = max([os.path.join(download_path, f) for f in files], key=os.path.getctime)
        print(f"다운로드된 파일: {latest_file}")
        
        # 4단계: 파일 수정
        print("3. 가격 수정 중...")
        df = pd.read_csv(latest_file, encoding='utf-8-sig')
        
        # P00000IB 상품 찾기
        mask = df['상품코드'] == 'P00000IB'
        if mask.any():
            print(f"현재 가격: {df.loc[mask, '판매가'].values[0]}")
            df.loc[mask, '판매가'] = 13500
            print("새 가격: 13500")
            
            # 수정된 파일 저장
            modified_file = os.path.join(download_path, "price_updated.csv")
            df.to_csv(modified_file, index=False, encoding='utf-8-sig')
            print(f"수정된 파일 저장: {modified_file}")
        else:
            print("P00000IB 상품을 찾을 수 없습니다")
            return
        
        # 5단계: 엑셀 업로드 탭으로 이동
        print("4. 엑셀 업로드 탭으로 이동...")
        upload_tab = driver.find_element(By.XPATH, "//a[contains(., '엑셀 업로드')] | //button[contains(., '엑셀 업로드')]")
        upload_tab.click()
        time.sleep(2)
        
        # 6단계: 파일 업로드
        print("5. 수정된 파일 업로드...")
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        file_input.send_keys(modified_file)
        print("파일 선택 완료")
        
        # 업로드 버튼 클릭
        upload_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., '업로드')] | //input[@value='업로드']"))
        )
        upload_btn.click()
        print("업로드 실행")
        
        time.sleep(5)
        print("SUCCESS: 가격 수정 완료!")
        
        # 결과 확인
        try:
            result_msg = driver.find_element(By.XPATH, "//*[contains(text(), '완료')] | //*[contains(text(), '성공')]")
            print(f"결과: {result_msg.text}")
        except:
            print("결과 확인 필요")
        
        time.sleep(10)
        
    except Exception as e:
        print(f"오류: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(10)
    
    finally:
        driver.quit()
        print("완료")

if __name__ == "__main__":
    main()