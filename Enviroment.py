from llvmlite import ir

class Enviroment():
    def __init__(self, records: dict[str, tuple[ir.Value, ir.Type]] = None, parent = None, name: str = "global"):
        self.records: dict[str, tuple] = records if records else {}
        self.parent: Enviroment | None = parent
        self.name: str = name

    def define(self, name:str, value: ir.Value, type_: ir.Type):
        self.records[name] = (value, type_)
        return value
    
    def lookup(self, name: str):
        return self.__resolve(name)
    
    def __resolve(self, name:str):
        if name in self.records:
            return self.records[name]
        elif self.parent:
            return self.parent.__resolve(name)
        else:
            return None
    

