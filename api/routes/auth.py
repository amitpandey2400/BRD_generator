"""
API routes for authentication
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=Token)
async def login(request: LoginRequest):
    """User login endpoint"""
    # Implement authentication logic
    # For now, return a dummy token
    return {
        "access_token": "dummy_token",
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout():
    """User logout endpoint"""
    return {"message": "Logged out successfully"}
