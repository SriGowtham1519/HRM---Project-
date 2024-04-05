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

#                                                       ***** C L I E N T   P A G E *****

#=========================================================================================>>>> Profile Visible Page  

@router.get("/emplyee_profile/{ids}")
async def getting(request:Request,ids:int,db:Session=Depends(get_db)):
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
                            employee_data = db.query(models.Employee).filter(models.Employee.id == ids).filter(models.Employee.status=='ACTIVE').first()
                            personal = db.query(models.Employee_Personal_Info).filter(models.Employee_Personal_Info.Employee_ID==ids).filter(models.Employee_Personal_Info.status=='ACTIVE').first()
                            emergency_data = db.query(models.Emergency_Contact).filter(models.Emergency_Contact.Employee_ID==ids).filter(models.Emergency_Contact.status=='ACTIVE').first()
                            return templates.TemplateResponse("Admin/Employees/Employee/profile.html",context={"request":request,'emp_data':emp_data,"employee_data":employee_data,"personal":personal,"emergency_data":emergency_data})
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('Error',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})
    
#=========================================================================================>>>> Personal Informations 
    
@router.post("/emplpoyee_personalinfo")
async def add(request:Request,db:Session=Depends(get_db),employee_id:int=Form(...),pass_no:str=Form(...),pass_expiry:str=Form(...),tele:str=Form(...),national:str=Form(...),religin:str=Form(...),marry:str=Form(...),spous:str=Form(...),child:str=Form(...)):
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
                            check_data = db.query(models.Employee_Personal_Info).filter(models.Employee_Personal_Info.Employee_ID == str(employee_id)).filter(models.Employee_Personal_Info.status=='ACTIVE').first()
                            if check_data is None:
                                employee = models.Employee_Personal_Info(Passport_No=pass_no,Passport_Exp_Date=pass_expiry,Tel=tele,Nationality=national,Religion=religin,Marital_status=marry,spouse=spous,No_children=child,status='ACTIVE',created_by=loginer_id)
                                db.add(employee)
                                db.commit()
                                db.refresh(employee)
                            else:
                                db.query(models.Employee_Personal_Info).filter(models.Employee_Personal_Info.Employee_ID==employee_id).update({"Passport_No":pass_no,"Passport_Exp_Date":pass_expiry,"Tel":tele,"Nationality":national,"Religion":religin,"Marital_status":marry,"spouse":spous,"No_children":child})
                                db.commit()
                            return RedirectResponse(f'/HrmTool/Employee/emplyee_profile/{employee_id}',status_code=302)
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
    
#=========================================================================================>>>> Emergency Contact 

@router.get('/get_employee_emergency/{emp_id}')
async def get_employee_emergency(request:Request,emp_id:int,db:Session=Depends(get_db)):
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
                            employee_data = db.query(models.Employee).filter(models.Employee.id == emp_id).filter(models.Employee.status=='ACTIVE').first()
                            if employee_data:
                                emergency_data = db.query(models.Emergency_Contact).filter(models.Emergency_Contact.Employee_ID==str(emp_id)).filter(models.Emergency_Contact.status=='ACTIVE').first()
                                if emergency_data:
                                    return emergency_data
                                else:
                                    return JSONResponse({'None':None},status_code=200)
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
    
@router.post("/emplpoyee_emergeny_contact")
async def add(request:Request,db:Session=Depends(get_db),employee_id:int=Form(...),p_name:str=Form(...),p_relation:str=Form(...),p_phone:str=Form(...),p_phone_2:str=Form(...),s_name:str=Form(...),s_relation:str=Form(...),s_phone:str=Form(...),s_phone_2:str=Form(...)):
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
                            check_emergency_data = db.query(models.Emergency_Contact).filter(models.Emergency_Contact.Employee_ID == str(employee_id)).filter(models.Emergency_Contact.status=='ACTIVE').first()
                            if check_emergency_data:
                                db.query(models.Emergency_Contact).filter(models.Emergency_Contact.Employee_ID==str(employee_id)).update({'Primary_Name':p_name,'Primary_Relationship':p_relation,'Primary_Phone':p_phone,'Primary_Phone_II':p_phone_2,'Secondary_Name':s_name,'Secondary_Relationship':s_relation,'Secondary_Phone':s_phone,'Secondary_Phone_II':s_phone_2})
                                db.commit()
                                return RedirectResponse(f'/HrmTool/Employee/emplyee_profile/{employee_id}',status_code=302)
                            else:
                                add_data = models.Emergency_Contact(Employee_ID=employee_id,Primary_Name=p_name,Primary_Relationship=p_relation,Primary_Phone=p_phone,Primary_Phone_II=p_phone_2,Secondary_Name=s_name,Secondary_Relationship=s_relation,Secondary_Phone=s_phone,Secondary_Phone_II=s_phone_2,status='ACTIVE',created_by=loginer_id)
                                db.add(add_data)
                                db.commit()
                                db.refresh(add_data)
                                return RedirectResponse(f'/HrmTool/Employee/emplyee_profile/{employee_id}',status_code=302)
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
    
