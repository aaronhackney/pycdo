# we do not want to import model classes here because that would create a circular reference
# do not import all models into this module because that uses a lot of memory and stack frames
# if you need the ability to import all models from one package, import them with
# from {{packageName}.models import ModelA, ModelB
