"""
패턴 관리자 - 학습한 패턴을 관리하고 재사용
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional


class PatternManager:
    """범용 패턴 관리 클래스"""
    
    def __init__(self, base_dir: str = "KNOWLEDGE_BASE"):
        self.base_dir = base_dir
        self.universal_patterns_dir = os.path.join(base_dir, "UNIVERSAL_PATTERNS")
        self.patterns = self.load_all_patterns()
        
    def load_all_patterns(self) -> Dict:
        """모든 패턴 로드"""
        patterns = {}
        
        # 범용 패턴 로드
        if os.path.exists(self.universal_patterns_dir):
            for file in os.listdir(self.universal_patterns_dir):
                if file.endswith('.json'):
                    pattern_type = file.replace('.json', '')
                    with open(os.path.join(self.universal_patterns_dir, file), 'r', encoding='utf-8') as f:
                        patterns[pattern_type] = json.load(f)
                        
        return patterns
    
    def find_similar_pattern(self, element_purpose: str, site_type: str = None) -> Optional[Dict]:
        """유사한 패턴 찾기"""
        # 1. 정확한 매칭
        if element_purpose in self.patterns.get('common_elements', {}):
            return self.patterns['common_elements'][element_purpose]
            
        # 2. 키워드 기반 매칭
        keywords = element_purpose.lower().split()
        for pattern_type, patterns in self.patterns.items():
            for pattern_name, pattern_data in patterns.items():
                if any(keyword in pattern_name.lower() for keyword in keywords):
                    return pattern_data
                    
        return None
    
    def save_new_pattern(self, pattern_name: str, pattern_data: Dict, category: str = "custom"):
        """새 패턴 저장"""
        pattern_file = os.path.join(self.universal_patterns_dir, f"{category}_patterns.json")
        
        # 기존 패턴 로드
        if os.path.exists(pattern_file):
            with open(pattern_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        else:
            existing = {}
            
        # 새 패턴 추가
        existing[pattern_name] = {
            **pattern_data,
            "created_at": datetime.now().isoformat(),
            "usage_count": 0
        }
        
        # 저장
        os.makedirs(self.universal_patterns_dir, exist_ok=True)
        with open(pattern_file, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
            
    def extract_pattern_from_site(self, site_name: str) -> Dict:
        """특정 사이트에서 패턴 추출"""
        site_knowledge_dir = os.path.join(self.base_dir, site_name)
        extracted_patterns = {
            "login": None,
            "search": None,
            "navigation": None
        }
        
        if os.path.exists(site_knowledge_dir):
            # elements.json 분석
            elements_file = os.path.join(site_knowledge_dir, "elements.json")
            if os.path.exists(elements_file):
                with open(elements_file, 'r', encoding='utf-8') as f:
                    elements = json.load(f)
                    
                # 로그인 패턴 추출
                login_elements = self._extract_login_pattern(elements)
                if login_elements:
                    extracted_patterns["login"] = login_elements
                    
                # 검색 패턴 추출
                search_elements = self._extract_search_pattern(elements)
                if search_elements:
                    extracted_patterns["search"] = search_elements
                    
        return extracted_patterns
    
    def _extract_login_pattern(self, elements: Dict) -> Optional[Dict]:
        """로그인 관련 요소 추출"""
        login_keywords = ['login', '로그인', 'id', '아이디', 'password', '비밀번호']
        login_elements = {}
        
        for elem_name, elem_data in elements.get('elements', {}).items():
            if any(keyword in elem_name.lower() for keyword in login_keywords):
                # 요소 타입 분류
                if 'id' in elem_name.lower() or '아이디' in elem_name:
                    login_elements['username_field'] = elem_data
                elif 'password' in elem_name.lower() or '비밀번호' in elem_name:
                    login_elements['password_field'] = elem_data
                elif 'button' in str(elem_data.get('type', '')) or '버튼' in elem_name:
                    login_elements['login_button'] = elem_data
                    
        return login_elements if len(login_elements) >= 2 else None
    
    def _extract_search_pattern(self, elements: Dict) -> Optional[Dict]:
        """검색 관련 요소 추출"""
        search_keywords = ['search', '검색', 'keyword', '키워드', 'query']
        search_elements = {}
        
        for elem_name, elem_data in elements.get('elements', {}).items():
            if any(keyword in elem_name.lower() for keyword in search_keywords):
                if 'input' in str(elem_data.get('type', '')):
                    search_elements['search_input'] = elem_data
                elif 'button' in str(elem_data.get('type', '')):
                    search_elements['search_button'] = elem_data
                elif 'select' in str(elem_data.get('type', '')):
                    search_elements['search_category'] = elem_data
                    
        return search_elements if search_elements else None
    
    def apply_pattern_to_new_site(self, pattern: Dict, site_name: str) -> Dict:
        """패턴을 새 사이트에 적용"""
        adapted_pattern = {}
        
        for element_role, element_data in pattern.items():
            # 기본 정보는 유지하되, 사이트별 조정 가능
            adapted_pattern[element_role] = {
                **element_data,
                "adapted_for": site_name,
                "needs_validation": True
            }
            
        return adapted_pattern
    
    def get_pattern_success_rate(self, pattern_name: str) -> float:
        """패턴 성공률 조회"""
        # 실제로는 로그에서 계산
        # 여기서는 예시값
        return 0.85
    
    def suggest_patterns_for_site(self, site_url: str) -> List[str]:
        """사이트 URL 기반 패턴 제안"""
        suggestions = []
        
        # URL 분석
        if 'admin' in site_url or 'manage' in site_url:
            suggestions.append("admin_login_pattern")
            suggestions.append("admin_navigation_pattern")
        
        if 'shop' in site_url or 'store' in site_url:
            suggestions.append("ecommerce_pattern")
            suggestions.append("product_search_pattern")
            
        if 'blog' in site_url:
            suggestions.append("blog_posting_pattern")
            
        return suggestions


# 사용 예시
if __name__ == "__main__":
    pm = PatternManager()
    
    # 카페24에서 패턴 추출
    cafe24_patterns = pm.extract_pattern_from_site("cafe24")
    print("카페24 패턴:", cafe24_patterns)
    
    # 네이버에 적용
    if cafe24_patterns.get("login"):
        naver_login = pm.apply_pattern_to_new_site(cafe24_patterns["login"], "naver")
        print("네이버용 로그인 패턴:", naver_login)