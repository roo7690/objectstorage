from fastapi import Request, Response, APIRouter
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from key import Token
import os,json
from ..manager import Manager

router=APIRouter()
token=Token(os.getenv('APP_NAME'))

class SecuriseMiddleware(BaseHTTPMiddleware):
  async def dispatch(self,req:Request,call_next:RequestResponseEndpoint):
    if req.url.path!='/' and req.url.path.startswith('/dashboard')==False \
      and req.url.path.startswith('/download/public')==False :
      res=Response()
      key=req.headers.get('Access-Key')
      if not key:
        res.status_code=403
        res.body='{"message":"Access-Key manquant"}'
        return res
      if not token.verifyToken(key):
        res.status_code=403
        res.body='{"message":"Access-Key invalide"}'
        return res
      client_id=token.getClient(key)
      if Manager.bucket_exists(client_id)==False:
        res.status_code=403
        res.body='{"message":"Accès refusé"}'
        return res
      req.state.client_id=client_id
    return await call_next(req)
  

splitter="......."

@router.get('/')
async def home():
  with open('res/home.json') as h:
    return json.load(h)