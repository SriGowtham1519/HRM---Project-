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
from sqlalchemy import text,func,update

router = APIRouter()

templates = Jinja2Templates(directory="templates")

current_datetime = datetime.today()

#                                 *********** A S S E S T S ***********


@router.get('/localization') 
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
                            localization_data = db.query(models.Localization_Settings).filter(models.Localization_Settings.status=='ACTIVE').first()
                            return templates.TemplateResponse("Admin/Administration/Settings/localization.html",context={"request":request,'emp_data':emp_data,'localization_data':localization_data})
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/HrmTool/login/login',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"}) 
    
@router.post('/localization')
def Localization_Settings(request:Request,db:Session=Depends(get_db),default_Country:str=Form(...),date_Format:str=Form(...),timezone:str=Form(...),default_Language:str=Form(...),currency_Code:str=Form(...),currency_Symbol:str=Form(...)):
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
                            check_db = db.query(models.Localization_Settings).filter(models.Localization_Settings.status=='ACTIVE').all()
                            try:
                                if check_db==[]:
                                    body = models.Localization_Settings(Default_Country=default_Country,Date_Format=date_Format,Timezone=timezone,Default_Language=default_Language,Currency_Code=currency_Code,Currency_Symbol=currency_Symbol,status="ACTIVE",created_by=loginer_id)
                                    print("thid id mew",body)
                                    db.add(body)
                                    db.commit()
                                    return RedirectResponse("/HrmTool/Administration/localization",status_code=302)
                                else:
                                    db.query(models.Localization_Settings).update({"Default_Country":default_Country,"Date_Format":date_Format,"Timezone":timezone,"Default_Language":default_Language,"Currency_Code":currency_Code,"Currency_Symbol":currency_Symbol})
                                    print(date_Format)
                                    db.commit()
                                    return RedirectResponse("/HrmTool/Administration/localization",status_code=302)
                            except:
                                print('error')
                                return templates.TemplateResponse("localization.html",context={"request":request,"method":"Post"})
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/HrmTool/login/login',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)   
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"}) 