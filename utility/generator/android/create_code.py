import os
import json
from Cheetah.Template import Template
from shutil import copyfile

# TODO: figure out date and time handling
javaFieldTypes = {
    "models.AutoField": {"name": "Integer", "accessor": "cursor.getInt({})"},
    "models.BigIntegerField": {"name": "Long", "accessor": "cursor.getLong({})"},
    "models.BinaryField": {"name": "Byte[]", "accessor": "cursor.getBlob({})"},
    "models.BooleanField": {"name": "Boolean", "accessor": "cursor.getInt({})>0"},
    "models.CharField": {"name": "String", "accessor": "cursor.getString({})"},
    "models.CommaSeparatedIntegerField": {"name": "Integer[]", "accessor": ""},#TODO
    "models.DateField": {"name": "String", "accessor": "cursor.getString({})"},#TODO
    "models.DateTimeField": {"name": "String", "accessor": "cursor.getString({})"},#TODO
    "models.DecimalField": {"name": "Double", "accessor": "cursor.getDouble({})"},
    "models.EmailField": {"name": "String", "accessor": "cursor.getString({})"},
    "models.FileField": {"name": "String", "accessor": "cursor.getString({})"},
    "models.FilePathField": {"name": "String", "accessor": "cursor.getString({})"},
    "models.FloatField": {"name": "Float", "accessor": "cursor.getFloat({})"},
    "models.ImageField": {"name": "String", "accessor": "cursor.getString({})"},
    "models.IntegerField": {"name": "Integer", "accessor": "cursor.getInt({})"},
    "models.IPAddressField": {"name": "String", "accessor": "cursor.getString({})"},
    "models.GenericIPAddressField": {"name": "String", "accessor": "cursor.getString({})"},
    "models.NullBooleanField": {"name": "Boolean", "accessor": "cursor.getInt({})>0"},
    "models.PositiveIntegerField": {"name": "Integer", "accessor": "cursor.getInt({})"},
    "models.PositiveSmallIntegerField": {"name": "Short", "accessor": "cursor.getShort({})"},
    "models.SlugField": {"name": "String", "accessor": "cursor.getString({})"},
    "models.SmallIntegerField": {"name": "Short", "accessor": "cursor.getShort({})"},
    "models.TextField": {"name": "String", "accessor": "cursor.getString({})"},
    "models.TimeField": {"name": "String", "accessor": "cursor.getString({})"},#TODO
    "models.URLField": {"name": "String", "accessor": "cursor.getString({})"},
    "models.ForeignKey": {"name": "Integer", "accessor": "cursor.getInt({})"},
    "models.ManyToManyField": {"name": "ManyToMany", "accessor": ""},#TODO
    "models.OneToOneField": {"name": "Integer", "accessor": "cursor.getInt({})"},

}

PROJECT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)))

def uppercaseFirst(text):
    return text[:1].upper() + text[1:] if text else ''


def lowercaseFirst(text):
    return text[:1].lower() + text[1:] if text else ''

def getModelPath():
    path = os.path.join(PROJECT_PATH, '..', 'android', 'database', 'models')
    try:
        os.makedirs(path, 0777)
    except:
        pass # dirs already exist
    return path

def getDatabasePath():
    path = os.path.join(PROJECT_PATH, '..', 'android', 'database')
    try:
        os.makedirs(path, 0777)
    except:
        pass # dirs already exist
    return path

def readTemplate(templateName):
    with open("./generator/android/template/{}".format(templateName), 'r') as template:
        template = template.read()
    return template

def writeTemplate(content, filename):
    with open(filename, 'w') as outputFile:
        outputFile.write(str(content))

