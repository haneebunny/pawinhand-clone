"""
routers/questions.py — [개발자 A] 보호소 질문지 및 사전 검진 질문 조회 API.
"""
from typing import List
from fastapi import APIRouter, HTTPException

from ..schemas import QuestionInput, QuestionResponse
from .. import rag

router = APIRouter(prefix="/api", tags=["questions"])


from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .. import rag

router = APIRouter(prefix="/api", tags=["questions"])

class QuestionRequest(BaseModel):
    species: Optional[str] = "dog"
    housing: Optional[str] = None
    out_hours: Optional[str] = None
    walk_time: Optional[str] = None
    pet_experience: Optional[str] = None
    budget: Optional[str] = None
    child_plan: Optional[str] = None

def get_category_by_title(title: str) -> str:
    title_lower = title.lower()
    if any(x in title_lower for x in ["가족", "동의", "이사", "수명", "책임", "파양", "비용", "예산", "양육비", "돈", "경제"]):
        return "입양절차"
    elif any(x in title_lower for x in ["알레르기", "fel", "건강", "질병", "중성화", "예방", "의료", "아픈"]):
        return "건강상태"
    elif any(x in title_lower for x in ["짖음", "하울링", "배변", "분리불안", "공포", "공격성", "입질", "물", "성격", "성향"]):
        return "행동/성격"
    elif any(x in title_lower for x in ["산책", "활동성", "에너지", "시간"]):
        return "산책/활동"
    elif any(x in title_lower for x in ["사회성", "사회화", "합사", "교감", "사람", "어울"]):
        return "사회성"
    return "입양절차"

@router.post("/questions")
def get_questions(payload: QuestionRequest):
    """
    지정된 축종(dog 또는 cat)에 맞는 사전 입양 자가점검 및 심사 질문지 목록을 반환합니다.
    """
    species_lower = (payload.species or "dog").strip().lower()
    
    if species_lower not in ("dog", "cat"):
        species_lower = "dog"
        
    try:
        all_questions = rag.load_screening_questions()
    except Exception as e:
        print(f"[questions] 질문 데이터 로드 오류: {e}")
        return {"questions": [], "checklist": []}
    
    # Filter by species
    filtered_raw = [
        q for q in all_questions
        if q.get("species", "").strip().lower() == species_lower
    ]
    
    # Map to frontend expected format: [{"category": "...", "text": "..."}]
    questions_list = []
    checklist_set = set()
    
    for q in filtered_raw:
        title = q.get("title", "")
        category = get_category_by_title(title)
        
        # We can formulate 1-2 practical questions from this RAG screening item
        criteria = q.get("criteria", [])
        if criteria:
            for c in criteria[:2]: # Get up to 2 items
                questions_list.append({
                    "category": category,
                    "text": c
                })
                # Add to checklist as well
                checklist_set.add(c)
        else:
            # Fallback to guide/title
            questions_list.append({
                "category": category,
                "text": q.get("guide", title)
            })
            
    # Default fallback checklist items if too short
    default_checklist = [
        "동물을 평생 책임지고 키울 수 있는 경제적 여건이 마련되었나요?",
        "가족 구성원 전원이 입양에 동의했나요?",
        "소음이나 알레르기 등으로 인한 이웃과의 마찰 대비책이 있나요?",
        "동물이 혼자 지낼 시간의 한계를 알고 있으며, 이에 대비하셨나요?",
        "반려동물이 거주할 공간 내 위험 물질 및 탈출 경로를 차단하셨나요?"
    ]
    
    checklist_list = list(checklist_set) if len(checklist_set) >= 3 else default_checklist
    
    return {
        "questions": questions_list[:25],
        "checklist": checklist_list[:5]
    }
