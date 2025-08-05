"""
카페24 유연한 검색 및 다운로드
상품번호 또는 상품명으로 검색 가능
"""

import time
import os
import glob
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

def search_and_download(search_type="product_name", search_value="[인생]점보떡볶이1490g"):
    """
    search_type: "product_code" 또는 "product_name"
    search_value: 검색할 값
    """
    print(f"=== 카페24 검색 및 다운로드 ({search_type}: {search_value}) ===")
    
    # 기본 다운로드 폴더
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    print(f"다운로드 폴더: {download_path}")
    
    # 다운로드 전 파일 목록
    before_files = set(glob.glob(os.path.join(download_path, "*.csv")))
    
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    
    # 현재 창 핸들
    main_window = driver.current_window_handle
    
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
        
        # 1. 검색 타입 설정
        print("1. 검색 설정...")
        search_type_select = driver.find_element(By.XPATH, "//th[contains(text(), '검색분류')]/following-sibling::td//select")
        select = Select(search_type_select)
        
        if search_type == "product_code":
            # 상품코드로 검색
            for option in select.options:
                if "상품코드" in option.text:
                    select.select_by_visible_text(option.text)
                    print("검색분류: 상품코드")
                    break
        else:
            # 상품명으로 검색
            for option in select.options:
                if "상품명" in option.text:
                    select.select_by_visible_text(option.text)
                    print("검색분류: 상품명")
                    break
        
        # 2. 검색어 입력
        parent_td = search_type_select.find_element(By.XPATH, "./ancestor::td")
        search_field = parent_td.find_element(By.XPATH, ".//input[@type='text']")
        search_field.clear()
        search_field.send_keys(search_value)
        print(f"검색어 입력: {search_value}")
        
        # 3. 검색 실행
        print("검색 실행...")
        # form submit으로 검색 실행
        try:
            driver.execute_script("document.querySelector('form').submit();")
            print("검색 폼 제출")
        except:
            # 검색 버튼 직접 찾기
            try:
                # 검색 버튼 찾기 - 다양한 방법 시도
                search_selectors = [
                    "//a[@class='btnSubmit']",
                    "//a[contains(@onclick, 'search')]",
                    "//a[contains(text(), '검색') and not(contains(text(), '상세'))]",
                    "//img[@alt='검색']/.."
                ]
                
                for selector in search_selectors:
                    try:
                        search_button = driver.find_element(By.XPATH, selector)
                        if search_button.is_displayed():
                            driver.execute_script("arguments[0].click();", search_button)
                            print("검색 버튼 클릭")
                            break
                    except:
                        continue
            except:
                print("검색 버튼을 찾을 수 없습니다")
        
        time.sleep(3)
        
        # 검색 결과 확인
        try:
            results = driver.find_elements(By.XPATH, "//tbody//tr[@class!='nodata']")
            print(f"검색 결과: {len(results)}개 상품")
        except:
            print("검색 결과 확인 실패")
        
        # 4. 체크박스 선택
        print("4. 상품 선택...")
        try:
            checkbox = driver.find_element(By.XPATH, "//tbody//input[@type='checkbox'][@name='product_no[]'][1]")
            if not checkbox.is_selected():
                checkbox.click()
                print("체크박스 선택 완료")
        except:
            print("체크박스 선택 실패")
        
        # 5. 엑셀다운로드
        print("5. 엑셀다운로드 실행...")
        
        # 엑셀다운로드 버튼 찾기 - 다양한 방법
        excel_button = None
        excel_selectors = [
            "//a[@class='btnNormal'][contains(., '엑셀다운로드')]",
            "//a[contains(text(), '엑셀다운로드')]",
            "//button[contains(text(), '엑셀다운로드')]",
            "//a[contains(@onclick, 'product_excel_download')]",
            "//img[@alt='엑셀다운로드']/..",
            "//span[contains(text(), '엑셀다운로드')]/.."
        ]
        
        for selector in excel_selectors:
            try:
                excel_button = driver.find_element(By.XPATH, selector)
                if excel_button.is_displayed():
                    print(f"엑셀다운로드 버튼 찾음: {selector}")
                    break
            except:
                continue
        
        if excel_button:
            driver.execute_script("arguments[0].scrollIntoView(true);", excel_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", excel_button)
            print("엑셀다운로드 버튼 클릭")
        else:
            # JavaScript 함수 직접 호출
            try:
                driver.execute_script("product_excel_download();")
                print("JavaScript로 엑셀다운로드 실행")
            except:
                print("엑셀다운로드 버튼을 찾을 수 없습니다")
                return None
        
        time.sleep(2)
        
        # 6. 새 창 처리
        all_windows = driver.window_handles
        if len(all_windows) > 1:
            driver.switch_to.window(all_windows[-1])
            print("새 창으로 전환")
            
            # 엑셀파일요청
            request_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., '엑셀파일요청')] | //a[contains(., '엑셀파일요청')]"))
            )
            request_btn.click()
            print("엑셀파일요청 클릭")
            
            # 알림창 처리
            try:
                alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                print(f"알림: {alert.text}")
                alert.accept()
            except:
                pass
            
            # 다운로드 링크 대기 및 클릭
            print("다운로드 링크 대기...")
            time.sleep(5)  # 파일 생성 대기
            
            # 페이지 새로고침
            driver.refresh()
            time.sleep(3)
            
            # 다운로드 링크 찾기 - 여러 방법 시도
            download_found = False
            download_selectors = [
                "//a[contains(@href, 'download')]",
                "//a[contains(text(), '다운로드')]",
                "//img[@alt='다운로드']/..",
                "//button[contains(text(), '다운로드')]",
                "//a[@class='download']",
                "//td[@class='center']//a"
            ]
            
            for selector in download_selectors:
                try:
                    download_elements = driver.find_elements(By.XPATH, selector)
                    for element in download_elements:
                        if element.is_displayed() and element.is_enabled():
                            href = element.get_attribute('href')
                            if href and ('download' in href or 'xls' in href or 'csv' in href):
                                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                                time.sleep(1)
                                element.click()
                                print(f"다운로드 클릭! ({selector})")
                                download_found = True
                                break
                    if download_found:
                        break
                except:
                    continue
            
            if not download_found:
                print("다운로드 링크를 찾을 수 없습니다")
            
            time.sleep(5)
            
            # 메인 창으로 돌아가기
            driver.switch_to.window(main_window)
        
        # 7. 다운로드 파일 확인
        print("\n6. 다운로드 파일 확인...")
        time.sleep(5)
        
        after_files = set(glob.glob(os.path.join(download_path, "*.csv")))
        new_files = after_files - before_files
        
        if new_files:
            latest_file = list(new_files)[0]
            print(f"다운로드 완료: {os.path.basename(latest_file)}")
            
            # CSV 파일 수정
            try:
                df = pd.read_csv(latest_file, encoding='utf-8-sig')
                print(f"상품 수: {len(df)}개")
                
                if '판매가' in df.columns:
                    # 첫 번째 상품의 가격 수정
                    current_price = df.loc[0, '판매가']
                    print(f"현재 가격: {current_price}")
                    
                    df.loc[0, '판매가'] = 13500
                    print("새 가격: 13500")
                    
                    # 수정된 파일 저장
                    modified_file = os.path.join(download_path, f"price_modified_{int(time.time())}.csv")
                    df.to_csv(modified_file, index=False, encoding='utf-8-sig')
                    print(f"\n수정된 파일 저장: {modified_file}")
                    
                    print("\n이제 카페24에서:")
                    print("1. 상품 > 상품 엑셀 관리 > 엑셀 업로드")
                    print("2. 위 파일을 업로드하세요")
                    
                    return modified_file
                    
            except Exception as e:
                print(f"CSV 처리 오류: {e}")
        else:
            print("다운로드된 파일이 없습니다")
        
        time.sleep(10)
        
    except Exception as e:
        print(f"오류: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(10)
    
    finally:
        driver.quit()
        print("종료")
    
    return None

if __name__ == "__main__":
    # 상품명으로 검색
    search_and_download("product_name", "[인생]점보떡볶이1490g")
    
    # 또는 상품코드로 검색
    # search_and_download("product_code", "P00000IB")