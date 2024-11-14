from fastapi import APIRouter,Response,Request, \
  File, UploadFile, Form
from ..manager import Manager
import random, string
from pydantic import BaseModel
from minio.deleteobjects import DeleteObject

router= APIRouter()

def random_string():
  letters= string.ascii_letters
  return ''.join(random.choice(letters) for i in range(7))

@router.post('/upload')
async def upload(req:Request,res:Response, \
  file:UploadFile=File(...),to:str=Form(...)):
  filename=to+'/'+random_string()+'.'+file.filename
  filename=filename.replace("//","/")
  try:
    Manager.put_object(req.state.client_id,
      filename,file.file,file.size,
      content_type=file.content_type)
  except Exception as e:
    res.status_code=500
    return {"erreur":"fichier non enregistré"}
  return {"filename":filename}
  
class Object(BaseModel):
  name:str|None=None
  names:list[str]|None=None
  
@router.post("/delete")
async def delete(req:Request,res:Response,object:Object):
  if not ((object.name!=None) ^ (object.names!=None)):
    res.status_code=400
    return {"erreur":"nom de fichier manquant ou en trop avec propriété names"}
  try:
    errors=[]
    if object.name!=None:
      Manager.remove_object(req.state.client_id,object.name)
    else:
      objects=[]
      for name in object.names:
        objects.append(DeleteObject(name))
      errors=Manager.remove_objects(req.state.client_id,objects)
  except Exception as e:
    res.status_code=500
    return {"erreur":"une erreur s'est produite lors de la suppression du fichier"}
  finally:
    for error in errors:
      print(f"une erreur s'est produit lors de la suppresion de {error.name}",error)

  return {"message":f"fichier {object.name or object.names} supprimé"}