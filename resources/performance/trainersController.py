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
from icecream import ic

router = APIRouter()

templates = Jinja2Templates(directory="templates")

current_datetime = datetime.today()

#========================================================================================#
#=======================================  Trainers ======================================#
#========================================================================================#
#cGet The Template
@router.get('/add_trainers') 
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
                            trainers_data = db.query(models.Trainers).filter(models.Trainers.status=='ACTIVE').all()
                            return templates.TemplateResponse("Admin/Performance/Trainings/trainers.html",context={"request":request,'emp_data':emp_data,'trainers_data':trainers_data})
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
    
@router.post('/add_trainers')
def create_data(request: Request, db: Session = Depends(get_db),fname: str =Form(...), lname: str = Form(...),rol: str = Form(...) , mail: str = Form(...), ph: str = Form(...),des: str = Form(...),client_photo:UploadFile=File(...)):
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

                            file_location = f"./templates/assets/uploaded_files/{client_photo.filename}"
                            with open(file_location, 'wb+') as file_object:
                                shutil.copyfileobj(client_photo.file,file_object)
                            
                            data_check = db.query(models.Trainers).filter(models.Trainers.Email==mail,models.Trainers.Phone ==ph).filter(models.Trainers.status=='ACTIVE').all()
                            if not data_check:
                                body = models.Trainers(First_Name=fname,Last_Name =lname,Role_id=rol,Email=mail,Phone =ph,Current_status="Pending",Description=des,Photo=client_photo.filename,status="ACTIVE",created_by="admin")
                                db.add(body)
                                db.commit()
                                response_data = jsonable_encoder({'Result':'Done'})
                                return JSONResponse(content=response_data,status_code=200)
                            else :
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
    
# edit
@router.get("/eidt_trainers/{ids}")       
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
                            single_data = db.query(models.Trainers).filter(models.Trainers.id==ids).filter(models.Trainers.status=='ACTIVE').first()
                            return single_data
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
    
@router.post('/trainers_update')
def create_data(request: Request, db: Session = Depends(get_db),edit_idz:int=Form(...),edit_fname:str=Form(...),edit_lname:str=Form(...),edit_rol:str=Form(...),edit_mail:str=Form(...),edit_ph:str=Form(...),edit_des:str=Form(...),edit_client_photo:UploadFile=File(None)):
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

                            check_exit_data_1 = db.query(models.Trainers).filter(models.Trainers.id!=edit_idz).filter(models.Trainers.Email==edit_mail).filter(models.Trainers.status=='ACTIVE').all()
                            if not check_exit_data_1:
                                if  str(edit_client_photo)!='None':
                                    unique_photo_name = str(uuid.uuid4())+'.png'
                                    with open(f'./templates/assets/uploaded_files/{unique_photo_name}' ,'wb+') as New_file_object:
                                        shutil.copyfileobj(edit_client_photo.file,New_file_object)
                                        db.query(models.Trainers).filter(models.Trainers.id==edit_idz).update({'Photo':unique_photo_name})
                                        db.commit()

                                db.query(models.Trainers).filter(models.Trainers.id==edit_idz).update({'First_Name':edit_fname,'Last_Name':edit_lname,'Role_id':edit_rol,'Email':edit_mail,'Phone':edit_ph,'Description':edit_des})
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
    
# # delete
@router.get("/delete_trainers/{ids}")
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
                            a = db.query(models.Trainers).filter(models.Trainers.status=='ACTIVE').all()
                            db.query(models.Trainers).filter(models.Trainers.id == ids).update({"status":"INACTIVE","Current_status":"Inactive"})
                            db.commit()
                            return templates.TemplateResponse("trainers.html",context={"request":request})
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
    
@router.get("/current_trainer/{data}/{ids}")
async def taking_dlt_id(ids:int,data:str,request: Request,db: Session = Depends(get_db)):
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
                            print('here')
                            db.query(models.Trainers).filter(models.Trainers.id==ids).update({'Current_status':data})
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
    
@router.get("/change_status_trainer/{ids}/{info}")       
def taking_edit_id(ids:int,info:str,request:Request,db: Session = Depends(get_db)):
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
                            db.query(models.Trainers).filter(models.Trainers.id==ids).update({'Current_status':info})
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
    
#========================================================================================#
#==================================  Training Type ======================================#
#========================================================================================#
    
@router.get('/training_type') 
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
                            training_type_data = db.query(models.Training_Type).filter(models.Training_Type.status=='ACTIVE').all()
                            return templates.TemplateResponse("Admin/Performance/Trainings/training-type.html",context={"request":request,'emp_data':emp_data,'training_type_data':training_type_data})
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
    
