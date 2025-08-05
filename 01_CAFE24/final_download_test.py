"""
카페24 최종 다운로드 테스트
기본 다운로드 폴더 사용
"""

import time
import os
import glob
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
    print("=== 카페24 최종 다운로드 테스트 ===")
    
    # 기본 다운로드 폴더 사용
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
        
        # 1. 검색분류를 상품명으로 변경
        print("1. 검색 설정...")
        search_type_select = driver.find_element(By.XPATH, "//th[contains(text(), '검색분류')]/following-sibling::td//select")
        select = Select(search_type_select)
        
        for option in select.options:
            if "상품명" in option.text:
                select.select_by_visible_text(option.text)
                break
        
        # 2. 검색어 입력
        parent_td = search_type_select.find_element(By.XPATH, "./ancestor::td")
        search_field = parent_td.find_element(By.XPATH, ".//input[@type='text']")
        search_field.clear()
        search_field.send_keys("[인생]점보떡볶이1490g")
        print("검색어: [인생]점보떡볶이1490g")
        
        # 3. 검색/초기화 영역에서 검색 버튼 클릭
        print("검색 버튼 찾기...")
        # 검색/초기화가 함께 있는 영역의 검색 버튼 찾기
        search_buttons = driver.find_elements(By.XPATH, "//a[text()='검색'] | //button[text()='검색'] | //input[@value='검색']")
        
        # 검색 버튼이 여러 개일 경우, 검색/초기화가 함께 있는 버튼 찾기
        clicked = False
        for btn in search_buttons:
            try:
                # 같은 영역에 초기화 버튼이 있는지 확인
                parent = btn.find_element(By.XPATH, "./parent::*")
                if "초기화" in parent.text:
                    btn.click()
                    print("검색 버튼 클릭 (검색/초기화 영역)")
                    clicked = True
                    break
            except:
                pass
        
        # 찾지 못했으면 첫 번째 검색 버튼 클릭
        if not clicked and search_buttons:
            search_buttons[0].click()
            print("검색 버튼 클릭")
        
        time.sleep(3)
        
        # 4. 체크박스 선택
        try:
            checkbox = driver.find_element(By.XPATH, "//tbody//input[@type='checkbox'][1]")
            if not checkbox.is_selected():
                checkbox.click()
        except:
            pass
        
        # 5. 엑셀다운로드
        print("2. 엑셀다운로드 실행...")
        
        # JavaScript 실행
        try:
            driver.execute_script("product_excel_download();")
        except:
            # 버튼 클릭
            excel_btn = driver.find_element(By.XPATH, "//a[contains(., '엑셀다운로드')]")
            excel_btn.click()
        
        time.sleep(2)
        
        # 6. 새 창 처리
        all_windows = driver.window_handles
        if len(all_windows) > 1:
            driver.switch_to.window(all_windows[-1])
            print("새 창으로 전환")
            
            time.sleep(2)
            
            # 엑셀파일요청
            request_btn = driver.find_element(By.XPATH, "//button[contains(., '엑셀파일요청')] | //a[contains(., '엑셀파일요청')]")
            request_btn.click()
            print("엑셀파일요청 클릭")
            
            # 알림창 처리
            try:
                alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                print(f"알림: {alert.text}")
                alert.accept()
            except:
                pass
            
            time.sleep(3)
            
            # 다운로드 시도
            print("3. 다운로드 찾기...")
            
            # 페이지 내 모든 링크 확인
            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href")
                text = link.text
                if href and ("download" in href.lower() or "excel" in href.lower()):
                    print(f"다운로드 링크 발견: {text} - {href}")
                    link.click()
                    break
            
            time.sleep(5)
            
            # 메인 창으로 돌아가기
            driver.switch_to.window(main_window)
        
        # 다운로드 확인
        print("\n4. 다운로드 파일 확인...")
        time.sleep(5)
        
        # 새로 생성된 파일 찾기
        after_files = set(glob.glob(os.path.join(download_path, "*.csv")))
        new_files = after_files - before_files
        
        if new_files:
            for file in new_files:
                print(f"✅ 다운로드된 파일: {os.path.basename(file)}")
                
                # 파일 내용 미리보기
                try:
                    with open(file, 'r', encoding='utf-8-sig') as f:
                        lines = f.readlines()[:3]
                        print("\n파일 내용 미리보기:")
                        for line in lines:
                            print(line.strip()[:100] + "...")
                except:
                    pass
        else:
            print("❌ 다운로드된 CSV 파일이 없습니다")
            
            # 모든 새 파일 확인
            all_after = set(glob.glob(os.path.join(download_path, "*.*")))
            all_new = all_after - set(glob.glob(os.path.join(download_path, "*.*")))
            if all_new:
                print("\n다른 형식의 파일:")
                for file in all_new:
                    print(f"  - {os.path.basename(file)}")
        
        print("\n작업 완료!")
        time.sleep(10)
        
    except Exception as e:
        print(f"오류: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(10)
    
    finally:
        driver.quit()
        print("종료")

if __name__ == "__main__":
    main()