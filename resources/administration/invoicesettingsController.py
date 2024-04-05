from typing import Dict, List,Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Depends, FastAPI, Request, Form,status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi.encoders import jsonable_encoder
# from models.schemas import masterSchemas
import base64
import shutil,uuid,os
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
#-------------------------------- invoices settings --------------------------#
#-----------------------------------------------------------------------------#

@router.get('/invoices_settings')
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
                            invocies_data = db.query(models.Invoice_Settings).filter(models.Invoice_Settings.status=='ACTIVE').first()
                            return templates.TemplateResponse("Admin/Administration/Settings/invoice-settings.html",context={"request":request,'emp_data':emp_data,'invocies_data':invocies_data})
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
    
@router.post('/invoices_settings')
async def emailSettings(request:Request,db:Session=Depends(get_db),invoicePrefix:str=Form(...),invoiceFile:UploadFile=Form(...),):
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

                            user_data=db.query(models.Invoice_Settings).all()
                            
                            file_type = invoiceFile.content_type
                            extention = file_type.split('/')[-1]
                            print(extention)

                            if user_data:
                                print('fdff')
                                if extention != 'octet-stream':
                                    token_image = str(uuid.uuid4()) + '.' + str(extention)
                                    file_location =  f"./templates/assets/uploaded_files/{token_image}"
                                    with open(file_location, 'wb+') as file_object:
                                        shutil.copyfileobj(invoiceFile.file, file_object)

                                        db.query(models.Invoice_Settings).update({"Invoice_Logo":token_image})
                                        db.commit()

                                db.query(models.Invoice_Settings).update({"Invoice_prefix":invoicePrefix})
                                db.commit()

                                return RedirectResponse('/HrmTool/Administration/invoices_settings',status_code=302)
                                

                            else:
                                if extention != 'octet-stream':
                                    token_image = str(uuid.uuid4()) + '.' + str(extention)
                                    file_location =  f"./templates/assets/uploaded_files/{token_image}"
                                    with open(file_location, 'wb+') as file_object:
                                        shutil.copyfileobj(invoiceFile.file, file_object)
                                    body=models.Invoice_Settings(Invoice_prefix=invoicePrefix,Invoice_Logo=token_image,status="ACTIVE",created_by=loginer_id)
                                    db.add(body)
                                    db.commit() 
                                    alert_script = f"""
                                        <script>
                                            alert("Settings saved successfully!");
                                            window.location.href = "/HrmTool/Administration/invoices_settings"; 
                                        </script>
                                    """
                                    return RedirectResponse('/HrmTool/Administration/invoices_settings',status_code=302)
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
