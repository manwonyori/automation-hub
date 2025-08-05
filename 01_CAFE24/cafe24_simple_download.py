"""
카페24 심플 다운로드 - 최소한의 코드로 테스트
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

def test_download():
    print("=== 카페24 다운로드 테스트 ===")
    
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    before_files = set(os.listdir(download_path))
    
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    
    try:
        # 로그인
        driver.get("https://manwonyori.cafe24.com/admin")
        
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert.accept()
        except:
            pass
        
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
        
        # 상품관리 페이지
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
        
        # 검색분류 선택
        search_type_select = driver.find_element(By.XPATH, "//th[contains(text(), '검색분류')]/following-sibling::td//select")
        select = Select(search_type_select)
        for option in select.options:
            if "상품명" in option.text:
                select.select_by_visible_text(option.text)
                break
                
        # 검색어 입력
        parent_td = search_type_select.find_element(By.XPATH, "./ancestor::td")
        search_field = parent_td.find_element(By.XPATH, ".//input[@type='text']")
        search_field.clear()
        search_field.send_keys("[인생]점보떡볶이1490g")
        
        # 검색 실행
        driver.execute_script("document.querySelector('form').submit();")
        time.sleep(5)
        
        # 체크박스 선택
        checkbox = driver.find_element(By.XPATH, "//tbody//input[@type='checkbox'][1]")
        if not checkbox.is_selected():
            checkbox.click()
            
        print("\n=== 엑셀다운로드 버튼 찾기 ===")
        
        # 모든 a 태그 확인
        links = driver.find_elements(By.TAG_NAME, "a")
        for i, link in enumerate(links):
            text = link.text.strip()
            href = link.get_attribute('href') or ""
            onclick = link.get_attribute('onclick') or ""
            
            if text and any(keyword in text for keyword in ['엑셀', 'excel', 'Excel', 'xls']):
                print(f"\n링크 {i}: {text}")
                print(f"  href: {href}")
                print(f"  onclick: {onclick}")
                
                # 엑셀다운로드 버튼이면 클릭
                if "다운로드" in text:
                    driver.execute_script("arguments[0].scrollIntoView(true);", link)
                    time.sleep(1)
                    
                    # 스크린샷
                    driver.save_screenshot("before_excel_click.png")
                    
                    # 클릭 시도
                    try:
                        link.click()
                    except:
                        driver.execute_script("arguments[0].click();", link)
                    
                    print("엑셀다운로드 클릭!")
                    break
        
        # 새 창 처리
        time.sleep(3)
        if len(driver.window_handles) > 1:
            print("\n새 창 열림")
            driver.switch_to.window(driver.window_handles[-1])
            
            # 스크린샷
            driver.save_screenshot("excel_popup.png")
            
            # 엑셀파일요청
            request_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., '엑셀파일요청')] | //a[contains(., '엑셀파일요청')]"))
            )
            request_btn.click()
            print("엑셀파일요청 클릭")
            
            # 알림창
            try:
                alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                print(f"알림: {alert.text}")
                alert.accept()
            except:
                pass
            
            # 파일 생성 대기
            print("\n파일 생성 대기중...")
            for i in range(10):
                time.sleep(3)
                driver.refresh()
                
                # 현재 페이지 내용 확인
                page_source = driver.page_source
                if "다운로드" in page_source:
                    print(f"{i+1}회차: 다운로드 링크 확인 중...")
                    
                    # 모든 링크 다시 확인
                    all_links = driver.find_elements(By.TAG_NAME, "a")
                    for link in all_links:
                        href = link.get_attribute('href') or ""
                        text = link.text or ""
                        
                        # 실제 다운로드 링크인지 확인
                        if href and ('download' in href.lower() or '.xls' in href or '.csv' in href):
                            print(f"\n다운로드 링크 발견!")
                            print(f"  텍스트: {text}")
                            print(f"  href: {href}")
                            
                            # 스크린샷
                            driver.save_screenshot(f"download_link_{i}.png")
                            
                            # 다운로드
                            link.click()
                            print("다운로드 시작!")
                            
                            # 다운로드 완료 대기
                            time.sleep(10)
                            
                            # 새 파일 확인
                            after_files = set(os.listdir(download_path))
                            new_files = after_files - before_files
                            
                            if new_files:
                                print(f"\n다운로드 완료: {list(new_files)}")
                            else:
                                print("\n새 파일을 찾을 수 없음")
                            
                            return
                
                if i == 4:
                    # 5회차에 한 번 더 엑셀파일요청 시도
                    try:
                        request_btn2 = driver.find_element(By.XPATH, "//button[contains(., '엑셀파일요청')] | //a[contains(., '엑셀파일요청')]")
                        if request_btn2.is_displayed():
                            request_btn2.click()
                            print("엑셀파일요청 재시도")
                    except:
                        pass
        
        print("\n테스트 완료")
        
    except Exception as e:
        print(f"오류: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        input("\nEnter를 눌러 종료...")
        driver.quit()

if __name__ == "__main__":
    test_download()