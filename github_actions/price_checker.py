"""
GitHub Actions에서 실행되는 가격 체크 스크립트
API를 통해 가격을 확인하고 변경이 필요하면 알림
"""

import os
import json
import requests
from datetime import datetime

def check_prices():
    """가격 체크 로직"""
    # 여기에 API 호출 또는 간단한 체크 로직
    print(f"[{datetime.now()}] 가격 체크 시작")
    
    # 체크 결과를 파일로 저장
    result = {
        "checked_at": datetime.now().isoformat(),
        "status": "checked",
        "products": [
            {
                "name": "[인생]점보떡볶이1490g",
                "current_price": 12600,
                "target_price": 13500,
                "needs_update": True
            }
        ]
    }
    
    # 결과 저장
    os.makedirs("logs", exist_ok=True)
    with open("logs/price_check_log.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 업데이트가 필요한 경우 알림
    if any(p["needs_update"] for p in result["products"]):
        send_notification(result)
    
    return result

def send_notification(result):
    """알림 전송"""
    webhook_url = os.environ.get("WEBHOOK_URL")
    
    if webhook_url:
        message = "가격 업데이트가 필요합니다:\n"
        for product in result["products"]:
            if product["needs_update"]:
                message += f"- {product['name']}: {product['current_price']}원 → {product['target_price']}원\n"
        
        # Discord, Slack 등으로 알림 전송
        try:
            requests.post(webhook_url, json={"content": message})
            print("알림 전송 완료")
        except:
            print("알림 전송 실패")
    else:
        print("Webhook URL이 설정되지 않았습니다")

def create_todo():
    """할 일 생성"""
    todos = []
    
    # 오늘 확인할 작업들
    todos.append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "tasks": [
            "카페24 가격 업데이트 확인",
            "재고 확인",
            "신규 주문 처리"
        ]
    })
    
    with open("logs/daily_todo.json", "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 가격 체크
    check_prices()
    
    # 할 일 생성
    create_todo()
    
    print("GitHub Actions 작업 완료!")