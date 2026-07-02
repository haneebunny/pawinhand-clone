"""
routers/votes.py — [개발자 B] 이름 지어주기 투표 API.

- GET /api/animals/{animal_id}/votes : 해당 동물의 이름 후보 및 득표수 조회
- POST /api/animals/{animal_id}/vote : 해당 동물에게 새로운 이름 추천 또는 투표
  - 득표수가 5표 이상 달성 시 원본 animals.json의 name 필드를 공식 이름으로 자동 업데이트합니다.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status

from app.schemas import VotesResponse, CandidateSchema, VoteInput
from app.rag import load_animals, save_animals, load_votes, save_votes

router = APIRouter(
    prefix="/api/animals",
    tags=["name-votes"],
)

# 기본 시연용 초기 후보군 데이터 생성 헬퍼
def get_or_create_animal_votes(animal_id: str, votes_data: dict) -> dict:
    if animal_id not in votes_data:
        # 썰렁하지 않도록 기본 3가지 후보군 사전 득표 상태 세팅
        votes_data[animal_id] = [
            {"name": "누룽지", "votes": 4},
            {"name": "버터", "votes": 3},
            {"name": "초코", "votes": 1}
        ]
        save_votes(votes_data)
    return votes_data[animal_id]


@router.get("/{animal_id}/votes", response_model=VotesResponse)
def get_name_votes(animal_id: str):
    """
    특정 유기동물의 이름 투표 리스트를 조회합니다.
    """
    # 1. 원본 동물의 이름 상태 검사
    animals = load_animals()
    target_animal = next((a for a in animals if a.get("id") == animal_id), None)
    
    if not target_animal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="동물 정보를 찾을 수 없습니다."
        )

    # 2. 이미 공식 이름이 지정되어 있는지 확인 (기존 이름이 '이름 없음', '지어주세요' 등이 아닌 유의미한 이름인 경우)
    orig_name = target_animal.get("name", "").strip()
    is_nameless = not orig_name or "없음" in orig_name or "지어주세요" in orig_name
    
    if not is_nameless:
        # 공식 이름이 확정된 상태이므로 투표 후보군 없이 확정 이름만 반환
        return VotesResponse(confirmed_name=orig_name, candidates=[])

    # 3. 투표 정보 파일 로드
    votes_data = load_votes()
    candidates_list = get_or_create_animal_votes(animal_id, votes_data)

    # 4. 투표 리스트 중 혹시 5표 이상인 것이 있는지 이중 검사
    confirmed_name = None
    sorted_candidates = sorted(candidates_list, key=lambda x: x["votes"], reverse=True)
    
    for c in sorted_candidates:
        if c["votes"] >= 5:
            confirmed_name = c["name"]
            break

    # 5. 5표 이상 획득한 이름이 발견되었으나 아직 원본 animals.json에 반영되지 않은 경우 백업 동기화
    if confirmed_name and is_nameless:
        for a in animals:
            if a.get("id") == animal_id:
                a["name"] = confirmed_name
                break
        save_animals(animals)

    # 6. CandidateSchema Pydantic 형태로 매핑
    candidates = [
        CandidateSchema(name=c["name"], votes=c["votes"])
        for c in sorted_candidates
    ]

    return VotesResponse(
        confirmed_name=confirmed_name,
        candidates=candidates
    )


@router.post("/{animal_id}/vote", response_model=VotesResponse)
def submit_name_vote(animal_id: str, payload: VoteInput):
    """
    이름 후보를 신규 등록(추천)하거나, 기존 후보에게 투표를 던집니다.
    득표수가 5표 이상이 되면 공식 이름으로 자동 확정 및 데이터베이스(animals.json)를 갱신합니다.
    """
    animals = load_animals()
    target_animal = next((a for a in animals if a.get("id") == animal_id), None)
    
    if not target_animal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="동물 정보를 찾을 수 없습니다."
        )

    orig_name = target_animal.get("name", "").strip()
    is_nameless = not orig_name or "없음" in orig_name or "지어주세요" in orig_name
    
    if not is_nameless:
        return VotesResponse(confirmed_name=orig_name, candidates=[])

    # 투표 데이터 로드 및 갱신
    votes_data = load_votes()
    candidates_list = get_or_create_animal_votes(animal_id, votes_data)
    
    vote_name = payload.name.strip()
    
    # 중복 후보 검사 및 카운트 증가
    matched = False
    for c in candidates_list:
        if c["name"] == vote_name:
            c["votes"] += 1
            matched = True
            break
            
    if not matched:
        # 새로운 후보 등록 시 기본 1표 획득
        candidates_list.append({"name": vote_name, "votes": 1})

    # 저장소 파일 동기화
    votes_data[animal_id] = candidates_list
    save_votes(votes_data)

    # 5표 이상 획득 여부 체크
    confirmed_name = None
    sorted_candidates = sorted(candidates_list, key=lambda x: x["votes"], reverse=True)
    for c in sorted_candidates:
        if c["votes"] >= 5:
            confirmed_name = c["name"]
            break

    # 5표 도달 시 공식 이름으로 갱신 후 animals.json 파일 물리적 덮어쓰기
    if confirmed_name:
        for a in animals:
            if a.get("id") == animal_id:
                a["name"] = confirmed_name
                break
        save_animals(animals)

    candidates = [
        CandidateSchema(name=c["name"], votes=c["votes"])
        for c in sorted_candidates
    ]

    return VotesResponse(
        confirmed_name=confirmed_name,
        candidates=candidates
    )