"""
    Adds java data to our json input.

    fields added to models: name_lower, name_upper, counter, projection
    fields added to fields: javaType, name_lower, name_upper, name_all_caps

"""
def genJavaData(jsonData, packageName):
    modelCounter = 100
    jsonData["packageName"] = packageName
    for appKey, app in enumerate(jsonData['apps']):
        for modelKey, model in enumerate(app['models']):
            # And let the silliness commence
            jsonData['apps'][appKey]['models'][modelKey]['fields'].insert(0, {
                "name": "_id",
                "type": "models.IntegerField",
                "null": False,
                "blank": False
            })
            modelName = jsonData['apps'][appKey]['models'][modelKey]['name']
            jsonData['apps'][appKey]['models'][modelKey]['name_lower'] = modelName.lower()
            jsonData['apps'][appKey]['models'][modelKey]['name_upper'] = modelName.upper()
            jsonData['apps'][appKey]['models'][modelKey]['counter'] = modelCounter
            modelCounter += 100
            projection = []
            for fieldKey, field in enumerate(jsonData['apps'][appKey]['models'][modelKey]['fields']):

                # adjust foreign key fields
                if field['type'] in ['models.ForeignKey', 'models.OneToOneField']:
                    field['name'] = "{}_id".format(field['key'].lower())

                # several casings for field name
                jsonData['apps'][appKey]['models'][modelKey]['fields'][fieldKey]['name_lower'] = lowercaseFirst(field['name'])
                jsonData['apps'][appKey]['models'][modelKey]['fields'][fieldKey]['name_upper'] = uppercaseFirst(field['name'])
                jsonData['apps'][appKey]['models'][modelKey]['fields'][fieldKey]['name_all_caps'] = field['name'].upper()

                # Java type and method to access data from cursor
                jsonData['apps'][appKey]['models'][modelKey]['fields'][fieldKey]['javaType'] = {'name': javaFieldTypes[field['type']]['name'], 'accessor': ""}
                accessor = javaFieldTypes[field['type']]['accessor']
                jsonData['apps'][appKey]['models'][modelKey]['fields'][fieldKey]['javaType']['accessor'] = accessor.format("cursor.getColumnIndex({}Descriptor.Cols.{})".format(modelName, field['name'].upper()))

                # build up projection
                projection.append("Cols.{}".format(field['name'].upper()))

            jsonData['apps'][appKey]['models'][modelKey]['projection'] = ", ".join(projection)

    with open(os.path.join(PROJECT_PATH, 'output.json'), 'w') as outputFile:
            outputFile.write(str(json.dumps(jsonData)))

    return jsonData


"""
    Generates ContentDescriptor.java

"""
def genDescriptor(data):
    print "generating database/ContentDescriptor.java"
    # read templates
    descriptorTemplate = readTemplate("content_descriptor.tmpl")
    modelDescriptorTemplate = readTemplate("model_content_descriptor.tmpl")
    path = getDatabasePath()

    for app in data['apps']:
        # render model descriptors
        compiledTemplates = ""
        for model in app['models']:
            compiledTemplate = Template(
                modelDescriptorTemplate,
                searchList=[{'model': model, 'packageName': data['packageName']}]
            )
            compiledTemplates = "{}\n{}".format(compiledTemplates, compiledTemplate)
    # and collect the whole show in our final file
    compiledTemplate = Template(
        descriptorTemplate,
        searchList=[{'modelDescriptors': compiledTemplates, 'models': app['models'], 'packageName': data['packageName']}]
    )
    writeTemplate(compiledTemplate, os.path.join(path, 'ContentDescriptor.java'))


"""
    Generates the content provider

"""
def genProvider(data):
    print "generating database/DatabaseContentProvider.java"
    models = []
    for app in data['apps']:
        for model in app['models']:
            models.append(model)
    template = readTemplate('database_content_provider.tmpl')
    compiledTemplate = Template(
        template,
        searchList=[{'models': models, 'packageName': data['packageName']}]
    )
    writeTemplate(compiledTemplate, os.path.join(getDatabasePath(), 'DatabaseContentProvider.java'))




