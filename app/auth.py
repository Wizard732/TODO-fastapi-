from fastapi import HTTPException, Header

def verify_admin(task: str = Header(None)):
    if task != "admin":
        raise HTTPException(status_code=400,detail="Доступ ограничен")
