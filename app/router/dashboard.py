from fastapi import APIRouter,Response,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..manager import Manager
from pydantic import BaseModel
from key import _2FA
from dotenv import load_dotenv
import os
from . import token

load_dotenv()

router= APIRouter(prefix='/dashboard')
templates=Jinja2Templates(
  directory=os.path.join(os.path.dirname(
    os.path.abspath(__file__)),'../../res')
)

class IsAdmin(BaseModel):
  id:str
  pw:str
  sc:int|None=None
  to:str|None=None
  delay:int|None=None
  
def isadmin(ad:IsAdmin,res:Response|None=None):
  if not(os.getenv('MINIO_ROOT_USER')==ad.id and os.getenv('MINIO_ROOT_PASSWORD')==ad.pw):
    res.status_code=403
    return {"message":"Vous n'avez pas le droit de faire cette demande"}
  elif not ad.sc:
    code=_2FA.updateAdminCode()
    try:
      _res={"message":"Veuillez entrer le code envoyé à votre email"}
      _2FA.sendAdminCode(code,os.getenv('MAIL_USER'))
    except Exception as e:
      res.status_code=504
      print(str(e))
      _res={"message":"Le code n'a pas pu être envoyé!"}
    return _res
  else:
    if _2FA.verifyAdminCode(ad.sc)==False:
      return {"message":"Code incorrect"}
  return True

@router.get('/',response_class=HTMLResponse)
async def dashboard(req:Request):
  return templates.TemplateResponse('dashboard.html',{"request":req})
  
@router.post('/get-access')
async def getAccess(ad:IsAdmin,res:Response):
  is_admin=isadmin(ad,res)
  if is_admin!=True:
    return is_admin
  
  if not ad.to:
    return {
      "message":"Veuillez préciser pour qui vous voulez générer le token",
      "to":"<client>",
      "delay":"<delay>"
    }
  
  if Manager.bucket_exists(ad.to):
    return {"message":f"{ad.to} possède déjà des accès."}
  try:
    Manager.make_bucket(ad.to,object_lock=True)
    res=token.createToken(ad.to,ad.delay)
  except Exception as e:
    print(f"Une erreur est survenue dans la création d'un client: {e}")
    res={"message":"Oups! Une erreur est survenue."} 
  
  return {"token":res}