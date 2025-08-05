"""
대화형 웹 자동화 학습 시스템
사용자가 UI를 보면서 직접 가르치는 방식
"""

import os
import json
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


class InteractiveTeacher:
    def __init__(self):
        self.driver = None
        self.root = tk.Tk()
        self.root.title("🎓 웹 자동화 학습 시스템")
        self.root.geometry("800x600")
        
        # 학습 데이터
        self.current_site = None
        self.knowledge = {}
        self.recording = False
        self.workflow = []
        
        # UI 설정
        self.setup_ui()
        
        # 마우스 클릭 감지를 위한 JavaScript
        self.click_listener_script = """
        window.lastClickedElement = null;
        window.clickedElements = [];
        
        document.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            window.lastClickedElement = e.target;
            
            // 요소 정보 수집
            let info = {
                tagName: e.target.tagName,
                id: e.target.id,
                className: e.target.className,
                name: e.target.name,
                text: e.target.textContent.substring(0, 50),
                type: e.target.type,
                href: e.target.href,
                xpath: getXPath(e.target)
            };
            
            window.clickedElements.push(info);
            
            // 하이라이트
            e.target.style.border = '3px solid red';
            e.target.style.backgroundColor = 'yellow';
            
            console.log('Clicked:', info);
            
            return false;
        }, true);
        
        function getXPath(element) {
            if (element.id !== '')
                return '//*[@id="' + element.id + '"]';
            if (element === document.body)
                return element.tagName;
            
            var ix = 0;
            var siblings = element.parentNode.childNodes;
            for (var i = 0; i < siblings.length; i++) {
                var sibling = siblings[i];
                if (sibling === element)
                    return getXPath(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
                if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
                    ix++;
            }
        }
        """
        
    def setup_ui(self):
        """UI 구성"""
        # 상단 프레임
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # 사이트 정보
        ttk.Label(top_frame, text="사이트:").grid(row=0, column=0, padx=5)
        self.site_var = tk.StringVar(value="cafe24")
        site_entry = ttk.Entry(top_frame, textvariable=self.site_var, width=20)
        site_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(top_frame, text="URL:").grid(row=0, column=2, padx=5)
        self.url_var = tk.StringVar(value="https://manwonyori.cafe24.com/admin")
        url_entry = ttk.Entry(top_frame, textvariable=self.url_var, width=40)
        url_entry.grid(row=0, column=3, padx=5)
        
        # 버튼들
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(button_frame, text="🌐 브라우저 시작", 
                  command=self.start_browser).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="🎯 학습 모드", 
                  command=self.enable_learning_mode).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="📹 워크플로우 기록", 
                  command=self.toggle_recording).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="💾 저장", 
                  command=self.save_knowledge).grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="🤖 코드 생성", 
                  command=self.generate_code).grid(row=0, column=4, padx=5)
        
        # 중간 프레임 - 현재 상태
        status_frame = ttk.LabelFrame(self.root, text="현재 상태", padding="10")
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="대기 중...")
        self.status_label.grid(row=0, column=0)
        
        # 학습 프레임
        learn_frame = ttk.LabelFrame(self.root, text="요소 학습", padding="10")
        learn_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        # 요소 이름
        ttk.Label(learn_frame, text="요소 이름:").grid(row=0, column=0, sticky=tk.W)
        self.element_name_var = tk.StringVar()
        ttk.Entry(learn_frame, textvariable=self.element_name_var, width=30).grid(row=0, column=1, padx=5)
        
        # 요소 타입
        ttk.Label(learn_frame, text="요소 타입:").grid(row=1, column=0, sticky=tk.W)
        self.element_type_var = tk.StringVar(value="button")
        type_combo = ttk.Combobox(learn_frame, textvariable=self.element_type_var, 
                                 values=["button", "input", "link", "dropdown", "checkbox"])
        type_combo.grid(row=1, column=1, padx=5)
        
        # 학습 버튼
        ttk.Button(learn_frame, text="🖱️ 요소 클릭하고 학습", 
                  command=self.learn_from_click).grid(row=2, column=0, columnspan=2, pady=10)
        
        # 학습된 요소 표시
        self.element_listbox = tk.Listbox(learn_frame, height=8)
        self.element_listbox.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 로그 프레임
        log_frame = ttk.LabelFrame(self.root, text="로그", padding="10")
        log_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=80)
        self.log_text.grid(row=0, column=0)
        
        # 가중치 설정
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def log(self, message):
        """로그 메시지 추가"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def update_status(self, status):
        """상태 업데이트"""
        self.status_label.config(text=status)
        self.root.update()
        
    def start_browser(self):
        """브라우저 시작"""
        self.log("브라우저 시작 중...")
        
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
        # 창 크기 조정 (화면의 절반)
        self.driver.set_window_size(960, 1080)
        self.driver.set_window_position(0, 0)
        
        # 학습 도구 창도 위치 조정
        self.root.geometry("800x600+960+0")
        
        # URL로 이동
        url = self.url_var.get()
        if url:
            self.driver.get(url)
            self.current_site = self.site_var.get()
            
        self.log(f"브라우저 시작 완료: {url}")
        self.update_status("브라우저 실행 중")
        
    def enable_learning_mode(self):
        """학습 모드 활성화"""
        if not self.driver:
            messagebox.showwarning("경고", "먼저 브라우저를 시작하세요!")
            return
            
        self.log("학습 모드 활성화 중...")
        
        # 클릭 감지 스크립트 주입
        self.driver.execute_script(self.click_listener_script)
        
        self.log("학습 모드 활성화 완료")
        self.update_status("학습 모드 - 요소를 클릭하세요")
        
        messagebox.showinfo("학습 모드", 
                           "이제 브라우저에서 학습할 요소를 클릭하세요.\n"
                           "클릭한 요소는 노란색으로 표시됩니다.")
        
    def learn_from_click(self):
        """클릭한 요소 학습"""
        if not self.driver:
            messagebox.showwarning("경고", "브라우저가 실행되지 않았습니다!")
            return
            
        element_name = self.element_name_var.get()
        if not element_name:
            messagebox.showwarning("경고", "요소 이름을 입력하세요!")
            return
            
        # 마지막 클릭한 요소 정보 가져오기
        clicked_info = self.driver.execute_script("return window.lastClickedElement ? window.clickedElements[window.clickedElements.length - 1] : null;")
        
        if not clicked_info:
            messagebox.showwarning("경고", "클릭한 요소가 없습니다!\n학습 모드를 활성화하고 요소를 클릭하세요.")
            return
            
        self.log(f"요소 학습: {element_name}")
        self.log(f"  태그: {clicked_info['tagName']}")
        self.log(f"  ID: {clicked_info.get('id', 'N/A')}")
        self.log(f"  Class: {clicked_info.get('className', 'N/A')}")
        
        # 지식 저장
        if 'elements' not in self.knowledge:
            self.knowledge['elements'] = {}
            
        self.knowledge['elements'][element_name] = {
            'method': 'xpath',
            'value': clicked_info['xpath'],
            'type': self.element_type_var.get(),
            'tag': clicked_info['tagName'],
            'id': clicked_info.get('id', ''),
            'class': clicked_info.get('className', ''),
            'text': clicked_info.get('text', ''),
            'learned_at': datetime.now().isoformat()
        }
        
        # 대체 선택자 저장
        if clicked_info.get('id'):
            self.knowledge['elements'][element_name]['alternatives'] = {
                'id': clicked_info['id']
            }
        
        # 리스트박스에 추가
        self.element_listbox.insert(tk.END, f"{element_name} ({clicked_info['tagName']})")
        
        # 워크플로우에 추가
        if self.recording:
            self.workflow.append({
                'action': 'find_element',
                'element': element_name,
                'timestamp': datetime.now().isoformat()
            })
        
        self.log(f"✅ '{element_name}' 학습 완료!")
        
        # 클릭 기록 초기화
        self.driver.execute_script("window.lastClickedElement = null;")
        
    def toggle_recording(self):
        """워크플로우 기록 토글"""
        self.recording = not self.recording
        
        if self.recording:
            self.workflow = []
            self.log("📹 워크플로우 기록 시작")
            self.update_status("워크플로우 기록 중...")
        else:
            self.log(f"📹 워크플로우 기록 종료 (스텝: {len(self.workflow)})")
            self.update_status("워크플로우 기록 완료")
            
    def save_knowledge(self):
        """학습 내용 저장"""
        if not self.current_site:
            messagebox.showwarning("경고", "사이트 정보가 없습니다!")
            return
            
        # 저장 경로
        knowledge_dir = f"KNOWLEDGE_BASE/{self.current_site}"
        os.makedirs(knowledge_dir, exist_ok=True)
        
        # 요소 정보 저장
        elements_file = os.path.join(knowledge_dir, "elements.json")
        with open(elements_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge, f, ensure_ascii=False, indent=2)
            
        # 워크플로우 저장
        if self.workflow:
            workflow_file = os.path.join(knowledge_dir, f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(workflow_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'name': 'recorded_workflow',
                    'steps': self.workflow,
                    'created_at': datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
                
        self.log(f"✅ 지식 저장 완료: {knowledge_dir}")
        messagebox.showinfo("저장 완료", f"학습 내용이 저장되었습니다.\n{knowledge_dir}")
        
    def generate_code(self):
        """자동화 코드 생성"""
        if not self.knowledge.get('elements'):
            messagebox.showwarning("경고", "학습된 요소가 없습니다!")
            return
            
        code = f'''"""
{self.current_site} 자동화 스크립트
자동 생성: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 학습된 요소
elements = {json.dumps(self.knowledge['elements'], ensure_ascii=False, indent=4)}

