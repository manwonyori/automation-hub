"""
브라우저 관리 모듈
모든 사이트에서 공통으로 사용
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging

logger = logging.getLogger(__name__)


class BrowserManager:
    """브라우저 관리 클래스"""
    
    def __init__(self):
        self.driver = None
        self.options = None
        
    def setup_driver(self, headless=False, download_dir=None):
        """브라우저 드라이버 설정"""
        self.options = Options()
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        
        if headless:
            self.options.add_argument("--headless")
            
        if download_dir:
            prefs = {
                "download.default_directory": download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            self.options.add_experimental_option("prefs", prefs)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.options)
        self.driver.maximize_window()
        
        # 자동화 감지 우회
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        logger.info("브라우저 시작 완료")
        return self.driver
    
    def get_driver(self):
        """현재 드라이버 반환"""
        if not self.driver:
            self.setup_driver()
        return self.driver
    
    def quit(self):
        """브라우저 종료"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("브라우저 종료")
    
    def take_screenshot(self, filename):
        """스크린샷 저장"""
        if self.driver:
            self.driver.save_screenshot(filename)
            logger.info(f"스크린샷 저장: {filename}")
    
    def handle_alert(self, accept=True):
        """알림창 처리"""
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            
            if accept:
                alert.accept()
            else:
                alert.dismiss()
                
            logger.info(f"알림창 처리: {alert_text}")
            return alert_text
        except:
            return None