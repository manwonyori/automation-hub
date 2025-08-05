"""
카페24 특정 상품(P00000IB) 다운로드 및 가격 수정
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
    print("=== 카페24 P00000IB 상품 다운로드 및 수정 ===")
    
    # 다운로드 폴더 설정
    download_path = "C:\\Users\\8899y\\Documents\\cafe24\\downloads"
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    # 기존 파일 정리
    for file in os.listdir(download_path):
        if file.endswith('.csv') and 'product' in file.lower():
            try:
                os.remove(os.path.join(download_path, file))
                print(f"기존 파일 삭제: {file}")
            except:
                pass
    
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
        
        # P00000IB 검색
        print("P00000IB 상품 검색...")
        try:
            # 드롭다운 선택 (상품코드로 검색)
            try:
                search_type = driver.find_element(By.XPATH, "//select[@name='search_type'] | //select[contains(@name, 'search')]")
                from selenium.webdriver.support.ui import Select
                select = Select(search_type)
                select.select_by_value("product_code")
                print("검색 타입: 상품코드")
            except:
                print("검색 타입 선택 스킵")
            
            # 검색어 입력
            search_field = driver.find_element(By.XPATH, "//input[@name='keyword'] | //input[@name='search_keyword'] | //input[@type='text'][1]")
            search_field.clear()
            search_field.send_keys("P00000IB")
            
            # 검색 실행
            search_field.send_keys(Keys.RETURN)
            time.sleep(3)
            print("검색 완료")
            
            # 상품 체크박스 선택
            print("상품 선택...")
            checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox'][@name='product_no[]'] | //input[@type='checkbox'][contains(@value, '209')]")
            
            if checkboxes:
                for checkbox in checkboxes:
                    if not checkbox.is_selected():
                        checkbox.click()
                        print("체크박스 선택")
                        break
            else:
                # 전체 선택 시도
                print("개별 체크박스를 찾을 수 없어 전체 선택 시도")
                all_checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox'][@id='allChk'] | //input[@type='checkbox'][1]")
                if not all_checkbox.is_selected():
                    all_checkbox.click()
        except Exception as e:
            print(f"검색/선택 오류: {e}")
        
        # 엑셀 다운로드
        print("엑셀 다운로드 시작...")
        
        # 다운로드 버튼 찾기 - 여러 가능성
        download_clicked = False
        download_buttons = [
            "//a[contains(., '엑셀다운로드')]",
            "//button[contains(., '엑셀다운로드')]",
            "//a[contains(., '엑셀 다운로드')]",
            "//button[contains(., '엑셀 다운로드')]",
            "//a[@onclick and contains(., '다운로드')]",
            "//button[@onclick and contains(., '다운로드')]",
            "//img[@alt='엑셀다운로드']/..",
            "//input[@value='엑셀다운로드']"
        ]
        
        for btn_xpath in download_buttons:
            try:
                btn = driver.find_element(By.XPATH, btn_xpath)
                if btn.is_displayed():
                    btn.click()
                    download_clicked = True
                    print(f"다운로드 버튼 클릭: {btn.text or '버튼'}")
                    break
            except:
                continue
        
        if not download_clicked:
            print("다운로드 버튼을 찾을 수 없습니다")
            # JavaScript로 다운로드 함수 실행 시도
            try:
                driver.execute_script("product_excel_download();")
                print("JavaScript로 다운로드 실행")
            except:
                print("JavaScript 실행 실패")
        
        # 다운로드 대기
        time.sleep(5)
        
        # 다운로드된 파일 확인
        files = [f for f in os.listdir(download_path) if f.endswith('.csv') and os.path.getsize(os.path.join(download_path, f)) > 1000]
        
        if files:
            latest_file = max([os.path.join(download_path, f) for f in files], key=os.path.getctime)
            print(f"\n다운로드된 파일: {os.path.basename(latest_file)}")
            
            # CSV 파일 읽기 및 수정
            try:
                df = pd.read_csv(latest_file, encoding='utf-8-sig')
                print(f"총 {len(df)}개 상품 로드")
                
                # P00000IB 찾기
                if '상품코드' in df.columns:
                    mask = df['상품코드'] == 'P00000IB'
                    if mask.any():
                        current_price = df.loc[mask, '판매가'].values[0]
                        print(f"\nP00000IB 현재 가격: {current_price}")
                        
                        # 가격 수정
                        df.loc[mask, '판매가'] = 13500
                        print("새 가격 설정: 13500")
                        
                        # 수정된 파일 저장
                        modified_file = os.path.join(download_path, "price_modified_P00000IB.csv")
                        df.to_csv(modified_file, index=False, encoding='utf-8-sig')
                        print(f"수정된 파일 저장: {modified_file}")
                        
                        # 엑셀 업로드 페이지로 이동
                        print("\n엑셀 업로드 페이지로 이동...")
                        driver.get("https://manwonyori.cafe24.com/disp/admin/shop1/product/ProductExcelManage")
                        time.sleep(2)
                        
                        # 엑셀 업로드 탭 클릭
                        try:
                            upload_tab = driver.find_element(By.XPATH, "//a[contains(., '엑셀 업로드')] | //button[contains(., '엑셀 업로드')]")
                            upload_tab.click()
                            time.sleep(1)
                        except:
                            pass
                        
                        # 파일 업로드
                        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
                        file_input.send_keys(modified_file)
                        print("파일 선택 완료")
                        
                        # 업로드 실행
                        upload_btn = driver.find_element(By.XPATH, "//button[contains(., '업로드')] | //input[@value='업로드']")
                        upload_btn.click()
                        print("업로드 실행!")
                        
                        time.sleep(5)
                        print("\nSUCCESS: 가격 수정 완료!")
                        
                    else:
                        print("P00000IB 상품을 찾을 수 없습니다")
                else:
                    print("상품코드 컬럼을 찾을 수 없습니다")
                    print(f"컬럼 목록: {list(df.columns)[:10]}")
            except Exception as e:
                print(f"CSV 처리 오류: {e}")
        else:
            print("다운로드된 파일이 없습니다")
        
        print("\n10초 후 종료...")
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