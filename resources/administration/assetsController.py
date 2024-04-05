from typing import Dict, List,Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Depends, FastAPI, Request, Form ,status
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
from icecream import ic
from pathlib import Path

router = APIRouter()

templates = Jinja2Templates(directory="templates")

current_datetime = datetime.today()


#                                 *********** A S S E S T S ***********

@router.get('/assets') 
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
                            employee_data = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                            def asset_id_gen():
                                try:
                                    len_asset_data = len(db.query(models.Asset).filter(models.Asset.status=='ACTIVE').all())
                                    value_assets = "AST-"+str(len_asset_data+1)
                                    return value_assets
                                except:
                                    return "AST-1"

                            return templates.TemplateResponse("Admin/Administration/Assets/assets.html",context={"request":request,'emp_data':emp_data,'asset_data':asset_data,"asset_id_gen":asset_id_gen(),"employee_data":employee_data})
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
    
@router.post("/add_asset")
def create_data(request: Request, db: Session = Depends(get_db),Asset_Name:str=Form(...),Asset_Id: str = Form(...),Purchase_Date: str = Form(...),Purchase_From: str = Form(...),Model: str = Form(...),Serial_Number: str= Form(...),Supplier: str= Form(...),Warranty:str=Form(...),Warranty_endDate:str=Form(...),Value:str=Form(...),Manufacturer: str = Form(...),Asset_User_id:str=Form(...),desc:str=Form(...),Condition:str=Form(...),Current_status:str=Form(...),image_1:UploadFile=File(...),image_2:UploadFile=File(...),image_3:UploadFile=File(...),image_4:UploadFile=File(...)):#,
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

                            ic(image_1)
                            ic(Asset_Name)

                            check_serial_no = db.query(models.Asset).filter(models.Asset.Serial_Number == Serial_Number).filter(models.Asset.status=='ACTIVE').all()
                            if not check_serial_no:
                                #===============================>>> Image 1
                                unique_image_1 = str(uuid.uuid4())+'.png'
                                with open(f'./templates/assets/uploaded_files/{unique_image_1}','wb+') as File_object_1:
                                    shutil.copyfileobj(image_1.file,File_object_1)
                                #===============================>>> Image 2
                                unique_image_2 = str(uuid.uuid4())+'.png'
                                with open(f'./templates/assets/uploaded_files/{unique_image_2}','wb+') as File_object_2:
                                    shutil.copyfileobj(image_2.file,File_object_2)
                                #===============================>>> Image 3
                                unique_image_3 = str(uuid.uuid4())+'.png'
                                with open(f'./templates/assets/uploaded_files/{unique_image_3}','wb+') as File_object_3:
                                    shutil.copyfileobj(image_3.file,File_object_3)
                                #===============================>>> Image 4
                                unique_image_4 = str(uuid.uuid4())+'.png'
                                with open(f'./templates/assets/uploaded_files/{unique_image_4}','wb+') as File_object_4:
                                    shutil.copyfileobj(image_4.file,File_object_4)

                                body = models.Asset(Asset_Image_1=unique_image_1,Asset_Image_2=unique_image_2,Asset_Image_3=unique_image_3,Asset_Image_4=unique_image_4,Asset_Name=Asset_Name,Asset_Id=Asset_Id,Purchase_Date=Purchase_Date,Purchase_From=Purchase_From,Manufacturer=Manufacturer,Model=Model,Serial_Number=Serial_Number,Supplier=Supplier,Warranty_Months=Warranty,Warranty_end_Date=Warranty_endDate,Value=Value,Asset_User_id=Asset_User_id,Description=desc,Condition=Condition,Current_status=Current_status,status='ACTIVE',created_by=loginer_id)
                                db.add(body)
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
                            asset_data = db.query(models.Asset).filter(models.Asset.id==ids).filter(models.Asset.status=='ACTIVE').first()
                            List_Images = [asset_data.Asset_Image_1,asset_data.Asset_Image_2,asset_data.Asset_Image_3,asset_data.Asset_Image_4]
                            for item in List_Images:
                                file_path = Path(f'./templates/assets/uploaded_files/{item}')
                                if os.path.exists(file_path):
                                    os.remove(file_path)
                            db.query(models.Asset).filter(models.Asset.id == ids).update({"status":"INACTIVE"})
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
    
@router.get("/taking_edit_id/{ids}")       
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
                            single_data = db.query(models.Asset).filter(models.Asset.id==ids).filter(models.Asset.status=='ACTIVE').first()
                            return single_data
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
    
