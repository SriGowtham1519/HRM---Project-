from typing import Dict, List,Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Depends, FastAPI, Request, Form ,status
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

@router.get('/resignation')
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
                            employee_datas = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                            department_datas=db.query(models.Department).filter(models.Department.status=='ACTIVE').all()
                            resigination_datas=db.query(models.Resignation).filter(models.Resignation.status=='ACTIVE').all()
                            return templates.TemplateResponse("Admin/Performance/Resignation/resignation.html",context={"request":request,'emp_data':emp_data,'employee_datas':employee_datas,"department_datas":department_datas,"resigination_datas":resigination_datas})
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
    
@router.post('/resiginationSave')
async def emailSettings(request:Request,db:Session=Depends(get_db),employeeName:str=Form(...),noticeDate:str=Form(...),resignationDate:str=Form(...),reason:str=Form(...)):
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
                            check_resig_data = db.query(models.Resignation).filter(models.Resignation.Employee_id==employeeName).filter(models.Resignation.status=='ACTIVE').first()
                            if not check_resig_data:
                                body=models.Resignation(Employee_id=employeeName,Notice_Date=noticeDate,Date=resignationDate,Reason=reason,status="ACTIVE",created_by=loginer_id)
                                db.add(body)
                                db.commit()

                                # #After resignation employee remove from the table also ... 
                                # db.query(models.Employee).filter(models.Employee.id==employeeName).update({'status':'INACTIVE'})
                                # db.commit()

                                response_data = jsonable_encoder({"Result":"Done"})
                                return JSONResponse(content=response_data,status_code=200)
                            else:
                                response_data = jsonable_encoder({"Result":"Error"})
                                return JSONResponse(content=response_data,status_code=200)
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

@router.get('/getid/{main_id}')
def getid(main_id:int,request:Request,db:Session=Depends(get_db)):
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
                            employee_datas = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                            resigination_data = db.query(models.Resignation).filter(models.Resignation.id==main_id).filter(models.Resignation.status=='ACTIVE').first()
                            return {"resigination_data":resigination_data,"employee_datas":employee_datas}
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
    
@router.post('/updateData')
def updatedata(request:Request,db:Session=Depends(get_db),edit_id:str=Form(...),edit_notice:str=Form(...),edit_date:str=Form(...),edit_reason:str=Form(...)):
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
                            db.query(models.Resignation).filter(models.Resignation.id==edit_id).update({"Notice_Date": edit_notice,"Date":edit_date,"Reason":edit_reason})
                            db.commit()
                            print(Request)
                            return RedirectResponse('/HrmTool/Performance/resignation',status_code=303)
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
    
@router.post('/delete')
def delete(request:Request,db:Session=Depends(get_db),delete_id:int=Form(...)):       
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
                            resigination_data = db.query(models.Resignation).filter(models.Resignation.id==delete_id).filter(models.Resignation.status=='ACTIVE').first()
                            print(resigination_data)
                            if resigination_data:
                                    db.query(models.Resignation).filter(models.Resignation.id==delete_id).update({"status":"INACTIVE"})
                                    db.commit()
                            return RedirectResponse('/HrmTool/Performance/resignation',status_code=303)
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