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
from sqlalchemy import text,func,update

router = APIRouter()

templates = Jinja2Templates(directory="templates")

current_datetime = datetime.today()

#=========================================================================================#
#================================= Performance Indicator =================================#
#=========================================================================================#

@router.get("/performance_indicator")
async def getting(request:Request,db:Session=Depends(get_db)):
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
                            designation_data = db.query(models.Designation).filter(models.Designation.status=='ACTIVE').all()
                            department_data = db.query(models.Department).filter(models.Department.status=='ACTIVE').all()
                            employee_data = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                            indicator_data = db.query(models.Performance_Indicator).filter(models.Performance_Indicator.status=='ACTIVE').all()
                            return templates.TemplateResponse("Admin/Performance/Performances/performance-indicator.html",context={"request":request,'emp_data':emp_data,'designation_data':designation_data,'indicator_data':indicator_data,'department_data':department_data,'employee_data':employee_data})
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

@router.post("/performanc_indicator")
async def getting(request:Request,db:Session=Depends(get_db),desg:str=Form(...),c_exp:str=Form(...),mark:str=Form(...),t_manage:str=Form(...),admin:str=Form(...),skill:str=Form(...),work:str=Form(...),efficy:str=Form(...),integ:str=Form(...),profes:str=Form(...),team:str=Form(...),think:str=Form(...),manage:str=Form(...),attend:str=Form(...),deadline:str=Form(...),c_status:str=Form(...)):
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
                            check_exit_data = db.query(models.Performance_Indicator).filter(models.Performance_Indicator.Designation_id==desg).filter(models.Performance_Indicator.status=='ACTIVE').all()
                            if not check_exit_data:
                               newdata = models.Performance_Indicator(Designation_id=desg,Customer_Experience=c_exp,Marketing=mark,Management=t_manage,Administration=admin,Presentation_Skill=skill,Quality_Of_Work=work,Efficiency=efficy,Integrity=integ,Professionalism=profes,Team_Work=team,Critical_Thinking=think,Conflict_Management=manage,Attendance=attend,Meet_Deadline=deadline,Current_status=c_status,status='ACTIVE',created_by=loginer_id)
                               db.add(newdata)
                               db.commit()
                               db.refresh(newdata)
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
  
@router.get("/performance_indicator_status_update/{ids}/{info}")
async def getting(request:Request,ids:int,info:str,db:Session=Depends(get_db)):
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
                           db.query(models.Performance_Indicator).filter(models.Performance_Indicator.id==ids).update({'Current_status':info})
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

@router.get("/performance_indicator_id/{ids}")
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
                            singular_data = db.query(models.Performance_Indicator).filter(models.Performance_Indicator.id==ids).filter(models.Performance_Indicator.status=='ACTIVE').first()
                            response_data = jsonable_encoder({'Result':singular_data})
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

@router.post("/performanc_indicator_update")
async def getting(request:Request,db:Session=Depends(get_db),edit_idz:int=Form(...),e_desg:str=Form(...),e_c_exp:str=Form(...),e_mark:str=Form(...),e_t_manage:str=Form(...),e_admin:str=Form(...),e_skill:str=Form(...),e_work:str=Form(...),e_efficy:str=Form(...),e_integ:str=Form(...),e_profes:str=Form(...),e_team:str=Form(...),e_think:str=Form(...),e_manage:str=Form(...),e_attend:str=Form(...),e_deadline:str=Form(...),e_c_status:str=Form(...)):
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
                            check_exit_data = db.query(models.Performance_Indicator).filter(models.Performance_Indicator.id!=edit_idz,models.Performance_Indicator.Designation_id==e_desg).filter(models.Performance_Indicator.status=='ACTIVE').all()
                            if not check_exit_data:
                               db.query(models.Performance_Indicator).filter(models.Performance_Indicator.id==edit_idz).update({'Designation_id':e_desg,'Customer_Experience':e_c_exp,'Marketing':e_mark,'Management':e_t_manage,'Administration':e_admin,'Presentation_Skill':e_skill,'Quality_Of_Work':e_work,'Efficiency':e_efficy,'Integrity':e_integ,'Professionalism':e_profes,'Team_Work':e_team,'Critical_Thinking':e_think,'Conflict_Management':e_manage,'Attendance':e_attend,'Meet_Deadline':e_deadline,'Current_status':e_c_status})
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
  
#=========================================================================================#
#================================= Performance Appraisal =================================#
#=========================================================================================#
    
@router.get("/performance_appraisal")
async def getting(request:Request,db:Session=Depends(get_db)):
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
                            designation_data = db.query(models.Designation).filter(models.Designation.status=='ACTIVE').all()
                            department_data = db.query(models.Department).filter(models.Department.status=='ACTIVE').all()
                            employee_data = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                            appraisal_data = db.query(models.Performance_Appraisal).filter(models.Performance_Appraisal.status=='ACTIVE').all()
                            return templates.TemplateResponse("Admin/Performance/Performances/performance-appraisal.html",context={"request":request,'emp_data':emp_data,'designation_data':designation_data,'appraisal_data':appraisal_data,'department_data':department_data,'employee_data':employee_data})
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
    