@router.post('/edit_asset')
def create_data(request: Request,db: Session = Depends(get_db),edit_idz:str=Form(...),edit_image_1:UploadFile=File(None),edit_image_2:UploadFile=File(None),edit_image_3:UploadFile=File(None),edit_image_4:UploadFile=File(None),edit_asset_name: str= Form(...),edit_assetid: str =Form(...),edit_pdate:str = Form(...),edit_pfrom: str = Form(...),edit_man: str = Form(...),edit_model: str = Form(...),edit_snum: str = Form(...),edit_sup: str = Form(...),edit_war: str = Form(...),edit_warEnd: str = Form(...),edit_val: str = Form(...),edit_assuser: str = Form(...),edit_desc: str = Form(...),edit_con:str=Form(...),edit_stat:str=Form(...)):
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
                            check_exit_data = db.query(models.Asset).filter(models.Asset.id != edit_idz,models.Asset.Serial_Number == edit_snum).filter(models.Asset.status=='ACTIVE').all()
                            if not check_exit_data:
                                #=========================================>>>> Image 1
                                if (edit_image_1 != None):
                                    unique_image_1 = str(uuid.uuid4())+'.png'
                                    with open(f'./templates/assets/uploaded_files/{unique_image_1}','wb+') as File_object_1:
                                        shutil.copyfileobj(edit_image_1.file,File_object_1)
                                        db.query(models.Asset).filter(models.Asset.id==int(edit_idz)).update({'Asset_Image_1':unique_image_1})
                                        db.commit()
                                 #=========================================>>>> Image 2
                                if (edit_image_2 != None):
                                    unique_image_2 = str(uuid.uuid4())+'.png'
                                    with open(f'./templates/assets/uploaded_files/{unique_image_2}','wb+') as File_object_2:
                                        shutil.copyfileobj(edit_image_2.file,File_object_2)
                                        db.query(models.Asset).filter(models.Asset.id==int(edit_idz)).update({'Asset_Image_2':unique_image_2})
                                        db.commit()
                                 #=========================================>>>> Image 3
                                if (edit_image_3 != None):
                                    unique_image_3 = str(uuid.uuid4())+'.png'
                                    with open(f'./templates/assets/uploaded_files/{unique_image_3}','wb+') as File_object_3:
                                        shutil.copyfileobj(edit_image_3.file,File_object_3)
                                        db.query(models.Asset).filter(models.Asset.id==int(edit_idz)).update({'Asset_Image_3':unique_image_3})
                                        db.commit()
                                 #=========================================>>>> Image 4
                                if (edit_image_4 != None):
                                    unique_image_4 = str(uuid.uuid4())+'.png'
                                    with open(f'./templates/assets/uploaded_files/{unique_image_4}','wb+') as File_object_4:
                                        shutil.copyfileobj(edit_image_4.file,File_object_4)
                                        db.query(models.Asset).filter(models.Asset.id==int(edit_idz)).update({'Asset_Image_4':unique_image_4})
                                        db.commit()

                                db.query(models.Asset).filter(models.Asset.id==int(edit_idz)).update({'Asset_Name':edit_asset_name,'Asset_Id':edit_assetid,'Purchase_Date':edit_pdate,'Purchase_From':edit_pfrom,'Manufacturer':edit_man,'Model':edit_model,'Serial_Number':edit_snum,'Supplier':edit_sup,'Warranty_Months':edit_war,'Warranty_end_Date':edit_warEnd,'Value':edit_val,'Asset_User_id':edit_assuser,'Description':edit_desc,'Condition':edit_con,'Current_status':edit_stat})
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
 
@router.get("/status_update/{ids}/{info}")
def taking_dlt_id_overtime(request: Request,ids:int,info:str,db: Session = Depends(get_db)):
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
                            db.query(models.Asset).filter(models.Asset.id==ids).update({'Current_status':info})
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
    
@router.get("/search_employee_assets/{name}")
def taking_dlt_id_overtime(request: Request,name:str,db: Session = Depends(get_db)):
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
                            def employee_table():
                                try:
                                    search_employee = db.query(models.Employee.id).from_statement(text(f'SELECT * FROM employee WHERE First_Name LIKE "%{name.lower()}%" OR Last_Name LIKE "%{name.lower()}%"')).all()
                                    list_employee_id = []
                                    for ids in search_employee:
                                        for id in ids:
                                            list_employee_id.append(id)
                                    return list_employee_id
                                except:
                                    pass
                            all_emp_table_id = employee_table()

                            active_employee_ids = []

                            for i in all_emp_table_id:
                                check_active_or_not = db.query(models.Employee).filter(models.Employee.id==int(i)).filter(models.Employee.status=='ACTIVE').first()
                                if check_active_or_not:
                                    active_employee_ids.append(i)

                            def assets_table(Employee_ids):
                                try:
                                    list_asset_data = []
                                    for ids in Employee_ids:
                                        asset_data = db.query(models.Asset).filter(models.Asset.Asset_User_id==int(ids)).filter(models.Asset.status=='ACTIVE').first()
                                        list_asset_data.append(asset_data)
                                    return list_asset_data
                                except:pass
                            employee_data = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                            response_data = jsonable_encoder({'Result':assets_table(active_employee_ids),"employee_data":employee_data})
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
   
@router.get("/search_status_data/{info}")
def taking_dlt_id_overtime(request: Request,info:str,db: Session = Depends(get_db)):
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
                           result_data = db.query(models.Asset).filter(models.Asset.Current_status==info).filter(models.Asset.status=='ACTIVE').all()
                           employee_data = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                           response_data = jsonable_encoder({'Result':result_data,'employee_data':employee_data})
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
  
@router.get("/search_dates_via/{from_date}/{to_date}")
def taking_dlt_id_overtime(request: Request,from_date:str,to_date:str,db: Session = Depends(get_db)):
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
                           filter_by_dates_data = db.query(models.Asset).from_statement(text(f'select * from asset where Purchase_Date >={from_date} and Warranty_end_Date <={to_date} and status="ACTIVE"')).all()
                           employee_data = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                           response_data = jsonable_encoder({'Result':filter_by_dates_data,'employee_data':employee_data})
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
  