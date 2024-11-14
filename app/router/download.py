from fastapi import APIRouter,Response,Request
from fastapi.responses import RedirectResponse
from app.manager import Manager
from starlette.middleware.base import BaseHTTPMiddleware,RequestResponseEndpoint
from . import splitter

class DownloadMiddleware(BaseHTTPMiddleware):
  async def dispatch(self,req:Request,call_next:RequestResponseEndpoint):
    if req.url.path.startswith("/download"):
      nbrSlash=req.url.path.count("/")
      if nbrSlash>2:
        url=req.url.path[len("/download/"):]
        url=url.replace("/",splitter)
        return RedirectResponse("/download/"+url,status_code=307)
      pass
    res=await call_next(req)
    return res

router= APIRouter(prefix='/download')

@router.get('/{file}')
async def download(file:str,res:Response,req:Request):
  obj=None
  response=None
  file=file.replace(splitter,"/")
  bucket_name:str
  if file.startswith("public/"):
    file=file[len("public/"):]
    bucket_name="public"
  else:
    bucket_name=req.state.client_id
    
  try:
    response=Manager.get_object(bucket_name,file)
    obj=response.read()
  except Exception as e:
    res.status_code=404
    return {"erreur":"fichier introuvable"}
  finally:
    if response is not None:
      response.close()
      response.release_conn()
  return Response(content=obj,media_type="application/octet-stream",headers={"Content-Disposition":f"attachment; filename={file}"})