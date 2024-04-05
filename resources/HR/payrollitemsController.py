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

#===================================================================================#
#================================= PayRoll Addition ================================#
#===================================================================================#
 
@router.get('/payroll-items') 
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
                            a = db.query(models.Payroll_Items_Addition).filter(models.Payroll_Items_Addition.status=='ACTIVE').all()
                            b = db.query(models.Payroll_Items_Overtime).filter(models.Payroll_Items_Overtime.status=='ACTIVE').all()
                            c = db.query(models.Payroll_Items_Deducation).filter(models.Payroll_Items_Deducation.status=='ACTIVE').all()
                            employee_data = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                            return templates.TemplateResponse("Admin/HR/Payroll/payroll-items.html",context={"request":request,'emp_data':emp_data,'a':a,'b':b,'c':c,'employee_data':employee_data})
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

@router.post("/add_addition")
def add_addition(request: Request, db: Session = Depends(get_db),Name: str=Form(...), Category: str = Form(...),unit_amount: str = Form(...) , emp_id: str = Form(...), assigne_to: str= Form(...), unit_calcu: str=Form()):
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
                            body = models.Payroll_Items_Addition(Name=Name,Category=Category,Unit_calculation=unit_calcu,Unit_Amount=unit_amount,Assignee_radio=assigne_to,Employee_id=emp_id,status='ACTIVE',created_by=loginer_id)
                            db.add(body)
                            db.commit()
                            db.refresh(body)
                            response_data = jsonable_encoder({'Result':'Done'})
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

@router.get("/taking_edit_id_addition/{ids}")       
def taking_edit_id_addition(ids:int,request:Request,db: Session = Depends(get_db)):
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
                            single_data = db.query(models.Payroll_Items_Addition).filter(models.Payroll_Items_Addition.id==ids).filter(models.Payroll_Items_Addition.status=='ACTIVE').first()
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

@router.post("/edit_addition")
def create_data(request: Request, db: Session = Depends(get_db),edit_addition_id:str= Form(...),  edit_name: str = Form(...), edit_category: str = Form(...), edit_unit_Amount: str = Form(...), edit_Aemp_id: str = Form(...), edit_assigne_to: str=Form(...), edit_unit_calcu: str=Form(...)):
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
                            db.query(models.Payroll_Items_Addition).filter(models.Payroll_Items_Addition.id==int(edit_addition_id)).update({'Name':edit_name,'Category':edit_category,'Unit_calculation':edit_unit_calcu,'Unit_Amount':edit_unit_Amount,'Assignee_radio':edit_assigne_to,'Employee_id':edit_Aemp_id})
                            db.commit()
                            response_data = jsonable_encoder({'Result':'Done'})
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
    
@router.get("/taking_dlt_id_addition/{ids}")
def taking_dlt_id_addition(request: Request,ids:int,db: Session = Depends(get_db)):
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
                            a = db.query(models.Payroll_Items_Addition).filter(models.Payroll_Items_Addition.status=='ACTIVE').all()
                            b = db.query(models.Payroll_Items_Overtime).filter(models.Payroll_Items_Overtime.status=='ACTIVE').all()
                            c = db.query(models.Payroll_Items_Deducation).filter(models.Payroll_Items_Deducation.status=='ACTIVE').all()
                            db.query(models.Payroll_Items_Addition).filter(models.Payroll_Items_Addition.id == ids).delete()
                            db.commit()
                            return templates.TemplateResponse("payroll-items.html",context={"request":request,'c':c,'a':a,'b':b})
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
    
#===================================================================================#
#================================= PayRoll overtime ================================#
#===================================================================================#
  
@router.post("/add_overtime")
async def add_addition(request: Request, db: Session = Depends(get_db),overtime_name: str=Form(...), overtime_rate_type: str = Form(...),overtime_rate: str = Form(...)):
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
                            check_exit_data = db.query(models.Payroll_Items_Overtime).filter(models.Payroll_Items_Overtime.Name==overtime_name,models.Payroll_Items_Overtime.Rate_type_id==overtime_rate_type,models.Payroll_Items_Overtime.Rate==overtime_rate).filter(models.Payroll_Items_Overtime.status=='ACTIVE').all()
                            if not check_exit_data:
                                body = models.Payroll_Items_Overtime(Name=overtime_name,Rate_type_id= overtime_rate_type,Rate=overtime_rate,status="ACTIVE",created_by=loginer_id)
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
     
@router.get("/taking_edit_id_overtime/{ids}")       
async def taking_edit_id_overtime(ids:int,request:Request,db: Session = Depends(get_db)):
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
                            single_data = db.query(models.Payroll_Items_Overtime).filter(models.Payroll_Items_Overtime.id==ids).filter(models.Payroll_Items_Overtime.status=='ACTIVE').first()
                            reponse_data = jsonable_encoder({'Result':single_data})
                            return JSONResponse(content=reponse_data,status_code=200)
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
     
