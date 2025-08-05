"""
워크플로우 실행 엔진
학습된 지식을 바탕으로 작업 순서 실행
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import logging

logger = logging.getLogger(__name__)


class WorkflowEngine:
    """워크플로우 실행 엔진"""
    
    def __init__(self):
        self.wait_time = 10
        
    def find_element(self, driver, element_info):
        """학습된 방법으로 요소 찾기"""
        method = element_info.get('method', 'xpath')
        value = element_info.get('value')
        
        by_map = {
            'id': By.ID,
            'name': By.NAME,
            'class': By.CLASS_NAME,
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR,
            'text': By.LINK_TEXT,
            'partial_text': By.PARTIAL_LINK_TEXT
        }
        
        by_type = by_map.get(method, By.XPATH)
        
        try:
            element = WebDriverWait(driver, self.wait_time).until(
                EC.presence_of_element_located((by_type, value))
            )
            return element
        except Exception as e:
            logger.error(f"요소를 찾을 수 없음: {e}")
            return None
    
    def execute_step(self, driver, step, knowledge):
        """단일 스텝 실행"""
        action = step.get('action')
        element_name = step.get('element')
        
        # 요소 정보 가져오기
        element_info = knowledge.get('elements', {}).get(element_name)
        if not element_info:
            logger.error(f"알 수 없는 요소: {element_name}")
            return False
        
        # 요소 찾기
        element = self.find_element(driver, element_info)
        if not element:
            return False
        
        # 액션 실행
        try:
            if action == 'click':
                element.click()
                logger.info(f"클릭: {element_name}")
                
            elif action == 'input':
                value = step.get('value', '')
                element.clear()
                element.send_keys(value)
                logger.info(f"입력: {element_name} = {value}")
                
            elif action == 'select':
                value = step.get('value', '')
                select = Select(element)
                select.select_by_visible_text(value)
                logger.info(f"선택: {element_name} = {value}")
                
            elif action == 'wait':
                seconds = step.get('seconds', 1)
                time.sleep(seconds)
                logger.info(f"대기: {seconds}초")
                
            return True
            
        except Exception as e:
            logger.error(f"액션 실행 실패: {e}")
            return False
    
    def execute_workflow(self, driver, workflow, knowledge):
        """전체 워크플로우 실행"""
        logger.info(f"워크플로우 실행 시작: {workflow.get('name', 'Unknown')}")
        
        success_count = 0
        total_steps = len(workflow.get('steps', []))
        
        for i, step in enumerate(workflow.get('steps', [])):
            logger.info(f"스텝 {i+1}/{total_steps} 실행 중...")
            
            if self.execute_step(driver, step, knowledge):
                success_count += 1
            else:
                logger.warning(f"스텝 {i+1} 실패")
        
        logger.info(f"워크플로우 완료: {success_count}/{total_steps} 성공")
        return success_count == total_steps