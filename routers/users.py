from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status 
from typing import Optional, List
from uuid import UUID


router = APIRouter()