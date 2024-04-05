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
from pathlib import Path

router = APIRouter()

templates = Jinja2Templates(directory="templates")

current_datetime = datetime.today()

#                                                       ***** B U D G E T   E X P E N S E S *****


#cGet The Template
@router.get('/budget-revenues') 
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
                            budget_data = db.query(models.Budget_Revenues).filter(models.Budget_Revenues.status=='ACTIVE').all()
                            category_data = db.query(models.Categories).filter(models.Categories.status=='ACTIVE').all()
                            sub_category_data = db.query(models.Sub_Category).filter(models.Sub_Category.status=='ACTIVE').all()
                            return templates.TemplateResponse("Admin/HR/Accounting/budget-revenues.html",context={"request":request,'emp_data':emp_data,'budget_data':budget_data,'category_data':category_data,'sub_category_data':sub_category_data})
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

@router.get('/select_subcategory_rev/{ids}') 
def get_form(ids:int,request:Request,db:Session = Depends(get_db)):
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
                            selective_subcategory = db.query(models.Sub_Category).filter(models.Sub_Category.Category_id==ids).filter(models.Sub_Category.status=='ACTIVE').all()
                            response_data = jsonable_encoder({'Result':selective_subcategory})
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
    
@router.post("/budget_revenues")
def submit_expenses(request: Request, db: Session = Depends(get_db),
                    amount: str = Form(...), currency_symbol: str = Form(...), notes: str = Form(...),
                    revenue_Date: str = Form(...), main_category: str = Form(...), sub_cat_id: str = Form(...),
                    Files: UploadFile = File(...)):
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

                            unique_file_name = str(uuid.uuid4())+'.pdf'

                            with open (f'./templates/assets/uploaded_files/{unique_file_name}','wb+') as Budget_file:
                                shutil.copyfileobj(Files.file,Budget_file)


                            body = models.Budget_Revenues(
                                Amount=amount,
                                Currency=currency_symbol,
                                Notes=notes,
                                Revenue_Date=revenue_Date,
                                Category_id=main_category,
                                Sub_Category_id=sub_cat_id,
                                File=unique_file_name,
                                status='ACTIVE',
                                created_by=loginer_id)
                            
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
    
@router.get("/selective_budget_revenues_id/{ids}")       
def selective_budget_expense_id(ids:int,request:Request,db: Session = Depends(get_db)):
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
                            single_data = db.query(models.Budget_Revenues).filter(models.Budget_Revenues.id==ids).filter(models.Budget_Revenues.status=='ACTIVE').first()
                            sub_data = db.query(models.Sub_Category).filter(models.Sub_Category.Category_id==single_data.Category_id).filter(models.Sub_Category.status=='ACTIVE').all()
                            response_data = jsonable_encoder({'Result':single_data,'sub_data':sub_data})
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

@router.post('/budget_revenue_update')
def create_data(request: Request, db: Session = Depends(get_db),  edit_id: str= Form(...),edit_amount: str =Form(...), edit_currency_symbol: str = Form(...),edit_notes: str = Form(...) , edit_expense_date: str = Form(...), edit_main_categ: str = Form(...), editsub_cat_id: str = Form(...),File:UploadFile=File(None)):
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

                            if File!=None:
                                unique_file_name = str(uuid.uuid4())+'.pdf'
                                with open (f'./templates/assets/uploaded_files/{unique_file_name}','wb+') as Budget_file:
                                    shutil.copyfileobj(File.file,Budget_file)
                                    db.query(models.Budget_Revenues).filter(models.Budget_Revenues.id==edit_id).update({'File':unique_file_name})
                                    db.commit()

                            db.query(models.Budget_Revenues).filter(models.Budget_Revenues.id==edit_id).update({"Amount": edit_amount, "Currency": edit_currency_symbol, "Notes": edit_notes, "Revenue_Date": edit_expense_date, "Category_id": edit_main_categ, "Sub_Category_id": editsub_cat_id })
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
    
#delete
@router.get("/budget_revenues_delete/{ids}")
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
                            item = db.query(models.Budget_Revenues).filter(models.Budget_Revenues.id==ids).filter(models.Budget_Revenues.status=='ACTIVE').first()
                            db.query(models.Budget_Revenues).filter(models.Budget_Revenues.id == ids).update({"status":"INACTIVE"})
                            db.commit()
                            file_path = Path(f'./templates/assets/uploaded_files/{item.File}')
                            if os.path.exists(file_path):
                                os.remove(file_path)
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
    
