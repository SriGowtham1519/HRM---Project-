from typing import Dict, List,Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Depends, FastAPI, Request, Form,status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi.encoders import jsonable_encoder
# from models.schemas import masterSchemas
import base64
import shutil,uuid
from configs.base_config import BaseConfig
from jose import jwt, JWTError
# from django.contrib import messages
from datetime import datetime 
from models import get_db, models
from sqlalchemy.orm import Session
from sqlalchemy import text

router = APIRouter()

templates = Jinja2Templates(directory="templates")

current_datetime = datetime.today()

@router.get("/dashboard")
async def Product_page(request: Request,db: Session = Depends(get_db)):
    try:
        if 'loginer_details' in request.session:
            token = request.session['loginer_details']
            try:
                payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
                loginer_id : int= payload.get("empid") 
                try:
                    if loginer_id:
                        emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
                        if emp_data.Lock_screen == 'OFF':
                            employee_data = len(db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all())
                            task_data = len(db.query(models.Task).filter(models.Task.status=='ACTIVE').all())
                            client_data = db.query(models.Client).filter(models.Client.status=='ACTIVE').all()
                            project_data = db.query(models.Project).filter(models.Project.status=='ACTIVE').all()
                            # new_employee = len(db.query(models.Employee).from_statement(text(f"select * from employee where created_at={formatted_string} and status='ACTIVE' ")).all())
                            return templates.TemplateResponse('Admin/Main/Dashboard/admin-dashboard.html', context={'request': request,'emp_data':emp_data,
                            'employee_data':employee_data,'task_data':task_data,'client_data':client_data,'project_data':project_data})
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/Error',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})
    