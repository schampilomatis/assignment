import os
import sys
import json
from subprocess import call

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APPS_PATH = os.path.join(PROJECT_PATH, 'xs2xps')

with open(sys.argv[1], 'r') as f:
    data = json.loads(f.read())

templates = [
    'models',
    'serializers',
    'views',
    'urls',
    'admin',
    'urls_config',
    'populate_script'
]

print 'starting code generation...'
#compile all templates
print 'compiling templates...'
for tpl in templates:
    call('cheetah compile {}/utility/generator/template/apps/{}.tmpl'.format(PROJECT_PATH, tpl).split())
print 'finished compiling'

print 'generating code...'
m = __import__('template.apps', globals(), locals(), templates)

appnames = []
for app in data['apps']:
    appnames.append(app['appname'])
    try:
        os.mkdir(os.path.join(APPS_PATH, app['appname']))
    except OSError:
        pass
    init = open(os.path.join(APPS_PATH, app['appname'], '__init__.py'), 'w')
    init.close()
    for tpl in templates: 
        if tpl != 'urls_config':
            try:
                tmpl = eval('m.'+tpl+'.'+tpl)
                tmpl = tmpl()
                print tpl
                tmpl.model_list = app['models']
                tmpl.app_name = app['appname']
                with open(os.path.join(APPS_PATH, app['appname'], '{}.py'.format(tpl)), 'w') as x:
                    x.write(tmpl.respond())
            except Exception,e:
                print e
    print 'all code for app {} generated!'.format(app['appname'])

tpl = 'urls_config'
tmpl = eval('m.'+tpl+'.'+tpl)
tmpl = tmpl()
with open(os.path.join(PROJECT_PATH, 'config', 'urls.py'), "a") as x:
    tmpl.appnames = appnames
    x.write(tmpl.respond())

print 'finished generating code!'
