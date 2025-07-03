from ._model import *
from ._mapi import *

#Function to remove duplicate set of values from 2 lists
# def unique_lists(li1, li2):
#     if type (li1) == list and type (li2) == list:
#         if len(li1) == len(li2):
#             indices_to_remove = []
#             for i in range(len(li1)):
#                 for j in range(i+1,len(li1)):
#                     if li1[i] == li1[j] and li2[i] == li2[j]:
#                         indices_to_remove.append(j)
#             for index in sorted(indices_to_remove, reverse = True):
#                 del li1[index]
#                 del li2[index]


# def sect_inp(sec):
#     """Section ID.  Enter one section id or list of section IDs.  Sample:  sect_inp(1) OR sect_inp([3,2,5])"""
#     Model.units()
#     a = MidasAPI("GET","/db/SECT",{"Assign":{}})
#     if type(sec)==int: sec = [sec]
#     b={}
#     for s in sec:
#         if str(s) in a['SECT'].keys() : b.update({s : a['SECT'][str(s)]})
#     # if elem = [0] and sec!=0: b.update({sec : })
#     if b == {}: b = "The required section ID is not defined in connected model file."
#     return(b)
#---------------------------------------------------------------------------------------------------------------


def sFlatten(list_of_list):
    # list_of_list = [list_of_list]
    return [item for elem in list_of_list for item in (elem if isinstance(elem, list) else [elem])]

# def getID_orig(element_list):
#     """Return ID of Node and Element"""
#     return [beam.ID for beam in sFlatten(element_list)]

def getID(*objects):
    objects = list(objects)
    _getID2(objects)
    return objects

def _getID2(objects):
    for i in range(len(objects)):
        if isinstance(objects[i], list):
            _getID2(objects[i])  # Recursive call for sublist
        else:
            objects[i] = objects[i].ID



def getNodeID(*objects):
    objects = list(objects)
    _getNodeID2(objects)
    return objects

def _getNodeID2(objects):
    for i in range(len(objects)):
        if isinstance(objects[i], list):
            _getNodeID2(objects[i])  # Recursive call for sublist
        else:
            objects[i] = objects[i].NODES




# def getNodeID_orig(element_list):
#     """Return Node IDs of Element"""
#     # return list(sFlatten([beam.NODES for beam in sFlatten(element_list)]))
#     return list(sFlatten([beam.NODES for beam in sFlatten(element_list)]))


def arr2csv(nlist):
    strinff = ",".join(map(str,nlist))
    return strinff

def zz_add_to_dict(dictionary, key, value):
    if key in dictionary:
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]