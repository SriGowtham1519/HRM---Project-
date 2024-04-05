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
from icecream import ic
router = APIRouter()

templates = Jinja2Templates(directory="templates")

current_datetime = datetime.today()

@router.get('/termination')
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
                            termination_data = db.query(models.Termination).filter(models.Termination.status=='ACTIVE').all()
                            department_data = db.query(models.Department).filter(models.Department.status=='ACTIVE').all()
                            employee_datas = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                            termination_type_data = db.query(models.Termination_Type).filter(models.Termination_Type.status=='ACTIVE').all()
                            return templates.TemplateResponse("Admin/Performance/Termination/termination.html",context={"request":request,'emp_data':emp_data,'employee_datas':employee_datas,"termination_type_data":termination_type_data,"termination_data":termination_data,'department_data':department_data})
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
  
@router.get('/termination_type')
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
                            termination_type_data = db.query(models.Termination_Type).filter(models.Termination_Type.status=='ACTIVE').all()
                            return templates.TemplateResponse("Admin/Performance/Termination/termination_type.html",context={"request":request,'emp_data':emp_data,'termination_type_data':termination_type_data})
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
    
@router.post('/termination_type')
async def home(request:Request,db:Session=Depends(get_db),name:str=Form(...)):
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
                            check_data = db.query(models.Termination_Type).filter(models.Termination_Type.Name==name).filter(models.Termination_Type.status=='ACTIVE').all()
                            if not check_data:
                                add_type_data = models.Termination_Type(Name=name,status='ACTIVE',created_by=loginer_id)
                                db.add(add_type_data)
                                db.commit()
                                db.refresh(add_type_data)
                                response_data = jsonable_encoder({'Result':'Done'})
                                return JSONResponse(content=response_data,status_code=200)
                            else:
                                response_data = jsonable_encoder({'Result':'Error'})
                                return JSONResponse(content=response_data,status_code=200)
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
   
@router.get('/termination_type_id/{ids}')
async def home(request:Request,ids:int,db:Session=Depends(get_db)):
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
                            termination_data_id = db.query(models.Termination_Type).filter(models.Termination_Type.id==ids).filter(models.Termination_Type.status=='ACTIVE').first()
                            response_data = jsonable_encoder({'Result':termination_data_id})
                            return JSONResponse(content=response_data,status_code=200)
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
    
@router.post('/termination_type_update')
async def home(request:Request,db:Session=Depends(get_db),edit_idz:int=Form(...),edit_name:str=Form(...)):
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
                            check_data = db.query(models.Termination_Type).filter(models.Termination_Type.id!=edit_idz,models.Termination_Type.Name==edit_name).filter(models.Termination_Type.status=='ACTIVE').all()
                            if not check_data:
                                db.query(models.Termination_Type).filter(models.Termination_Type.id==edit_idz).update({'Name':edit_name})
                                db.commit()
                                response_data = jsonable_encoder({'Result':'Done'})
                                return JSONResponse(content=response_data,status_code=200)
                            else:
                                response_data = jsonable_encoder({'Result':'Error'})
                                return JSONResponse(content=response_data,status_code=200)
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
   
@router.get('/delete_termination_type/{ids}')
async def home(request:Request,ids:int,db:Session=Depends(get_db)):
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
                            db.query(models.Termination_Type).filter(models.Termination_Type.id==ids).update({'status':'INACTIVE'})
                            db.commit()
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
   
@router.post('/termination')
async def home(request:Request,db:Session=Depends(get_db),employee_id:str=Form(...),term_type:str=Form(...),term_date:str=Form(...),term_res:str=Form(...),notice_date:str=Form(...)):
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
                            check_data = db.query(models.Termination).filter(models.Termination.Employee_id==employee_id).filter(models.Termination.status=='ACTIVE').all()
                            if not check_data:
                                add_termination = models.Termination(Employee_id=employee_id,Termination_Type_id=term_type,Date=term_date,Reason=term_res,Notice_Date=notice_date,status='ACTIVE',created_by=loginer_id)
                                db.add(add_termination)
                                db.commit()
                                db.refresh(add_termination)
                                #
                                response_data = jsonable_encoder({'Result':'Done'})
                                return JSONResponse(content=response_data,status_code=200)
                            else:
                                response_data = jsonable_encoder({'Result':'Done'})
                                return JSONResponse(content=response_data,status_code=200)
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
    
@router.get('/termination_id/{ids}')
async def home(request:Request,ids:int,db:Session=Depends(get_db)):
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
                            termination_data_id = db.query(models.Termination).filter(models.Termination.id==ids).filter(models.Termination.status=='ACTIVE').first()
                            response_data = jsonable_encoder({'Result':termination_data_id})
                            return JSONResponse(content=response_data,status_code=200)
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
     
@router.post('/termination_update')
async def home(request:Request,db:Session=Depends(get_db),edit_idz:int=Form(...),editemployee_id:str=Form(...),editterm_type:str=Form(...),editterm_date:str=Form(...),editterm_res:str=Form(...),editnotice_date:str=Form(...)):
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
                            check_data = db.query(models.Termination).filter(models.Termination.id!=edit_idz,models.Termination.Employee_id==editemployee_id).filter(models.Termination.status=='ACTIVE').all()
                            if not check_data:
                                db.query(models.Termination).filter(models.Termination.id==edit_idz).update({'Employee_id':editemployee_id,'Termination_Type_id':editterm_type,'Date':editterm_date,'Reason':editterm_res,'Notice_Date':editnotice_date})
                                db.commit()
                                response_data = jsonable_encoder({'Result':'Done'})
                                return JSONResponse(content=response_data,status_code=200)
                            else:
                                response_data = jsonable_encoder({'Result':'Done'})
                                return JSONResponse(content=response_data,status_code=200)
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
  
@router.get('/del_termination/{ids}')
async def home(request:Request,ids:int,db:Session=Depends(get_db)):
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
                           db.query(models.Termination).filter(models.Termination.id==ids).update({'status':'INACTIVE'})
                           db.commit()
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
    