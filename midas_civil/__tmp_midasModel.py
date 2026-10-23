len_MULT = {"M":1,"CM":100, "MM" : 1000}

class _UNIT_DATA_:
    len_MULT = {}

class MIDAS_MODEL:
    def __init__(self,MAPI_KEY,name=None,len='M'):
        self.MAPI_KEY = MAPI_KEY
        self.NAME = name or "UNTITILED"


        self.DATA = {}



        self.UNITS = { "LEN":len }
        self._len_multiplier = 1


        self.Node = self._Node(self)   # bind the namespace to this instance
        

        print(f"-----------------       MODEL   CREATED  {self.NAME}      ----------------")

    def create(self):
        print(f"Creating model in CIVIL NX - MAPI - {self.MAPI_KEY}")

    def save(self,location=None):
        print(f"Saving model at {location}\\{self.NAME}.mcb")

    def clear(self):
        print("DELETING all data...")

    def print(self):
        print(self.Node.json())

    def Units(self,len):
        self._len_multiplier = len_MULT[self.UNITS["LEN"]]/len_MULT[len]

    # ---- the actual node data object ----
    class _NodeObj:
        def __init__(self, model, x ,y ,z):
            self.X = x * model._len_multiplier

        def __str__(self):
            return str(f"NODE at x = {self.X}")

    # ---- namespace/dispatcher exposed as `model.Node` ----
    class _Node:
        def __init__(self, model):
            self._model = model
            self.nodes = []   # optional: keep track of created nodes

        def json(self):
            for node in self.nodes:
                print(node)

        def __call__(self, x):
            """myModel.Node(1)"""
            node = MIDAS_MODEL._NodeObj(self._model, x)
            self.nodes.append(node)
            return node

        def create(self, x):
            """myModel.Node.create(1)"""
            print("creating node via create()")
            return self(x)   # reuse __call__

        def SE(self, x):
            """myModel.Node.SE(1) -- some special-element variant"""
            print("creating SE node")
            node = MIDAS_MODEL._NodeObj(self._model, x)
            node.TYPE = "SE"
            self.nodes.append(node)
            return node