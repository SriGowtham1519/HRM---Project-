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

#cGet The Template
@router.get('/employee_salary') 
def get_form(request:Request,db:Session = Depends(get_db)):
    try:
        if 'loginer_details' in request.session:
            token = request.session['loginer_details']
            try:
                payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
                loginer_id : int= payload.get("empid") 
                # try:
                if loginer_id:
                    emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
                    if emp_data.Lock_screen == 'OFF':
                        Emp_salary=db.query(models.Employee_Salary).filter(models.Employee_Salary.status=='ACTIVE').all()
                        employee_data = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                        return templates.TemplateResponse("Admin/HR/Payroll/salary.html",context={"request":request,'emp_data':emp_data,'Emp_salary':Emp_salary,'employee_data':employee_data})
                    else:
                        return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                else:
                    return RedirectResponse('/HrmTool/login/login',status_code=302)
                # except:
                #     return RedirectResponse('/HrmTool/login/login',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"}) 
    
@router.post("/create_data")
def create_data(
    request: Request,
    db: Session = Depends(get_db),
    Employee_ID: str = Form(...),
    Net_Salary: str = Form(...),
    Basic: str = Form(...),
    DA_40: str = Form(...),
    HRA_15: str = Form(...),
    Conveyance: str = Form(...),
    Allowance: str = Form(...),
    Medical_Allowance: str = Form(...),
    TDS: str = Form(...),
    ESI: str = Form(...),
    PF: str = Form(...),
    Leave: str = Form(...),
    Prof_Tax: str = Form(...),
    Labour_Welfare: str = Form(...),
):
    try:
        if 'loginer_details' in request.session:
            token = request.session['loginer_details']
            try:
                payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
                loginer_id : int= payload.get("empid") 
                # try:
                if loginer_id:
                    emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
                    if emp_data.Lock_screen == 'OFF':
                        check_exit_data = db.query(models.Employee_Salary).filter(models.Employee_Salary.Employee_id==Employee_ID).filter(models.Employee_Salary.status=='ACTIVE').all()
                        if not check_exit_data:
                            body = models.Employee_Salary(
                                Employee_id=Employee_ID,
                                Net_Salary=Net_Salary,
                                Basic=Basic,
                                TDS=TDS,
                                DA_40=DA_40,
                                ESI=ESI,
                                HRA_15=HRA_15,
                                PF=PF,
                                Conveyance=Conveyance,
                                Leave=Leave,
                                Allowance=Allowance,
                                Prof_Tax=Prof_Tax,
                                Medical_Allowance=Medical_Allowance,
                                Labour_Welfare=Labour_Welfare,
                                status="ACTIVE",
                                created_by=loginer_id,
                            )
                            db.add(body)
                            db.commit()
                            db.refresh(body)
                            response_data = jsonable_encoder({'Result':'Done'})
                            return JSONResponse(content=response_data,status_code=200)
                        else:
                            response_data = jsonable_encoder({'Result':'Error'})
                            return JSONResponse(content=response_data,status_code=200)
                    else:
                        return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                else:
                    return RedirectResponse('/HrmTool/login/login',status_code=302)
                # except:
                #     return RedirectResponse('/HrmTool/login/login',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"}) 
       
@router.get('/geting_form') 
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
                            employee_data = db.query(models.Employee).filter(models.Employee.status=='active').all()
                            Emp_salary=db.query(models.Employee_Salary).filter(models.Employee_Salary.status=='active').all()
                            return templates.TemplateResponse("payslip-reports.html",context={"request":request,'emp_data':emp_data,'employee_data':employee_data,'Emp_salary':Emp_salary})
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
    
@router.get('/gets_form') 
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
                            employee_data = db.query(models.Employee).filter(models.Employee.status=='active').all()
                            Emp_salary=db.query(models.Employee_Salary).filter(models.Employee_Salary.status=='active').all()
                            return templates.TemplateResponse("goal-tracking.html",context={"request":request,'emp_data':emp_data})
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
                  
@router.get("/employee_salary_id/{ids}")       
def taking_edit_id(ids:int,request:Request,db: Session = Depends(get_db)):
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
                            single_data = db.query(models.Employee_Salary).filter(models.Employee_Salary.id==ids).filter(models.Employee_Salary.status=='ACTIVE').first()
                            response_data = jsonable_encoder({'Result':single_data})
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
    
@router.post('/edit_data/')
def edit_data(
    request: Request,
    db: Session = Depends(get_db),
    edit_id: int = Form(...),
    edit_Employee_ID: str = Form(...),
    edit_Net_Salary: str = Form(...),
    edit_Basic: str = Form(...),
    edit_TDS: str = Form(...),
    edit_DA_40: str = Form(...),
    edit_ESI: str = Form(...),
    edit_PF: str = Form(...),
    edit_HRA_15: str = Form(...),
    edit_Conveyance: str = Form(...),
    edit_Leave: str = Form(...),
    edit_Allowance: str = Form(...),
    edit_Prof_Tax: str = Form(...),
    edit_Medical_Allowance: str = Form(...),
    edit_Labour_Welfare: str = Form(...),
):
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
                            check_exit_data = db.query(models.Employee_Salary).filter(models.Employee_Salary.id!=edit_id,models.Employee_Salary.Employee_id==edit_Employee_ID).filter(models.Employee_Salary.status=='ACTIVE').all()
                            if not check_exit_data:
                                db.query(models.Employee_Salary).filter(models.Employee_Salary.id == edit_id).update({
                                    
                                    "Employee_id": edit_Employee_ID,
                                    "Net_Salary": edit_Net_Salary,
                                    "Basic": edit_Basic,
                                    "TDS": edit_TDS,
                                    "DA_40": edit_DA_40,
                                    "ESI": edit_ESI,
                                    "PF": edit_PF,
                                    "HRA_15": edit_HRA_15,
                                    "Conveyance": edit_Conveyance,
                                    "Leave": edit_Leave,
                                    "Allowance": edit_Allowance,
                                    "Prof_Tax": edit_Prof_Tax,
                                    "Medical_Allowance": edit_Medical_Allowance,
                                    "Labour_Welfare": edit_Labour_Welfare,
                                })
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
                    return RedirectResponse('/HrmTool/login/login',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"}) 
    
@router.get("/employee_salary_delete/{ids}")
def taking_dlt_id(request: Request,ids:int,db: Session = Depends(get_db)):
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
                            db.query(models.Employee_Salary).filter(models.Employee_Salary.id == ids).update({"status":"INACTIVE"})
                            db.commit()
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
    
@router.get("/search_name/{data}")
def delete_project(request: Request,data:str,db: Session = Depends(get_db)):
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
                            search_data = db.query(models.Employee_Salary).from_statement(text(f'select * from Employee_Salary where employee_salary like "%{data}%" and status="ACTIVE" ')).first()
                            return search_data
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
    