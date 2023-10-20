
# -*- coding: utf-8 -*-

class NodeTalentNum(list):
    def __init__(self):
        list.__init__(self)

    def asDict(self):
        data = {
            "treeIdx": self[0],
            "nodeIdx": self[1],
            "elementary": self[2],
            "ultimate": self[3],
            "parent": self[4],
            "talentNum": self[5],
            "maxNum": self[6],
            "totalPoints": self[7]
        }
        return data

    def createFromDict(self, dictData):
        self.extend([dictData['treeIdx'],
                     dictData["nodeIdx"],
                     dictData["elementary"],
                     dictData["ultimate"],
                     dictData["parent"],
                     dictData["talentNum"],
                     dictData["maxNum"],
                     dictData["totalPoints"]
                     ])
        return self


class NODE_TALENT_NUM_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dictData):
        return NodeTalentNum().createFromDict(dictData)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, NodeTalentNum)


node_talent_num_inst = NODE_TALENT_NUM_PICKLER()


