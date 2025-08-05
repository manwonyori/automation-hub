"""
알림창과 팝업창을 모두 처리하는 스크립트
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def handle_alert(driver):
    """알림창 처리"""
    try:
        alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert_text = alert.text
        print(f"알림창 감지: {alert_text}")
        alert.accept()
        print("알림창 확인 완료")
        time.sleep(2)
        return True
    except:
        return False

def close_all_popups(driver):
    """모든 팝업 닫기"""
    print("팝업창 검색 및 닫기 시작...")
    
    # 다양한 팝업 닫기 버튼 선택자들
    popup_selectors = [
        "//button[contains(@class, 'close')]",
        "//span[text()='×']",
        "//span[text()='X']", 
        "//a[@class='close']",
        "//button[contains(text(), '닫기')]",
        "//button[contains(text(), '확인')]",
        "//input[@value='닫기']",
        "//input[@value='확인']",
        "//div[contains(@class, 'modal')]//button",
        "//div[contains(@class, 'popup')]//button",
        "//*[@title='닫기']",
        "//*[@title='close']",
        "//img[contains(@src, 'close')]",
        "//img[contains(@alt, '닫기')]",
        "//a[contains(@onclick, 'close')]",
        "//button[contains(@onclick, 'close')]"
    ]
    
    closed_count = 0
    
    for selector in popup_selectors:
        try:
            elements = driver.find_elements(By.XPATH, selector)
            for element in elements:
                try:
                    if element.is_displayed() and element.is_enabled():
                        # 스크롤해서 보이게 만들기
                        driver.execute_script("arguments[0].scrollIntoView(true);", element)
                        time.sleep(0.5)
                        
                        # 클릭 시도
                        try:
                            element.click()
                            closed_count += 1
                            print(f"팝업 닫기 성공: {selector}")
                            time.sleep(1)
                        except:
                            # JavaScript로 클릭 시도
                            driver.execute_script("arguments[0].click();", element)
                            closed_count += 1
                            print(f"팝업 닫기 성공 (JS): {selector}")
                            time.sleep(1)
                except Exception as e:
                    continue
        except:
            continue
    
    print(f"총 {closed_count}개의 팝업을 닫았습니다.")
    return closed_count

def main():
    print("=== 카페24 알림창 및 팝업 처리 ===")
    
    # 브라우저 설정
    print("1. 브라우저 연결...")
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    
    try:
        # 카페24 관리자 페이지로 이동
        print("2. 카페24 관리자 페이지 접속...")
        driver.get("https://manwonyori.cafe24.com/admin")
        time.sleep(2)
        
        # 알림창 처리
        print("3. 알림창 처리...")
        if handle_alert(driver):
            print("알림창 처리 완료")
        else:
            print("알림창 없음")
        
        print(f"현재 URL: {driver.current_url}")
        print(f"페이지 제목: {driver.title}")
        
        # 팝업 닫기 실행
        print("4. 팝업창 처리...")
        close_all_popups(driver)
        
        # 추가 알림창 확인 (팝업 닫은 후에 생길 수 있음)
        print("5. 추가 알림창 확인...")
        handle_alert(driver)
        
        print("=" * 50)
        print("모든 알림창과 팝업 처리 완료!")
        print("현재 페이지가 깨끗해졌습니다.")
        print(f"최종 URL: {driver.current_url}")
        print("=" * 50)
        
        # 10분 대기 (사용자가 다음 단계 진행)
        wait_time = 600
        print(f"사용자 작업을 위해 {wait_time//60}분 대기합니다...")
        
        for i in range(wait_time, 0, -60):
            print(f"남은 시간: {i//60}분 - 현재 URL: {driver.current_url}")
            time.sleep(60)
        
    except Exception as e:
        print(f"오류 발생: {e}")
        time.sleep(30)
    
    finally:
        try:
            driver.quit()
            print("브라우저 종료")
        except:
            pass

if __name__ == "__main__":
    main()