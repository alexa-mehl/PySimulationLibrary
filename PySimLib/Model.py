class Model:
    #Constructor
    def __init__(this, name):
        #Private members
        this.__name = name;
        
    #Public methods
    def GetCompatibleTools(this):
        from . import GetTools;
        
        tools = GetTools();
        result = [];
        
        for tool in tools:
            if(tool.Accepts(this)):
                result.append(tool);
        
        return result;
        
    def GetName(this):
        return this.__name;
