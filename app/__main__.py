import uvicorn,os
from argparse import ArgumentParser,ArgumentTypeError


def getServerOptions():
  parser=ArgumentParser()
  parser.add_argument('-p',type=int,help='port du server')
  parser.add_argument('-H',type=str,help='hostname du server')
  parser.add_argument('-M',type=str,help='Mode de lancement du server')
  args=parser.parse_args()

  if args.M not in ["dev","prod"]:
    raise ArgumentTypeError("le mode de lancement du server n'est pas spécifier (-M prod ou dev)")
  
  return {
    "server_address":{"hostname":args.H or 'localhost',"port":args.p or 7090},
    "env":{
      "mode":args.M
    }
  }

if __name__=='__main__':
  opt=getServerOptions()
  
  for var, val in opt["env"].items():
    os.environ[var]=val
    
  uvicorn.run("app.app:app",
    host=opt["server_address"]["hostname"],
    port=opt["server_address"]["port"],
    log_level='info',
    reload=True if opt["env"]["mode"]=='dev' else False,
    proxy_headers=False if opt["env"]["mode"]=='dev' else True)