"""
카페24 완전한 다운로드 프로세스
1. 올바른 검색 필드에서 검색
2. 엑셀다운로드
3. 엑셀파일요청
4. 다운로드 및 수정
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
    print("=== 카페24 완전한 다운로드 프로세스 ===")
    
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
        
        # 1. 검색분류를 상품명으로 변경
        print("1. 검색분류를 상품명으로 변경...")
        search_type_select = driver.find_element(By.XPATH, "//th[contains(text(), '검색분류')]/following-sibling::td//select")
        select = Select(search_type_select)
        
        for option in select.options:
            if "상품명" in option.text:
                select.select_by_visible_text(option.text)
                print("검색분류: 상품명으로 변경")
                break
        
        # 2. 같은 td 내의 input 찾기
        print("2. 검색어 입력...")
        parent_td = search_type_select.find_element(By.XPATH, "./ancestor::td")
        search_field = parent_td.find_element(By.XPATH, ".//input[@type='text']")
        search_field.clear()
        search_field.send_keys("[인생]점보떡볶이1490g")  # 정확한 상품명
        print("검색어 입력: [인생]점보떡볶이1490g")
        
        # 3. 판매상태를 전체로 변경
        print("3. 판매상태를 전체로 변경...")
        try:
            selling_status = driver.find_element(By.XPATH, "//th[contains(text(), '판매상태')]/following-sibling::td//select")
            select_selling = Select(selling_status)
            
            for option in select_selling.options:
                if "전체" in option.text:
                    select_selling.select_by_visible_text(option.text)
                    print("판매상태: 전체로 변경")
                    break
        except:
            print("판매상태 변경 스킵")
        
        # 4. 검색 실행
        print("4. 검색 실행...")
        search_field.send_keys(Keys.RETURN)
        time.sleep(3)
        
        # 5. 첫 번째 체크박스 선택
        print("5. 상품 선택...")
        try:
            # 상품 목록의 첫 번째 체크박스
            checkbox = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//tbody//input[@type='checkbox'][1]"))
            )
            if not checkbox.is_selected():
                checkbox.click()
                print("체크박스 선택 완료")
        except:
            print("체크박스 선택 실패 - 전체 선택 시도")
            try:
                all_checkbox = driver.find_element(By.XPATH, "//input[@id='allChk']")
                if not all_checkbox.is_selected():
                    all_checkbox.click()
            except:
                pass
        
        # 6. 엑셀다운로드 버튼 찾기
        print("6. 엑셀다운로드 버튼 찾기...")
        time.sleep(2)
        
        # JavaScript로 버튼 클릭 시도
        try:
            driver.execute_script("product_excel_download();")
            print("JavaScript로 엑셀다운로드 실행")
        except:
            # 버튼 직접 찾기
            excel_buttons = [
                "//a[@class='btnNormal'][contains(., '엑셀다운로드')]",
                "//a[contains(@onclick, 'excel')][contains(., '다운로드')]",
                "//button[contains(., '엑셀다운로드')]",
                "//span[contains(., '엑셀다운로드')]/.."
            ]
            
            for btn_xpath in excel_buttons:
                try:
                    excel_btn = driver.find_element(By.XPATH, btn_xpath)
                    if excel_btn.is_displayed():
                        excel_btn.click()
                        print("엑셀다운로드 버튼 클릭")
                        break
                except:
                    continue
        
        time.sleep(2)
        
        # 7. 새 창 처리
        print("7. 새 창 확인...")
        all_windows = driver.window_handles
        
        if len(all_windows) > 1:
            for window in all_windows:
                if window != main_window:
                    driver.switch_to.window(window)
                    print("새 창으로 전환")
                    break
            
            time.sleep(2)
            
            # 8. 엑셀파일요청 버튼 클릭
            print("8. 엑셀파일요청 버튼 찾기...")
            try:
                # iframe 확인
                iframes = driver.find_elements(By.TAG_NAME, "iframe")
                if iframes:
                    driver.switch_to.frame(iframes[0])
                    print("iframe으로 전환")
                
                # 파란색 버튼 찾기
                request_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary')] | //button[contains(., '엑셀파일요청')] | //a[contains(., '엑셀파일요청')]"))
                )
                request_btn.click()
                print("엑셀파일요청 버튼 클릭")
                
                time.sleep(2)
                
                # 알림창 처리
                try:
                    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                    alert_text = alert.text
                    print(f"알림창: {alert_text}")
                    alert.accept()
                    print("알림창 확인")
                except:
                    print("알림창 없음")
                
                # 페이지 새로고침 또는 대기
                time.sleep(3)
                
                # 다운로드 링크 대기
                print("9. 다운로드 링크 대기...")
                
                # 여러 방법으로 다운로드 링크 찾기
                download_found = False
                for i in range(10):  # 최대 10번 시도
                    try:
                        # 다운로드 아이콘이나 링크 찾기
                        download_elements = driver.find_elements(By.XPATH, "//a[contains(@href, 'download')] | //a[contains(., '다운로드')] | //img[@alt='다운로드']/.. | //button[contains(., '다운로드')]")
                        
                        for element in download_elements:
                            if element.is_displayed() and element.is_enabled():
                                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                                time.sleep(1)
                                element.click()
                                print("다운로드 시작!")
                                download_found = True
                                break
                        
                        if download_found:
                            break
                            
                    except:
                        pass
                    
                    # 페이지 새로고침
                    driver.refresh()
                    time.sleep(3)
                    print(f"다운로드 링크 찾는 중... ({i+1}/10)")
                
                time.sleep(5)
                
            except Exception as e:
                print(f"새 창 처리 오류: {e}")
            
            # 메인 창으로 돌아가기
            driver.switch_to.window(main_window)
        
        # 10. 다운로드된 파일 처리
        print("\n10. 다운로드된 파일 확인...")
        files = [f for f in os.listdir(download_path) if f.endswith('.csv') and os.path.getmtime(os.path.join(download_path, f)) > time.time() - 120]
        
        if files:
            latest_file = max([os.path.join(download_path, f) for f in files], key=os.path.getmtime)
            print(f"다운로드된 파일: {os.path.basename(latest_file)}")
            
            try:
                df = pd.read_csv(latest_file, encoding='utf-8-sig')
                print(f"총 {len(df)}개 상품")
                
                # P00000IB 찾기 또는 첫 번째 상품 수정
                if '상품코드' in df.columns and '판매가' in df.columns:
                    # P00000IB 찾기
                    mask = df['상품코드'] == 'P00000IB'
                    if mask.any():
                        idx = df[mask].index[0]
                        print(f"P00000IB 현재 가격: {df.loc[idx, '판매가']}")
                    else:
                        # 점보떡볶이 찾기
                        idx = 0
                        for i, row in df.iterrows():
                            if '점보떡볶이' in str(row.get('상품명', '')):
                                idx = i
                                break
                        print(f"점보떡볶이 현재 가격: {df.loc[idx, '판매가']}")
                    
                    # 가격 수정
                    df.loc[idx, '판매가'] = 13500
                    print("새 가격: 13500")
                    
                    # 저장
                    modified_file = os.path.join(download_path, f"price_modified_{int(time.time())}.csv")
                    df.to_csv(modified_file, index=False, encoding='utf-8-sig')
                    print(f"\n✅ 수정된 파일: {modified_file}")
                    
                    print("\n이제 카페24 관리자 페이지에서:")
                    print("1. 상품 > 상품 엑셀 관리 > 엑셀 업로드")
                    print("2. 위 파일을 업로드하세요")
                    
            except Exception as e:
                print(f"CSV 처리 오류: {e}")
        else:
            print("다운로드된 파일이 없습니다")
        
        print("\n작업 완료! 30초 후 종료...")
        time.sleep(30)
        
    except Exception as e:
        print(f"오류: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(30)
    
    finally:
        # 모든 창 닫기
        for window in driver.window_handles:
            driver.switch_to.window(window)
            driver.close()
        print("브라우저 종료")

if __name__ == "__main__":
    main()