@router.get("/performance_appraisal_employee/{emp_id}")
async def getting(request:Request,emp_id:int,db:Session=Depends(get_db)):
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
                            employee_data = db.query(models.Employee).filter(models.Employee.id==emp_id).filter(models.Employee.status=='ACTIVE').first()
                            Indicator_data = db.query(models.Performance_Indicator).filter(models.Performance_Indicator.Designation_id==int(employee_data.Designation_id)).filter(models.Performance_Indicator.status=='ACTIVE').first()
                            response_data =jsonable_encoder({'Result':Indicator_data})
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
 
@router.post("/performance_appraisal")
async def getting(request:Request,db:Session=Depends(get_db),emp_id:str=Form(...),date:str=Form(...),emp_exp:str=Form(...),emp_mark:str=Form(...),emp_manag:str=Form(...),emp_admin:str=Form(...),emp_skill:str=Form(...),emp_work:str=Form(...),emp_efficy:str=Form(...),emp_integ:str=Form(...),emp_profes:str=Form(...),emp_team:str=Form(...),emp_think:str=Form(...),emp_c_mange:str=Form(...),emp_attend:str=Form(...),emp_dead:str=Form(...),c_status:str=Form(...)):
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
                            check_exit_data = db.query(models.Performance_Appraisal).filter(models.Performance_Appraisal.Employee_id==emp_id).filter(models.Performance_Appraisal.status=='ACTIVE').all()
                            if not check_exit_data:
                                new_appraisal = models.Performance_Appraisal(Employee_id=emp_id,Date=date,Customer_Experience_Value=emp_exp,Marketing_Value=emp_mark,Management_Value=emp_manag,Administration_Value=emp_admin,Presentation_Skill_Value=emp_skill,Quality_Of_Work_Value=emp_work,Efficiency_Value=emp_efficy,Integrity_Value=emp_integ,Professionalism_Value=emp_profes,Team_Work_Value=emp_team,Critical_Thinking_Value=emp_think,Conflict_Management_Value=emp_c_mange,Attendance_Value=emp_attend,Meet_Deadline_Value=emp_dead,Current_status=c_status,status='ACTIVE',created_by=loginer_id)
                                db.add(new_appraisal)
                                db.commit()
                                db.refresh(new_appraisal)
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
   
@router.get("/performance_appraisal_status/{ids}/{info}")
async def getting(request:Request,ids:int,info:str,db:Session=Depends(get_db)):
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
                            db.query(models.Performance_Appraisal).filter(models.Performance_Appraisal.id==ids).update({'Current_status':info})
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
      
@router.get("/performance_appraisal_id/{ids}")
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
                            exit_data = db.query(models.Performance_Appraisal).filter(models.Performance_Appraisal.id==ids).filter(models.Performance_Appraisal.status=='ACTIVE').first()
                            employee_data = db.query(models.Employee).filter(models.Employee.id==int(exit_data.Employee_id)).filter(models.Employee.status=='ACTIVE').first()
                            indicator_data = db.query(models.Performance_Indicator).filter(models.Performance_Indicator.Designation_id==str(employee_data.Designation_id)).filter(models.Performance_Indicator.status=='ACTIVE').first()
                            response_data = jsonable_encoder({'Result':exit_data,'indicator':indicator_data})
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
   
@router.post("/performance_appraisal_update")
async def getting(request:Request,db:Session=Depends(get_db),edit_idz:int=Form(...),eemp_id:str=Form(...),edate:str=Form(...),eemp_exp:str=Form(...),eemp_mark:str=Form(...),eemp_manag:str=Form(...),eemp_admin:str=Form(...),eemp_skill:str=Form(...),eemp_work:str=Form(...),eemp_efficy:str=Form(...),eemp_integ:str=Form(...),eemp_profes:str=Form(...),eemp_team:str=Form(...),eemp_think:str=Form(...),eemp_c_mange:str=Form(...),eemp_attend:str=Form(...),eemp_dead:str=Form(...),ec_status:str=Form(...)):
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
                            check_exit_data = db.query(models.Performance_Appraisal).filter(models.Performance_Appraisal.id!=edit_idz,models.Performance_Appraisal.Employee_id==eemp_id).filter(models.Performance_Appraisal.status=='ACTIVE').all()
                            if not check_exit_data:
                                db.query(models.Performance_Appraisal).filter(models.Performance_Appraisal.id==edit_idz).update({'Employee_id':eemp_id,'Date':edate,'Customer_Experience_Value':eemp_exp,'Marketing_Value':eemp_mark,'Management_Value':eemp_manag,'Administration_Value':eemp_admin,'Presentation_Skill_Value':eemp_skill,'Quality_Of_Work_Value':eemp_work,'Efficiency_Value':eemp_efficy,'Integrity_Value':eemp_integ,'Professionalism_Value':eemp_profes,'Team_Work_Value':eemp_team,'Critical_Thinking_Value':eemp_think,'Conflict_Management_Value':eemp_c_mange,'Attendance_Value':eemp_attend,'Meet_Deadline_Value':eemp_dead,'Current_status':ec_status})
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
        
@router.get("/performance_appraisal_delete/{ids}")
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
                            db.query(models.Performance_Appraisal).filter(models.Performance_Appraisal.id==ids).update({'status':'INACTIVE'})
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
  