"""
    Generates a model for each table

"""
def genModels(data):
    with open("./generator/android/template/model.tmpl", 'r') as modelTemplate:
        modelTemplate = modelTemplate.read()

    with open("./generator/android/template/base_model.tmpl", 'r') as baseModelTemplate:
        baseModelTemplate = baseModelTemplate.read()

    modelsPath = getModelPath()

    # parse our base model
    print "generating database/models/Model.java"
    compiledBaseModelTemplate = Template(
        baseModelTemplate,
        searchList=[{'packageName': data['packageName']}]
    )
    with open(os.path.join(modelsPath, 'Model.java'), 'w') as outputFile:
        outputFile.write(str(compiledBaseModelTemplate))

    for app in data['apps']:
        # render models
        for model in app['models']:
            print "generating database/models/{}.java".format(uppercaseFirst(model['name']))
            nameSpace = {'model': model, 'packageName': data['packageName']}
            compiledTemplate = Template(
                modelTemplate,
                searchList=[nameSpace]
            )
            with open(os.path.join(modelsPath, '{}.java'.format(model['name'].title())), 'w') as outputFile:
                outputFile.write(str(compiledTemplate))


def genDbHelpers(data):
    path = getDatabasePath()
    searchList = [{'packageName': data['packageName']}]

    manifest_template = readTemplate("manifest.tmpl")
    compiledTemplate = Template(
        manifest_template,
        searchList = searchList
    )
    writeTemplate(compiledTemplate, os.path.join(path, 'ManifestFragment.xml'))

    database_helper_template = readTemplate("database_helper.tmpl")
    compiledTemplate = Template(
        database_helper_template,
        searchList = searchList
    )
    writeTemplate(compiledTemplate, os.path.join(path, 'DatabaseHelper.java'))

    sdcard_sqlite_open_helper_template = readTemplate("sdcard_sqlite_open_helper.tmpl")
    compiledTemplate = Template(
        sdcard_sqlite_open_helper_template,
        searchList = searchList
    )
    writeTemplate(compiledTemplate, os.path.join(path, 'SDCardSQLiteOpenHelper.java'))


"""
    Reads our input file and collects pakage name from command line

"""
def parse(filename):

    if not os.path.isfile(filename):
        print "{} was not found.... please try again.".format(filename)
        exit()
    try:
        with open(filename, 'r') as f:
            data = json.loads(f.read())
    except:
        print "{} does not parse as a json file dude.... please try again.".format(filename)
        exit()

    packageName = raw_input("Please enter a package name (com.xs2.project)")
    packageName = "com.xs2.project" if packageName == "" else packageName

    data = genJavaData(data, packageName)

    print 'Starting java code generation...'

    genDbHelpers(data)

    genDescriptor(data)

    genProvider(data)

    genModels(data)




















    print ''
    print ''
    print ''
    print 'All done...'
    print r"""


             .-----.
           ,' -   - `.
   _ _____/  <q> <p>  \_____ _
  /_||   ||`-._____.-`||   ||-\
 / _||===||           ||===|| _\    I GOT AN ANDROID AND WHAT THE FUCK
|- _||===||===========||===||- _|    IT'S NOT EVEN HUMAN-SHAPED
\___||___||___________||___||___/
 \\|///   \_:_:_:_:_:_/   \\\|//
 |   _|    |_________|    |   _|
 |   _|   /( ======= )\   |   _|
 \\||//  /\ `-.___.-' /\  \\||//
  (o )  /_ '._______.' _\  ( o)
 /__/ \ |    _|   |_   _| / \__\
 ///\_/ |_   _|   |    _| \_/\\\
///\\_\ \    _/   \    _/ /_//\\\
\\|//_/ ///|\\\   ///|\\\ \_\\|//
        \\\|///   \\\|///
        /-  _\\   //   _\
        |   _||   ||-  _|           I WAS HOPING FOR A FUCK TOY AND
      ,/\____||   || ___/\,          I ALL GOT WAS THIS STUPID PHONE
     /|\___`\,|   |,/'___/|\
     |||`.\\ \\   // //,'|||
     \\\\_//_//   \\_\\_////
        """