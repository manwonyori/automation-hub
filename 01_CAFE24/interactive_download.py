"""
카페24 대화형 다운로드 - 사용자가 직접 지정
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
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

def take_screenshot(driver, filename):
    """스크린샷 저장"""
    screenshot_path = os.path.join(os.getcwd(), f"{filename}.png")
    driver.save_screenshot(screenshot_path)
    print(f"스크린샷 저장: {screenshot_path}")
    return screenshot_path

def highlight_element(driver, element):
    """요소를 하이라이트"""
    driver.execute_script("""
        arguments[0].style.border = '3px solid red';
        arguments[0].style.backgroundColor = 'yellow';
    """, element)

def main():
    print("=== 카페24 대화형 다운로드 ===")
    print("각 단계에서 화면을 확인하고 진행합니다.")
    
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
        
        # 화면 확인
        print("\n=== 단계 1: 검색 영역 확인 ===")
        take_screenshot(driver, "step1_search_area")
        
        # 검색 영역 요소들 찾기
        print("\n검색 관련 요소들:")
        
        # 모든 select 요소 찾기
        selects = driver.find_elements(By.TAG_NAME, "select")
        for i, select in enumerate(selects):
            try:
                if select.is_displayed():
                    print(f"\nSelect #{i+1}:")
                    print(f"  Name: {select.get_attribute('name')}")
                    print(f"  ID: {select.get_attribute('id')}")
                    options = select.find_elements(By.TAG_NAME, "option")
                    print(f"  옵션들: {[opt.text for opt in options[:5]]}")
            except:
                pass
        
        # 모든 input 요소 찾기
        inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
        print(f"\n텍스트 입력 필드: {len(inputs)}개")
        
        # 모든 버튼/링크 찾기
        buttons = driver.find_elements(By.XPATH, "//a[@class='btnSubmit'] | //button | //input[@type='submit']")
        print(f"버튼/링크: {len(buttons)}개")
        
        # 사용자 입력 대기
        print("\n=== 사용자 지정 모드 ===")
        print("브라우저에서 직접 다음 작업을 수행해주세요:")
        print("1. 검색분류를 '상품명'으로 변경")
        print("2. 검색어 입력란에 '[인생]점보떡볶이1490g' 입력")
        print("3. 검색 버튼 클릭")
        print("\n완료되면 아래 명령을 입력하세요.")
        
        # JavaScript로 대기 및 상태 확인
        print("\n현재 페이지에서 검색을 완료하면 자동으로 감지됩니다...")
        
        # URL 변경 감지
        original_url = driver.current_url
        while True:
            time.sleep(2)
            current_url = driver.current_url
            
            # 테이블에 데이터가 있는지 확인
            try:
                product_rows = driver.find_elements(By.XPATH, "//tbody//tr[contains(@class, 'center')]")
                if len(product_rows) > 0:
                    print(f"\n검색 결과 감지: {len(product_rows)}개 상품")
                    take_screenshot(driver, "step2_search_results")
                    break
            except:
                pass
            
            if current_url != original_url:
                print("페이지 변경 감지")
                break
        
        # 체크박스 선택
        print("\n=== 단계 2: 상품 선택 ===")
        print("첫 번째 상품의 체크박스를 선택합니다...")
        
        try:
            checkbox = driver.find_element(By.XPATH, "//tbody//input[@type='checkbox'][1]")
            if not checkbox.is_selected():
                highlight_element(driver, checkbox)
                time.sleep(1)
                checkbox.click()
                print("체크박스 선택 완료")
        except:
            print("체크박스를 찾을 수 없습니다. 수동으로 선택해주세요.")
            time.sleep(5)
        
        # 엑셀다운로드 버튼 찾기
        print("\n=== 단계 3: 엑셀다운로드 버튼 ===")
        
        # 페이지의 모든 링크 표시
        links = driver.find_elements(By.TAG_NAME, "a")
        excel_links = []
        
        for link in links:
            text = link.text.strip()
            if text and ("엑셀" in text or "excel" in text.lower()):
                excel_links.append(link)
                print(f"엑셀 관련 링크 발견: '{text}'")
                highlight_element(driver, link)
        
        # 사용자에게 선택 요청
        if excel_links:
            print(f"\n{len(excel_links)}개의 엑셀 관련 버튼을 찾았습니다.")
            print("하이라이트된 버튼 중 '엑셀다운로드'를 클릭해주세요.")
        else:
            print("엑셀다운로드 버튼을 찾을 수 없습니다.")
            print("수동으로 클릭해주세요.")
        
        # 새 창 감지
        print("\n새 창이 열리기를 기다립니다...")
        while len(driver.window_handles) == 1:
            time.sleep(1)
        
        print("새 창 감지!")
        driver.switch_to.window(driver.window_handles[-1])
        take_screenshot(driver, "step3_excel_popup")
        
        # 엑셀파일요청 버튼
        print("\n=== 단계 4: 엑셀파일요청 ===")
        request_buttons = driver.find_elements(By.XPATH, "//button | //a | //input[@type='button']")
        
        for btn in request_buttons:
            text = btn.text.strip()
            if text and "요청" in text:
                highlight_element(driver, btn)
                print(f"요청 버튼 발견: '{text}'")
        
        print("\n하이라이트된 '엑셀파일요청' 버튼을 클릭해주세요.")
        print("그 후 다운로드 링크가 나타나면 클릭해주세요.")
        
        # 사용자가 다운로드를 완료할 때까지 대기
        print("\n다운로드가 완료되면 10초 후 종료됩니다...")
        time.sleep(10)
        
        # 메인 창으로 돌아가기
        driver.switch_to.window(main_window)
        
        print("\n=== 완료 ===")
        print("다운로드 폴더를 확인해주세요.")
        print(f"기본 다운로드 경로: {os.path.join(os.path.expanduser('~'), 'Downloads')}")
        
    except Exception as e:
        print(f"오류: {e}")
        take_screenshot(driver, "error_screenshot")
        import traceback
        traceback.print_exc()
    
    finally:
        time.sleep(5)
        driver.quit()
        print("종료")

if __name__ == "__main__":
    main()