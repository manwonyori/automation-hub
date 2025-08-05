"""
카페24 상품명으로 검색 후 다운로드
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
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

def main():
    print("=== 카페24 상품명 검색 및 다운로드 ===")
    
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
        
        # 검색 분류를 상품명으로 변경
        print("검색 분류를 상품명으로 변경...")
        try:
            # 검색 타입 드롭다운 찾기
            search_type_selectors = [
                "//select[@name='search_type']",
                "//select[contains(@name, 'search')]",
                "//select[@id='search_type']",
                "//select[1]"  # 첫 번째 select
            ]
            
            for selector in search_type_selectors:
                try:
                    search_type = driver.find_element(By.XPATH, selector)
                    if search_type.is_displayed():
                        select = Select(search_type)
                        # 상품명으로 변경
                        try:
                            select.select_by_value("product_name")
                        except:
                            try:
                                select.select_by_visible_text("상품명")
                            except:
                                # 옵션 값 확인
                                for option in select.options:
                                    if "상품명" in option.text or "name" in option.get_attribute("value"):
                                        option.click()
                                        break
                        print("검색 타입: 상품명으로 설정")
                        break
                except:
                    continue
        except Exception as e:
            print(f"검색 타입 변경 실패: {e}")
        
        # 상품명으로 검색
        print("점보떡볶이 검색...")
        search_field = driver.find_element(By.XPATH, "//input[@name='keyword'] | //input[@type='text'][1]")
        search_field.clear()
        search_field.send_keys("점보떡볶이")
        search_field.send_keys(Keys.RETURN)
        time.sleep(3)
        
        print("검색 완료")
        
        # 검색 결과에서 체크박스 선택
        try:
            # P00000IB 상품 찾기
            checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox'][@name='product_no[]']")
            
            selected = False
            for checkbox in checkboxes:
                try:
                    # 체크박스가 있는 행 찾기
                    row = checkbox.find_element(By.XPATH, "./ancestor::tr")
                    if "P00000IB" in row.text or "점보떡볶이" in row.text:
                        if not checkbox.is_selected():
                            checkbox.click()
                            selected = True
                            print("점보떡볶이 상품 선택")
                            break
                except:
                    continue
            
            if not selected:
                # 첫 번째 체크박스 선택
                if checkboxes and not checkboxes[0].is_selected():
                    checkboxes[0].click()
                    print("첫 번째 상품 선택")
        except:
            print("체크박스 선택 실패")
        
        # 엑셀 다운로드 버튼 찾기
        print("엑셀 다운로드 시작...")
        
        download_buttons = [
            "//a[text()='엑셀다운로드']",
            "//button[text()='엑셀다운로드']",
            "//a[contains(text(), '엑셀다운로드')]",
            "//button[contains(text(), '엑셀다운로드')]",
            "//a[contains(text(), '엑셀 다운로드')]",
            "//button[contains(text(), '엑셀 다운로드')]",
            "//a[@class='btnNormal']",
            "//span[contains(text(), '엑셀')]/.."
        ]
        
        for btn_xpath in download_buttons:
            try:
                btn = driver.find_element(By.XPATH, btn_xpath)
                if btn.is_displayed():
                    btn.click()
                    print("엑셀 다운로드 버튼 클릭")
                    break
            except:
                continue
        
        # 다운로드 대기
        time.sleep(5)
        
        # 다운로드된 파일 확인
        files = [f for f in os.listdir(download_path) if f.endswith('.csv') and 'product' in f.lower()]
        
        if files:
            # 최신 파일 찾기
            latest_file = max([os.path.join(download_path, f) for f in files], key=os.path.getctime)
            print(f"\n다운로드된 파일: {os.path.basename(latest_file)}")
            
            # CSV 수정
            try:
                df = pd.read_csv(latest_file, encoding='utf-8-sig')
                
                # P00000IB 찾기
                if '상품코드' in df.columns:
                    mask = df['상품코드'] == 'P00000IB'
                    if mask.any():
                        print(f"현재 가격: {df.loc[mask, '판매가'].values[0]}")
                        df.loc[mask, '판매가'] = 13500
                        
                        # 수정된 파일 저장
                        modified_file = os.path.join(download_path, "price_modified_jumbo.csv")
                        df.to_csv(modified_file, index=False, encoding='utf-8-sig')
                        print(f"수정된 파일: {modified_file}")
                        
                        print("\n이제 이 파일을 엑셀 업로드에서 업로드하세요!")
                    else:
                        print("P00000IB를 찾을 수 없습니다")
                else:
                    print("상품코드 컬럼이 없습니다")
            except Exception as e:
                print(f"CSV 처리 오류: {e}")
        else:
            print("다운로드된 파일이 없습니다")
        
        print("\n작업 완료! 20초 후 종료...")
        time.sleep(20)
        
    except Exception as e:
        print(f"오류: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(20)
    
    finally:
        driver.quit()
        print("브라우저 종료")

if __name__ == "__main__":
    main()