@router.post('/training_type') 
def get_form(request:Request,db:Session = Depends(get_db),types:str=Form(...),desc:str=Form(...),c_status:str=Form(...)):
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
                            check_type_data = db.query(models.Training_Type).filter(models.Training_Type.Name==types.lower()).filter(models.Training_Type.status=='ACTIVE').all()
                            if not check_type_data:
                                new_type = models.Training_Type(Name=types,Description=desc,Current_status=c_status,status='ACTIVE',created_by=loginer_id)
                                db.add(new_type)
                                db.commit()
                                db.refresh(new_type)
                                response_data = jsonable_encoder({"Result":'Done'})
                                return JSONResponse(content=response_data,status_code=200)
                            else:
                                response_data = jsonable_encoder({"Result":'Error'})
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
  
@router.get('/update_current_status/{ids}/{info}') 
def get_form(request:Request,ids:int,info:str,db:Session = Depends(get_db)):
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
                            db.query(models.Training_Type).filter(models.Training_Type.id==ids).update({"Current_status":info})
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
     
@router.get('/taking_traning_type_id/{ids}') 
def get_form(request:Request,ids:int,db:Session = Depends(get_db)):
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
                            type_data = db.query(models.Training_Type).filter(models.Training_Type.id==ids).filter(models.Training_Type.status=='ACTIVE').first()
                            response_data = jsonable_encoder({'Result':type_data})
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
      
@router.post('/training_type_update') 
def get_form(request:Request,db:Session = Depends(get_db),edit_idz:int=Form(...),edit_name:str=Form(...),edit_desc:str=Form(...),edit_c_status:str=Form(...)):
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
                            check_type_data = db.query(models.Training_Type).filter(models.Training_Type.id!=edit_idz,models.Training_Type.Name==edit_name.lower()).filter(models.Training_Type.status=='ACTIVE').all()
                            if not check_type_data:
                                db.query(models.Training_Type).filter(models.Training_Type.id==edit_idz).update({'Name':edit_name,'Description':edit_desc,'Current_status':edit_c_status})
                                db.commit()
                                response_data = jsonable_encoder({"Result":'Done'})
                                return JSONResponse(content=response_data,status_code=200)
                            else:
                                response_data = jsonable_encoder({"Result":'Error'})
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
    
@router.get('/del_training_type/{ids}') 
def get_form(request:Request,ids:int,db:Session = Depends(get_db)):
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
                            db.query(models.Training_Type).filter(models.Training_Type.id==ids).update({'status':'INACTIVE'})
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
       
#========================================================================================#
#==================================  Training List  =====================================#
#========================================================================================#
    
@router.get('/training_list') 
def get_form(request:Request,db:Session = Depends(get_db)):
    # try:
        if 'loginer_details' in request.session:
            token = request.session['loginer_details']
            try:
                payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
                loginer_id : int= payload.get("empid") 
                # try:
                if loginer_id:
                    emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
                    if emp_data.Lock_screen == 'OFF':
                        training_type_data = db.query(models.Training_Type).filter(models.Training_Type.status=='ACTIVE').all()
                        employee_data = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                        trainers_data = db.query(models.Trainers).filter(models.Trainers.status=='ACTIVE').all()
                        training_data = db.query(models.Training).filter(models.Training.status=='ACTIVE').all()
                        training_followers_data = db.query(models.Training_Followers).filter(models.Training_Followers.status=='ACTIVE').all()
                        return templates.TemplateResponse("Admin/Performance/Trainings/training.html",context={"request":request,'emp_data':emp_data,'training_type_data':training_type_data,'employee_data':employee_data,'trainers_data':trainers_data,'training_data':training_data,'training_followers_data':training_followers_data})
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
    # except JWTError:
    #         return RedirectResponse('/HrmTool/login/login',status_code=302)
    # except Exception as e:
    #     return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})
   
