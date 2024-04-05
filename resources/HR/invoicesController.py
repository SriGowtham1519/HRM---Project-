from typing import Dict, List,Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Depends, FastAPI, Request, Form,status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse,RedirectResponse,HTMLResponse
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


# Get The Template
@router.get('/invoice') 
def get_form(request: Request, db: Session = Depends(get_db)):
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
                            invoice_data = db.query(models.Invoice).filter(models.Invoice.status!="INACTIVE").all()
                            return templates.TemplateResponse("Admin/HR/Sales/invoices.html", context={"request": request, 'invoice_data': invoice_data,"format_display_date":format_display_date,'emp_data':emp_data})
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
    
def convert_to_db_date_format(date_str):
    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
    return date_obj.strftime('%Y-%m-%d')

@router.get('/filtered-invoices')
def get_filtered_invoices( request: Request, db: Session = Depends(get_db), from_date: str = None,to_date: str = None,status: str = None):
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
                            query = db.query(models.Invoice).filter(models.Invoice.status != "INACTIVE")
                            
                            if from_date:
                                from_date_converted = convert_to_db_date_format(from_date)
                                query = query.filter(models.Invoice.created_at >= from_date_converted)
                            if to_date:
                                to_date_converted = convert_to_db_date_format(to_date)
                                query = query.filter(models.Invoice.created_at <= to_date_converted)
                            if status:
                                query = query.filter(models.Invoice.status == status)
                            
                            invoice_data = query.all()
                            
                            # Process and return filtered data as needed
                            return {"invoice_data": invoice_data}
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
    
@router.get('/create-invoice') 
def get_form(request: Request, db: Session = Depends(get_db)):
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
                            client_data = db.query(models.Client).filter(models.Client.status=='ACTIVE').all()
                            tax_data = db.query(models.Taxes).filter(models.Taxes.status=='ACTIVE').all()
                            return templates.TemplateResponse("Admin/HR/Sales/create-invoice.html", context={"request": request,'emp_data':emp_data,'client_data':client_data,'tax_data':tax_data})
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
    