#=========================================================================================>>>> Education Information 

@router.get('/get_education_info/{emp_id}')
async def get_education_info(request:Request,emp_id:int,db:Session=Depends(get_db)):
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
                            check_education_info = db.query(models.Education_Informations).filter(models.Education_Informations.Employee_ID==emp_id).filter(models.Education_Informations.status=='ACTIVE').all()
                            #======================= returning a data based on the value have in a database or not =======================#
                            if check_education_info:
                                return check_education_info
                                return JSONResponse(content={'check_education_info':check_education_info},status_code=200)
                            else:
                                return JSONResponse(content={'None':None},status_code=200)
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except Exception as e:
                    ic(e)
                    return RedirectResponse('/Error',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})
    
@router.post("/emplpoyee_education_info")
async def add(request:Request,db:Session=Depends(get_db),employee_id:int=Form(...),instute:List[str]=Form(...),sub:List[str]=Form(...),s_date:List[str]=Form(...),e_date:List[str]=Form(...),deg:List[str]=Form(...),mark:List[str]=Form(...),card_id:List[str]=Form(None)):
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
                        check_education_data = db.query(models.Education_Informations).filter(models.Education_Informations.Employee_ID == employee_id).filter(models.Education_Informations.status=='ACTIVE').first()
                        #==================  Add  first time in database ====================#
                        if not check_education_data:
                            for inst,sub,start,end,degree,marks in zip(instute,sub,s_date,e_date,deg,mark):
                                add_education_info = models.Education_Informations(Employee_ID=employee_id,Institution=inst,Subject=sub,Starting_Date=start,Complete_Date=end,Degree=degree,Grade=marks,status='ACTIVE',created_by=loginer_id)
                                db.add(add_education_info)
                                db.commit()
                                db.refresh(add_education_info)
                            return RedirectResponse(f'/HrmTool/Employee/emplyee_profile/{employee_id}',status_code=302)
                        #================= Editing Portion for the Existing Data =============#
                        else:
                            employee_exit_data = db.query(models.Education_Informations).filter(models.Education_Informations.Employee_ID==str(employee_id)).filter(models.Education_Informations.status=='ACTIVE').all()
                            
                            calculate_exit_len = len(employee_exit_data)
                            calculate_arrival_len = len(instute)
                            
                            ic(calculate_exit_len)
                            ic(calculate_arrival_len)

                            ic(instute[:calculate_exit_len:])
                            ic(instute[calculate_exit_len::])

                            if  calculate_exit_len>=calculate_arrival_len:
                                #========>>>> here edit a old data only 
                                for edit_inst,edit_sub,edit_start,edit_end,edit_degree,edit_marks,edit_id in zip(instute[:calculate_exit_len:],sub[:calculate_exit_len:],s_date[:calculate_exit_len:],e_date[:calculate_exit_len:],deg[:calculate_exit_len:],mark[:calculate_exit_len:],card_id):
                                    db.query(models.Education_Informations).filter(models.Education_Informations.id==edit_id).update({'Institution':edit_inst,'Subject':edit_sub,'Starting_Date':edit_start,'Complete_Date':edit_end,'Degree':edit_degree,'Grade':edit_marks})
                                    db.commit()
                                return RedirectResponse(f'/HrmTool/Employee/emplyee_profile/{employee_id}',status_code=302)
                            else:
                                #=======>>> here edit old data and new data also
                                for edit_inst,edit_sub,edit_start,edit_end,edit_degree,edit_marks,edit_id in zip(instute[:calculate_exit_len:],sub[:calculate_exit_len:],s_date[:calculate_exit_len:],e_date[:calculate_exit_len:],deg[:calculate_exit_len:],mark[:calculate_exit_len:],card_id):
                                    db.query(models.Education_Informations).filter(models.Education_Informations.id==edit_id).update({'Institution':edit_inst,'Subject':edit_sub,'Starting_Date':edit_start,'Complete_Date':edit_end,'Degree':edit_degree,'Grade':edit_marks})
                                    db.commit()
                                print("1")
                                #======>>> Adding a new data 
                                for new_inst,new_sub,new_start,new_end,new_degree,new_marks in zip(instute[calculate_exit_len::],sub[calculate_exit_len::],s_date[calculate_exit_len::],e_date[calculate_exit_len::],deg[calculate_exit_len::],mark[calculate_exit_len::]):
                                    new_data = models.Education_Informations(Institution=new_inst,Subject=new_sub,Starting_Date=new_start,Complete_Date=new_end,Degree=new_degree,Grade=new_marks,status="ACTIVE",created_by=loginer_id)
                                    db.commit()
                                    db.refresh(new_data)
                                print("2")
                                return RedirectResponse(f'/HrmTool/Employee/emplyee_profile/{employee_id}',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                else:
                    return RedirectResponse('/HrmTool/login/login',status_code=302)
                # except:
                #     return RedirectResponse('/Error',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    # except JWTError:
    #         return RedirectResponse('/HrmTool/login/login',status_code=302)
    # except Exception as e:
    #     return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})
