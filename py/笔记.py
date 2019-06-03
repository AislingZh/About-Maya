import maya.cmds as cmds
def forLoopShort():
    objs = {1,2,3,4,5,6,7,8,9,10,11,12,13,14}
    objList = []
    for i in objs:
        if i > 10:
            objList.append(i)

    objListShort = [i for i in objs if i > 10]
    
def ifElseShort():
    nums = {0,1,2,3,4,5,6}
    if nums:
        maxNum = max(nums)
    else:
        maxNum = None
    
    minNum = min(nums) if nums else None

def lambdaMapShort():

    sqList = map(lambda x: x*x, [y for y in range(10)])

    orgList = [y for y in range(10)]
    sqList = []
    def sq(x):
        return x*x
    for i in orgList:
        a = sq(i)
        sqList.append(a)