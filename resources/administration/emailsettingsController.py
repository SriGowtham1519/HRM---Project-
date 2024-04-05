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

#-----------------------------------------------------------------------------#
#-------------------------------- E - mail Settings --------------------------#
#-----------------------------------------------------------------------------#

@router.get('/emailsettings')
async def home(request:Request,db:Session=Depends(get_db)):
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
                            php_email_settings=db.query(models.PHP_Email).filter(models.PHP_Email.status=='ACTIVE').all();
                            smtp_email_settings=db.query(models.SMTP_Email).filter(models.SMTP_Email.status=='ACTIVE').all();
                            if php_email_settings or smtp_email_settings:
                                if php_email_settings:
                                    if smtp_email_settings:
                                        return templates.TemplateResponse("Admin/Administration/Settings/email-settings.html",context={"request":request,'emp_data':emp_data,"php_email_settings":php_email_settings,"smtp_email_settings":smtp_email_settings})
                                    else:
                                        return templates.TemplateResponse("Admin/Administration/Settings/email-settings.html",context={"request":request,'emp_data':emp_data,"php_email_settings":php_email_settings,"smtp_email_settings":" "})
                                else:
                                    if php_email_settings:
                                        return templates.TemplateResponse("Admin/Administration/Settings/email-settings.html",context={"request":request,'emp_data':emp_data,"php_email_settings":php_email_settings,"smtp_email_settings":smtp_email_settings})
                                    else:
                                        return templates.TemplateResponse("Admin/Administration/Settings/email-settings.html",context={"request":request,'emp_data':emp_data,"php_email_settings":" ","smtp_email_settings":smtp_email_settings})
                            else:
                                return templates.TemplateResponse("Admin/Administration/Settings/email-settings.html",context={"request":request,'emp_data':emp_data,"php_email_settings":" ","smtp_email_settings":" "})
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
    
@router.post('/emailSettings')
async def emailSettings(request:Request,db:Session=Depends(get_db),mailoption:Optional[str]=Form('None'),phpEmail:str=Form('None'),phpName:str=Form('None'),smtpHost:str=Form('None'),smtpUser:str=Form('None'),smtpPassword:str=Form('None'),smtpPort:str=Form('None'),smtpSecurity:str=Form('None'),smtpAuthentication:str=Form('None')):
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
                            if(mailoption=="option1"):
                                user_data=db.query(models.PHP_Email).all()
                                if user_data:
                                    
                                    db.query(models.PHP_Email).update({"Email":phpEmail,"Name": phpName})
                                    db.commit()
                                    return RedirectResponse('/HrmTool/Administration/emailsettings',status_code=303)
                                else:
                                    body=models.PHP_Email(Email=phpEmail,Name=phpName,status="ACTIVE",created_by=loginer_id)
                                    db.add(body)
                                    db.commit()
                                    return RedirectResponse('/HrmTool/Administration/emailsettings',status_code=303)
                            else:
                                user_data=db.query(models.SMTP_Email).all()
                                if user_data:
                                    db.query(models.SMTP_Email).update({"SMTP_HOST":smtpHost,"SMTP_USER":smtpUser,"SMTP_PASSWORD":smtpPassword,"SMTP_PORT":smtpPort,"SMTP_Security":smtpSecurity,"Authentication_Domain":smtpAuthentication})
                                    db.commit()
                                    return RedirectResponse('/HrmTool/Administration/emailsettings',status_code=303)
                                else:
                                    body=models.SMTP_Email(SMTP_HOST=smtpHost,SMTP_USER=smtpUser,SMTP_PASSWORD=smtpPassword,SMTP_PORT=smtpPort,SMTP_Security=smtpSecurity,Authentication_Domain=smtpAuthentication,status="ACTIVE",created_by=loginer_id)
                                    print(body)
                                    db.add(body)
                                    db.commit()
                                    return RedirectResponse('/HrmTool/Administration/emailsettings',status_code=303)
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
        
      