@router.post('/new-invoice')
def create_data(
    request: Request,
    db: Session = Depends(get_db),
    Client_id: str = Form(...),
    Project_id: str = Form(...),
    Email: str = Form(...),
    Tax: str = Form(...),
    Client_address: str = Form(...),
    Biling_address: str = Form(...),
    
    Expiry_Date: str = Form(...),
    Estimate_Date: str = Form(...),
    Discount: str = Form(...),
    Total: str = Form(...),
    item_Tax: str = Form(...),
    Grand_Total: str = Form(...),
    Information: str = Form(...),
    Item: List[str] = Form(...),
    Description: List[str] = Form(...),
    UnitCost: List[float] = Form(...),
    Qty: List[int] = Form(...),
    Amount: List[float] = Form(...),
    status: str = Form(...),
    
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
                            body = models.Invoice(
                                Client_id=Client_id,
                                Project_id=Project_id,
                                Email=Email,
                                Tax=Tax,
                                Client_address=Client_address,
                                Biling_address=Biling_address,
                                
                                Expiry_Date=Expiry_Date,
                                Estimate_Date=Estimate_Date,
                                Total=Total,
                                item_tax=item_Tax,
                                Discount=Discount,
                                Grand_Total=Grand_Total,
                                Information=Information,
                                status=status,
                                created_by=Client_id,
                            )
                            db.add(body)
                            db.commit()
                            db.refresh(body)

                            invoice_items = []
                            for i in range(len(Item)):
                                invoice_item = models.Invoice_Items(
                                    Invoice_id=body.id,
                                    Item=Item[i],
                                    Description=Description[i],
                                    Unit_Cost=str(UnitCost[i]),  
                                    Qty=str(Qty[i]),  
                                    Amount=str(Amount[i]), 
                                    status=status,
                                    created_by=Client_id
                                )
                                invoice_items.routerend(invoice_item)
                            db.add_all(invoice_items)
                            db.commit()
                            return RedirectResponse("/invoice", status_code=303)
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
    
@router.get("/Client_list",response_model=list[str])
def get_Client_ids(request: Request,db: Session = Depends(get_db)):
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
                            Client_ids = db.query(models.Client.Username).all()
                            return [id for (id,) in Client_ids]
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
    
@router.get('/invoice-view/{id}') 
def get_form(request: Request, db: Session = Depends(get_db)):
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
                            invoice_data = db.query(models.Invoice).filter(models.Invoice.id==id).first()
                            return templates.TemplateResponse("invoice-view.html", context={"request": request,"id": id, 'invoice_data': invoice_data})
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
    
@router.get('/edit_invoice/{id}')
def get_edit_invoice(request: Request, id: int, db: Session = Depends(get_db)):
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
                            invoice_data = db.query(models.Invoice).filter(models.Invoice.id == id).first()
                            return templates.TemplateResponse("edit_invoice.html", context={"request": request, "id": id, "invoice_data": invoice_data})
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
def taking_edit_id_addition(ids:int,request: Request,db: Session = Depends(get_db)):
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
                            invoice_data = db.query(models.Invoice).filter(models.Invoice.id == ids).first()
                            if not invoice_data:
                                raise HTTPException(status_code=404, detail="Invoice not found")
                            
                            invoice_items = db.query(models.Invoice_Items).filter(models.Invoice_Items.Invoice_id == ids).filter(models.Invoice_Items.status != "INACTIVE")
                            
                            items_list = [{"Item": item.Item, "Description": item.Description, "Unit_Cost": item.Unit_Cost, "Qty": item.Qty, "Amount": item.Amount} for item in invoice_items]
                            
                            return {"invoice": invoice_data, "items": items_list}
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
    
@router.post('/update')
def update_invoice_data(
    request: Request,
    db: Session = Depends(get_db),
    edit_id_id: int = Form(...),
    edit_id: str = Form(...),
    edit_projectname: str = Form(...),
    edit_email: str = Form(...),
    edit_tax: str = Form(...),
    edit_clientaddress: str = Form(...),
    edit_billingaddress: str = Form(...),
    edit_expiry: str = Form(...),
    edit_estimate: str = Form(...),
    edit_discount: str = Form(...),
    edit_total: str = Form(...),
    edit_itemtax: str = Form(...),
    edit_grandtotal: str = Form(...),
    edit_info: str = Form(...),
    edit_Item: List[str] = Form(...),
    edit_Description: List[str] = Form(...),
    edit_UnitCost: List[float] = Form(...),
    edit_Qty: List[int] = Form(...),
    edit_Amount: List[float] = Form(...),
    status: str = Form(...),
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
                            # Update the Invoice record
                            db.query(models.Invoice).filter(models.Invoice.id == edit_id_id).update({
                                "Client_id": edit_id,
                                "Project_id": edit_projectname,
                                "Email": edit_email,
                                "Tax": edit_tax,
                                "Client_address": edit_clientaddress,
                                "Biling_address": edit_billingaddress,
                                "Estimate_Date": edit_estimate,
                                "Expiry_Date": edit_expiry,
                                "Total": edit_total,
                                "item_tax": edit_itemtax,
                                "Discount": edit_discount,
                                "Grand_Total": edit_grandtotal,
                                "Information": edit_info,
                                "status" :status,
                            })

                        
                            existing_items = db.query(models.Invoice_Items).filter(models.Invoice_Items.Invoice_id == edit_id_id).all()

                            existing_item_names = {item.Item for item in existing_items}  # Extracting existing item names

                            invoice_items = []

                            for i in range(len(edit_Item)):
                                # Check if the item already exists before adding it again
                                if edit_Item[i] not in existing_item_names:
                                    invoice_item = models.Invoice_Items(
                                        Invoice_id=edit_id_id,
                                        Item=edit_Item[i],
                                        Description=edit_Description[i],
                                        Unit_Cost=str(edit_UnitCost[i]),
                                        Qty=str(edit_Qty[i]),
                                        Amount=str(edit_Amount[i]),
                                        status=status,
                                        created_by=edit_id
                                    )
                                    invoice_items.routerend(invoice_item)

                                
                                    db.add_all(invoice_items)

                            print(edit_Item[i],id)

                            # db.execute(
                            #         models.Invoice_Items.__table__.delete().where(
                            #             models.Invoice_Items.Invoice_id == models.Invoice.id,
                            #             # models.Invoice_Items.Email == editemail,
                            #             models.Invoice_Items.Item == edit_Item[i]
                            #         )
                            #         )
                            db.query(models.Invoice_Items).filter(
                            models.Invoice_Items.Invoice_id == edit_id_id,
                            models.Invoice_Items.Item == edit_Item[i]
                        ).delete()

                            db.commit()
                                    # return RedirectResponse("/invoice", status_code=303)


                            
                            if any(edit_UnitCost[i] < 0 for i in range(len(edit_UnitCost))) or \
                                any(edit_Qty[i] < 0 for i in range(len(edit_Qty))) or \
                                any(edit_Amount[i] < 0 for i in range(len(edit_Amount))):
                                    # raise HTTPException(status_code=400, detail="Negative values are not allowed")
                                return HTMLResponse(
                                        """
                                        <script>
                                            alert("Negative value not accepted");
                                            window.location.href = "/invoice"; // Redirect to the department page
                                        </script>
                                        """
                                    )
                                
                                
                            db.add_all(invoice_items)
                            db.commit()
                            
                            return RedirectResponse("/invoice", status_code=303)
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
                            db.query(models.Invoice).all()
                            db.query(models.Invoice).filter(models.Invoice.id == ids).update({"status":"INACTIVE"})
                            db.query(models.Invoice_Items).filter(models.Invoice_Items.Invoice_id == ids).update({"status":"INACTIVE"})
                            db.commit()
                            return templates.TemplateResponse("invoices.html",context={"request":request})
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
    
@router.get("/projects/{client_id}")
def get_projects_for_client(client_id: str,request: Request, db: Session = Depends(get_db)):
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
                            projects = db.query(models.Project).filter(models.Project.Client_id == client_id).all()
                            if projects:
                                client_data = db.query(models.Client).filter(models.Client.id==int(client_id)).filter(models.Client.status=='ACTIVE').first()
                                return projects,client_data
                            else:
                                return 'empty'
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
    
def format_display_date(date_str):
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
    # Format the date as "day Month Year" (e.g., 12 May 2023)
    formatted_date = date_obj.strftime('%d %b %Y')
    return formatted_date

#===================================================>>>>> select a tax value 

@router.get("/Taxvalue/{tax_id}")
def get_projects_for_client(tax_id: int,request: Request, db: Session = Depends(get_db)):
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
                            tax_data = db.query(models.Taxes).filter(models.Taxes.id==tax_id).filter(models.Taxes.status=='ACTIVE').first()
                            return tax_data
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
    
  