import json,sys
c=json.load(open(sys.argv[1]))['services']
print(' | '.join([c['auth']['environment']['FRONTEND_URL'],c['api-gateway']['environment']['CORS_ORIGINS'].split(',',4)[-1],c['demo-service']['environment']['CORS_ORIGINS']]))