@router.post("/edit_overtime")
async def edit(request: Request, db: Session = Depends(get_db),edit_id_ovr:str= Form(...),  edit_ovr_name: str = Form(...), edit_ovr_rate_id: str = Form(...), edit_ovr_rate: str = Form(...)):
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
                            check_exit_data = db.query(models.Payroll_Items_Overtime).filter(models.Payroll_Items_Overtime.id!=edit_id_ovr,models.Payroll_Items_Overtime.Name==edit_ovr_name,models.Payroll_Items_Overtime.Rate_type_id==edit_ovr_rate_id,models.Payroll_Items_Overtime.Rate==edit_ovr_rate).filter(models.Payroll_Items_Overtime.status=='ACTIVE').all()
                            if not check_exit_data:
                                db.query(models.Payroll_Items_Overtime).filter(models.Payroll_Items_Overtime.id==edit_id_ovr).update({"Name": edit_ovr_name, "Rate_type_id": edit_ovr_rate_id, "Rate": edit_ovr_rate})
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
     
@router.get("/taking_dlt_id_overtime/{ids}")
def taking_dlt_id_overtime(request: Request,ids:int,db: Session = Depends(get_db)):
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
                            db.query(models.Payroll_Items_Overtime).filter(models.Payroll_Items_Overtime.id == ids).delete()
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
    
#=====================================================================================#
#================================= PayRoll Deductions ================================#
#=====================================================================================#
    
@router.post("/add_deduction")
def add_addition(request: Request, db: Session = Depends(get_db),ded_name: str=Form(...), unit_amount_deduction: str = Form(...), ded_emp_id: str = Form(...), assigne_to: str=Form(...), unit_calcu:str=Form(...)):
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
                            body = models.Payroll_Items_Deducation(Name=ded_name,Unit_calculation= unit_calcu, Unit_Amount=unit_amount_deduction, Assignee_radio= assigne_to, Assignee_drop=ded_emp_id, status="ACTIVE",created_by=loginer_id)
                            db.add(body)
                            db.commit()
                            db.refresh(body)
                            response_data = jsonable_encoder({'Result':'Done'})
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
  
@router.get("/taking_edit_id_deduction/{ids}")       
def taking_edit_id_deduction(ids:int,request:Request,db: Session = Depends(get_db)):
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
                            single_data = db.query(models.Payroll_Items_Deducation).filter(models.Payroll_Items_Deducation.id==ids).filter(models.Payroll_Items_Deducation.status=='ACTIVE').first()
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
   
@router.post("/edit_deduction")
def edit(request: Request, db: Session = Depends(get_db),edit_id_deduction:int= Form(...),  edit_deduction_name: str = Form(...), edit_deduction_unit_Amount: str = Form(...), edit_deduction_dropdwn: str = Form(...), edit_assigne_to: str = Form(), edit_unit_calcu: str = Form()):
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
                            db.query(models.Payroll_Items_Deducation).filter(models.Payroll_Items_Deducation.id==edit_id_deduction).update({"Name": edit_deduction_name, "Unit_calculation": edit_unit_calcu, "Unit_Amount": edit_deduction_unit_Amount, "Assignee_radio": edit_assigne_to, "Assignee_drop": edit_deduction_dropdwn})
                            db.commit()
                            response_data = jsonable_encoder({'Result':'Done'})
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

@router.get("/taking_dlt_id_deduction/{ids}")
def taking_dlt_id_overtime(request: Request,ids:int,db: Session = Depends(get_db)):
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
                            a = db.query(models.Payroll_Items_Addition).filter(models.Payroll_Items_Addition.status=='ACTIVE').all()
                            b = db.query(models.Payroll_Items_Overtime).filter(models.Payroll_Items_Overtime.status=='ACTIVE').all()
                            c = db.query(models.Payroll_Items_Deducation).filter(models.Payroll_Items_Deducation.status=='ACTIVE').all()
                            db.query(models.Payroll_Items_Deducation).filter(models.Payroll_Items_Deducation.id == ids).update({"status":"INACTIVE"})
                            db.commit()
                            return templates.TemplateResponse("payroll-items.html",context={"request":request,'c':c,'a':a,'b':b})
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

#=====================================================================================#
#======================================= Pay Slip ====================================#
#=====================================================================================#
    
@router.get('/Payslip_model') 
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
                            invoice_data = db.query(models.Invoice_Settings).filter(models.Invoice_Settings.status=='ACTIVE').first()
                            company_data = db.query(models.Company_Settings).filter(models.Company_Settings.status=='ACTIVE').first()

                            current_month = datetime.today().strftime('%b')
                            current_year  = datetime.today().year
                            return templates.TemplateResponse("Admin/HR/Payroll/salary-view.html",context={"request":request,'emp_data':emp_data,'invoice_data':invoice_data,'company_data':company_data,'current_month':current_month,'current_year':current_year})
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


