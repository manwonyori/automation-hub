"""
현재 열린 브라우저에서 모든 팝업창 닫기
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

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
        "//img[contains(@alt, '닫기')]"
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
    
    # iframe 내부의 팝업도 확인
    try:
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            try:
                driver.switch_to.frame(iframe)
                
                for selector in popup_selectors:
                    try:
                        elements = driver.find_elements(By.XPATH, selector)
                        for element in elements:
                            if element.is_displayed() and element.is_enabled():
                                element.click()
                                closed_count += 1
                                print(f"iframe 팝업 닫기 성공: {selector}")
                                time.sleep(1)
                    except:
                        continue
                
                driver.switch_to.default_content()
            except:
                driver.switch_to.default_content()
                continue
    except:
        pass
    
    print(f"총 {closed_count}개의 팝업을 닫았습니다.")
    return closed_count

def main():
    print("=== 카페24 팝업 닫기 ===")
    
    # 브라우저 설정 (기존 세션 연결)
    print("1. 브라우저 연결...")
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # 기존 브라우저 디버그 포트에 연결 시도
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        # 기존 세션에 연결 시도
        driver = webdriver.Chrome(options=options)
        print("기존 브라우저 세션에 연결됨")
    except:
        # 새 브라우저 시작
        print("새 브라우저 시작...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=Options())
        driver.maximize_window()
        
        # 카페24 관리자 페이지로 이동
        driver.get("https://manwonyori.cafe24.com/admin")
        time.sleep(3)
    
    try:
        print(f"현재 URL: {driver.current_url}")
        print(f"페이지 제목: {driver.title}")
        
        # 팝업 닫기 실행
        close_all_popups(driver)
        
        print("=" * 50)
        print("팝업 닫기 완료!")
        print("현재 페이지가 깨끗해졌습니다.")
        print("다음 단계를 계속 진행할 수 있습니다.")
        print("=" * 50)
        
        # 5분 대기
        print("5분 후 자동 종료됩니다...")
        time.sleep(300)
        
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