from fastapi import HTTPException, Request


def get_current_user_id(request: Request) -> str:
    user_id = request.cookies.get("session_user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return user_id
