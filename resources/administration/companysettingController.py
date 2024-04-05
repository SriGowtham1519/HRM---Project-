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

#-----------------------------------------------------------------------------------------------------------------#
#------------------------------------------------ Company Settings -----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

@router.get('/company_settings') 
def get_form(request:Request,db:Session = Depends(get_db)):
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
                            asset_data = db.query(models.Asset).filter(models.Asset.status=='ACTIVE').all()
                            company = db.query(models.Company_Settings).filter(models.Company_Settings.status=='ACTIVE').first()
                            return templates.TemplateResponse("Admin/Administration/Settings/settings.html",context={"request":request,'emp_data':emp_data,'asset_data':asset_data,'company':company})
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
    
@router.post('/company_settings')
def EmployeeRegisteration(request:Request,db:Session = Depends(get_db),Company_Name:str=Form(...),Contact_Person:str=Form(...),Address:str=Form(...),Country:str=Form(...),City:str=Form(...),State:str=Form(...),Postal_Code:str=Form(...),Email:str=Form(...),Phone_Number:str=Form(...),Mobile_Number:str=Form(...),Fax:str=Form(...),Website_Url:str=Form(...)): 
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
                            check_db = db.query(models.Company_Settings).filter(models.Company_Settings.status=="ACTIVE").all()
                            try:
                                if check_db==[]:
                                    body = models.Company_Settings(Company_Name=Company_Name,Contact_Person=Contact_Person,Address=Address,Country=Country,City=City,State=State,Postal_Code=Postal_Code,Email=Email,Phone_Number=Phone_Number,Mobile_Number=Mobile_Number,Fax=Fax, Website_Url = Website_Url ,status="ACTIVE",created_by=loginer_id)
                                    db.add(body)
                                    db.commit()
                                else:
                                    db.query(models.Company_Settings).update({"Company_Name":Company_Name,"Contact_Person":Contact_Person,"Address":Address,"Country":Country,"City":City,"State":State,"Postal_Code":Postal_Code,"Email":Email,"Phone_Number":Phone_Number,"Mobile_Number":Mobile_Number,"Fax":Fax,"Website_Url":Website_Url})
                                    db.commit()
                                return RedirectResponse("/HrmTool/Administration/company_settings",status_code=302)
                            except:
                                return RedirectResponse("/HrmTool/Administration/company_settings",status_code=302)
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