@router.post('/training_list') 
def get_form(request:Request,db:Session = Depends(get_db),t_type:str=Form(...),staff:str=Form(...),emps:List[str]=Form(...),cost:str=Form(...),s_date:str=Form(...),e_date:str=Form(...),desc:str=Form(...),c_status:str=Form(...)):
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

                            def emp_check():
                                try:
                                    for i in emps:
                                        if i!='':
                                            split_i = i.split(',')
                                            return split_i
                                        else:
                                            return 'Error'
                                except:
                                    return 'Error'
                                
                            if(emp_check()!='Error' or emp_check()==None):
                                check_exit_data = db.query(models.Training).filter(models.Training.Training_Type_id==t_type,models.Training.Trainer_id==staff).filter(models.Training.status=='ACTIVE').all()
                                if not check_exit_data:
                                    new_training = models.Training(Training_Type_id=t_type,Trainer_id=staff,Training_Cost=cost,Start_Date=s_date,End_Date=e_date,Description=desc,Current_status=c_status,status='ACTIVE',created_by=loginer_id)
                                    db.add(new_training)
                                    db.commit()
                                    db.refresh(new_training)

                                    list_Employee = emp_check()

                                    for i in list_Employee:
                                        new_training_followers = models.Training_Followers(Training_id=new_training.id,Employees_id=i,status='ACTIVE',created_by=loginer_id)
                                        db.add(new_training_followers)
                                        db.commit()
                                        db.refresh(new_training_followers)

                                    response_data = jsonable_encoder({'Result':'Done'})
                                    return JSONResponse(content=response_data,status_code=200)
                                else:
                                    response_data = jsonable_encoder({'Result':'Error'})
                                    return JSONResponse(content=response_data,status_code=200)
                            else:
                                response_data = jsonable_encoder({'Result':'Emp'})
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
      
@router.get('/update_status_training/{ids}/{info}') 
def get_form(request:Request,ids:int,info:str,db:Session = Depends(get_db)):
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
                            db.query(models.Training).filter(models.Training.id==ids).update({'Current_status':info})
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
      
@router.get('/collect_training_data/{ids}') 
def get_form(request:Request,ids:int,db:Session = Depends(get_db)):
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
                            find_particular_data = db.query(models.Training).filter(models.Training.id==ids).filter(models.Training.status=='ACTIVE').first()
                            find_sub_data = db.query(models.Training_Followers).filter(models.Training_Followers.Training_id==str(ids)).filter(models.Training_Followers.status=='ACTIVE').all()
                            employee_data = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                            response_data = jsonable_encoder({'Training':find_particular_data,'Followers':find_sub_data,'Employee':employee_data})
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
   
@router.post('/training_list_update') 
def get_form(request:Request,db:Session = Depends(get_db),edit_idz:int=Form(...),e_t_type:str=Form(...),e_staff:str=Form(...),e_emps:List[str]=Form(...),e_cost:str=Form(...),e_s_date:str=Form(...),e_e_date:str=Form(...),e_desc:str=Form(...),e_c_status:str=Form(...)):
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

                            def emp_check():
                                try:
                                    for i in e_emps:
                                        if i!='':
                                            split_i = i.split(',')
                                            return split_i
                                        else:
                                            return 'Error'
                                except:
                                    return 'Error'
                                
                            if(emp_check()!='Error' or emp_check()==None):
                                check_exit_data = db.query(models.Training).filter(models.Training.id!=edit_idz, models.Training.Training_Type_id==e_t_type,models.Training.Trainer_id==e_staff).filter(models.Training.status=='ACTIVE').all()
                                if not check_exit_data:
                                    db.query(models.Training).filter(models.Training.id==edit_idz).update({'Training_Type_id':e_t_type,'Trainer_id':e_staff,'Training_Cost':e_cost,'Start_Date':e_s_date,'End_Date':e_e_date,'Description':e_desc,'Current_status':e_c_status})
                                    db.commit()
                                    list_Employee = emp_check()
                                    #making a old data in inactive and creating a new data records
                                    db.query(models.Training_Followers).filter(models.Training_Followers.Training_id==edit_idz).update({'status':'INACTIVE'})
                                    db.commit()

                                    for new in list_Employee:
                                        Alter_data = models.Training_Followers(Training_id=edit_idz,Employees_id=new,status='ACTIVE',created_by=loginer_id)
                                        db.add(Alter_data)
                                        db.commit()
                                        db.refresh(Alter_data)

                                    response_data = jsonable_encoder({'Result':'Done'})
                                    return JSONResponse(content=response_data,status_code=200)
                                else:
                                    response_data = jsonable_encoder({'Result':'Error'})
                                    return JSONResponse(content=response_data,status_code=200)
                            else:
                                response_data = jsonable_encoder({'Result':'Emp'})
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
      
@router.get('/del_training_data/{ids}') 
def get_form(request:Request,ids:int,db:Session = Depends(get_db)):
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
                            db.query(models.Training).filter(models.Training.id==ids).update({'status':'INACTIVE'})
                            db.commit()

                            db.query(models.Training_Followers).filter(models.Training_Followers.Training_id==ids).update({'status':'INACTIVE'})
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
   