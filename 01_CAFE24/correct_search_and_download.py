"""
카페24 정확한 검색 및 다운로드 프로세스
1. 검색분류를 상품명으로 변경
2. 판매상태를 전체로 변경
3. [인생]점보떡볶이1490g 검색
4. 엑셀다운로드 → 엑셀파일요청 → 다운로드
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
    print("=== 카페24 정확한 검색 및 다운로드 ===")
    
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
    
    # 현재 창 핸들 저장
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
        try:
            # 검색분류 드롭다운 찾기
            search_type = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//select[contains(@name, 'search_type')] | //select[@name='search_type'] | //select[1]"))
            )
            select = Select(search_type)
            
            # 상품명 옵션 선택
            for option in select.options:
                if "상품명" in option.text:
                    select.select_by_visible_text(option.text)
                    print("검색분류: 상품명으로 변경 완료")
                    break
        except Exception as e:
            print(f"검색분류 변경 실패: {e}")
        
        # 2. 판매상태를 전체로 변경
        print("2. 판매상태를 전체로 변경...")
        try:
            # 판매상태 드롭다운 찾기
            selling_status = driver.find_element(By.XPATH, "//select[contains(@name, 'selling')] | //select[@name='selling_status']")
            select_selling = Select(selling_status)
            
            # 전체 옵션 선택
            for option in select_selling.options:
                if "전체" in option.text:
                    select_selling.select_by_visible_text(option.text)
                    print("판매상태: 전체로 변경 완료")
                    break
        except Exception as e:
            print(f"판매상태 변경 실패: {e}")
        
        # 3. 상품명 입력
        print("3. 상품명 입력...")
        search_field = driver.find_element(By.XPATH, "//input[@name='keyword'] | //input[@name='search_keyword'] | //input[@type='text'][1]")
        search_field.clear()
        search_field.send_keys("[인생]점보떡볶이1490g")
        print("상품명 입력: [인생]점보떡볶이1490g")
        
        # 4. 검색 버튼 클릭
        print("4. 검색 실행...")
        search_button = driver.find_element(By.XPATH, "//button[contains(text(), '검색')] | //input[@value='검색'] | //a[contains(text(), '검색')]")
        search_button.click()
        time.sleep(3)
        
        print("검색 완료")
        
        # 5. 체크박스 선택
        print("5. 상품 체크박스 선택...")
        try:
            # 첫 번째 상품의 체크박스 선택
            checkbox = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox'][@name='product_no[]'][1]"))
            )
            if not checkbox.is_selected():
                checkbox.click()
                print("체크박스 선택 완료")
        except:
            print("체크박스 선택 실패")
        
        # 6. 엑셀다운로드 클릭
        print("6. 엑셀다운로드 버튼 클릭...")
        excel_download_btn = driver.find_element(By.XPATH, "//a[contains(text(), '엑셀다운로드')] | //button[contains(text(), '엑셀다운로드')]")
        excel_download_btn.click()
        time.sleep(2)
        
        # 7. 새 창으로 전환
        print("7. 새 창 처리...")
        # 모든 창 핸들 가져오기
        all_windows = driver.window_handles
        
        # 새 창으로 전환
        for window in all_windows:
            if window != main_window:
                driver.switch_to.window(window)
                print("새 창으로 전환 완료")
                break
        
        time.sleep(2)
        
        # 8. 엑셀파일요청 버튼 클릭 (파란색 버튼)
        print("8. 엑셀파일요청 버튼 클릭...")
        try:
            # 파란색 버튼 찾기
            request_buttons = [
                "//button[@class='btn btn-primary'][contains(text(), '엑셀파일요청')]",
                "//button[contains(@class, 'btn-primary')][contains(text(), '엑셀파일요청')]",
                "//button[contains(text(), '엑셀파일요청')]",
                "//a[contains(text(), '엑셀파일요청')]",
                "//input[@value='엑셀파일요청']"
            ]
            
            for btn_xpath in request_buttons:
                try:
                    request_btn = driver.find_element(By.XPATH, btn_xpath)
                    if request_btn.is_displayed():
                        request_btn.click()
                        print("엑셀파일요청 버튼 클릭 완료")
                        break
                except:
                    continue
            
            time.sleep(3)
        except Exception as e:
            print(f"엑셀파일요청 버튼 클릭 실패: {e}")
        
        # 9. 다운로드 아이콘 대기 및 클릭
        print("9. 다운로드 아이콘 대기...")
        try:
            # 다운로드 아이콘/링크 대기 (최대 30초)
            download_link = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'download')] | //a[contains(text(), '다운로드')] | //button[contains(text(), '다운로드')] | //img[contains(@alt, '다운로드')]/.."))
            )
            
            # 스크롤해서 보이게 하기
            driver.execute_script("arguments[0].scrollIntoView(true);", download_link)
            time.sleep(1)
            
            download_link.click()
            print("다운로드 시작!")
            
            # 다운로드 완료 대기
            time.sleep(5)
            
        except Exception as e:
            print(f"다운로드 실패: {e}")
        
        # 10. 메인 창으로 돌아가기
        driver.switch_to.window(main_window)
        
        # 11. 다운로드된 파일 확인 및 수정
        print("\n10. 다운로드된 파일 확인...")
        files = [f for f in os.listdir(download_path) if f.endswith('.csv') and os.path.getmtime(os.path.join(download_path, f)) > time.time() - 60]
        
        if files:
            latest_file = max([os.path.join(download_path, f) for f in files], key=os.path.getmtime)
            print(f"다운로드된 파일: {os.path.basename(latest_file)}")
            
            # CSV 파일 수정
            try:
                df = pd.read_csv(latest_file, encoding='utf-8-sig')
                print(f"총 {len(df)}개 상품 로드")
                
                # 가격 수정
                if '판매가' in df.columns:
                    # 첫 번째 행의 가격 수정 (검색 결과가 하나일 것으로 예상)
                    print(f"현재 가격: {df.loc[0, '판매가']}")
                    df.loc[0, '판매가'] = 13500
                    print("새 가격: 13500")
                    
                    # 수정된 파일 저장
                    modified_file = os.path.join(download_path, f"price_modified_{int(time.time())}.csv")
                    df.to_csv(modified_file, index=False, encoding='utf-8-sig')
                    print(f"\n수정된 파일 저장 완료: {modified_file}")
                    
                    print("\n이제 이 파일을 카페24 엑셀 업로드에서 업로드하세요!")
                    print("경로: 상품 > 상품 엑셀 관리 > 엑셀 업로드")
                else:
                    print("판매가 컬럼을 찾을 수 없습니다")
                    print(f"컬럼 목록: {list(df.columns)}")
                    
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
        # 열린 모든 창 닫기
        for window in driver.window_handles:
            driver.switch_to.window(window)
            driver.close()
        print("브라우저 종료")

if __name__ == "__main__":
    main()