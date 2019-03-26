import json

class jsonExtractor:
    def bindJSON(this, JSON):
        if(type(JSON) == type("")):
            this.jsonTable = json.loads(JSON)
        elif(type(JSON) == type({})):
            this.jsonTable = JSON
        else:
            raise ValueError("JSON must be either a string or a dictionary")

    def getField(this, fieldname):
        try:
            return this.jsonTable[fieldname]
        except Exception as e:
            raise NameError("%s not in bound json obj\n"%(fieldname,))

    def getBool(this, fieldname, allowNull = False):
        field = this.getField(fieldname)
        if type(field) == type(True) or (allowNull and field == None):
            return field
        else:
            raise TypeError("%s is not a boolean value\n"%(fieldname,))

    def getString(this, fieldname, allowNull = False):
        field = this.getField(fieldname)
        if type(field) == type("") or (allowNull and field == None):
            return field
        else:
            raise TypeError("%s is not a string\n"%(fieldname,))

    def getInt(this, fieldname, allowNull = False, gt = None, gte = None, lt = None, lte = None):
        field = this.getField(fieldname)
        if type(field) == type(1) or (allowNull and field == None):
            if field != None and gt  != None and field <= gt :
                raise ValueError("%s must be greater than %i\n"%(fieldname, gt))
            if field != None and gte != None and field <  gte:
                raise ValueError("%s must be greater than or equal to %i\n"%(fieldname, gte))
            if field != None and lt  != None and field >= lt :
                raise ValueError("%s must be less than %i\n"%(fieldname, lt))
            if field != None and lte != None and field >  lte:
                raise ValueError("%s must be less than or equal to %i\n"%(fieldname, lte))
            return field
        else:
            raise TypeError("%s is not a int value\n"%(fieldname,))

    def getFloat(this, fieldname, allowNull = False, gt = None, gte = None, lt = None, lte = None):
        field = this.getField(fieldname)
        if type(field) == type(1.1) or (allowNull and field == None):
            if field != None and gt  != None and field <= gt :
                raise ValueError("%s must be greater than %i\n"%(fieldname, gt))
            if field != None and gte != None and field <  gte:
                raise ValueError("%s must be greater than or equal to %i\n"%(fieldname, gte))
            if field != None and lt  != None and field >= lt :
                raise ValueError("%s must be less than %i\n"%(fieldname, lt))
            if field != None and lte != None and field >  lte:
                raise ValueError("%s must be greater than or equal to %i\n"%(fieldname, lte))
            return field
        else:
            raise TypeError("%s is not a Float value\n"%(fieldname,))

    def getNumber(this, fieldname, allowNull = False, gt = None, gte = None, lt = None, lte = None):
        field = this.getField(fieldname)
        if type(field) == type(1.1) or type(field) == type(1) or (allowNull and field == None):
            if field != None and gt  != None and field <= gt :
                raise ValueError("%s must be greater than %i\n"%(fieldname, gt))
            if field != None and gte != None and field <  gte:
                raise ValueError("%s must be greater than or equal to %i\n"%(fieldname, gte))
            if field != None and lt  != None and field >= lt :
                raise ValueError("%s must be less than %i\n"%(fieldname, lt))
            if field != None and lte != None and field >  lte:
                raise ValueError("%s must be greater than or equal to %i\n"%(fieldname, lte))
            return field
        else:
            raise TypeError("%s is not a number value\n"%(fieldname,))

    def getJSON(this, fieldname, allowNull = False):
        field = this.getField(fieldname)
        if type(field) == type({}) or (allowNull and field == None):
            return field
        else:
            raise TypeError("%s is not a JSON object\n"%(fieldname,))

    def getArray(this, fieldname, allowNull = False):
        field = this.getField(fieldname)
        if type(field) == type([]) or (allowNull and field == None):
            return field
        else:
            raise TypeError("%s is not a array object\n"%(fieldname,))

    def getNull(this, fieldname):
        field = this.getField(fieldname)
        if field == None:
            return field
        else:
            raise TypeError("%s is not Null\n"%(fieldname,))