def find_element(driver, element_name):
    """학습된 요소 찾기"""
    element_info = elements[element_name]
    return driver.find_element(By.XPATH, element_info['value'])

# 사용 예시
driver = webdriver.Chrome()
driver.get("{self.url_var.get()}")

# 학습된 요소 사용
'''
        
        # 코드 파일 저장
        code_file = f"GENERATED_SCRIPTS/{self.current_site}_automation.py"
        os.makedirs("GENERATED_SCRIPTS", exist_ok=True)
        
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write(code)
            
        self.log(f"✅ 코드 생성 완료: {code_file}")
        
        # 코드 표시 창
        code_window = tk.Toplevel(self.root)
        code_window.title("생성된 코드")
        code_window.geometry("800x600")
        
        code_text = scrolledtext.ScrolledText(code_window, wrap=tk.NONE)
        code_text.pack(fill=tk.BOTH, expand=True)
        code_text.insert(tk.END, code)
        
    def run(self):
        """메인 실행"""
        self.log("🎓 대화형 웹 자동화 학습 시스템 시작")
        self.log("브라우저를 시작하고 학습 모드를 활성화하세요.")
        
        # 창 닫기 이벤트
        def on_closing():
            if self.driver:
                self.driver.quit()
            self.root.destroy()
            
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.mainloop()


def main():
    teacher = InteractiveTeacher()
    teacher.run()


if __name__ == "__main__":
    main()