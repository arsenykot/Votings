# Yaroshium DocGen
# Сложный скрипт для автоматизации сборки документации из одного центрального файла.

import xml.etree.ElementTree as XML
import os
import json
import csv
import io
#from datetime import datetime as dt

print("""
DocGen
""")

xfd = open("docs.xml", "r", encoding="utf-8")
xmlfile = XML.ElementTree(file=xfd)
xfd.close()
APPENDIX = "\n\n_Автоматически сгенерировано [DocGen](/doc/doc/index.md)_"
# dt.now().strftime("%d/%m/%Y %H:%M")

ROOT = xmlfile.getroot()

def csv2md(csv_data):
    sd = csv.reader(io.StringIO("\n".join(csv_data).replace("|","\\|")), delimiter=";")
    DATA = []
    PEAK_LEN = []
    for row in sd:
        DATA.append(row)
    for row in DATA:
        for i, col in enumerate(row):
            if len(PEAK_LEN) <= i:
                PEAK_LEN.append(0)
            if len(col) > PEAK_LEN[i]:
                PEAK_LEN[i] = len(col)
    rs = ""
    for i, row in enumerate(DATA):
        rs += "|"
        for j, col in enumerate(row):
            ffs = "{: <"+str(PEAK_LEN[j])+"}"
            rs += ffs.format(col)+"|"
        if i == 0:
            rs += "\n|"
            for j, col in enumerate(row):
                ffs = "{:-<"+str(PEAK_LEN[j]-1)+"}"
                rs += ":"+ffs.format("")+"|"
        rs += "\n"
    return rs

def find(element, name):
    return element.find("{.}"+name)

def findTxt(element, name):
    ed = find(element, name)
    if ed == None:
        return ""
    return ed.text

def parseDoc(element, prefix = ""):
    struct = {
        "type": "file",
        "title": findTxt(element, "title"),
        "desc": findTxt(element, "desc"),
        "xmltags": [],
        "methods": [],
        "models": [],
        "tables": []
    }
    ofp = prefix+"/"+find(element, "path").text+".md"
    print("Parsing: "+ofp)
    struct["path"] = ofp
    for elem in element:
        print("- "+elem.tag)
        match elem.tag:
            case "{.}method":
                mstruct = {
                    "type": "method",
                    "name": findTxt(elem, "name"),
                    "desc": findTxt(elem, "desc"),
                    "args": [],
                    "force_args": findTxt(elem, "argsor"),
                    "ret" : findTxt(elem, "ret")
                    }
                for arg in elem.findall("{.}arg"):
                    mstruct["args"].append({
                        "name": findTxt(arg, "name"),
                        "type": findTxt(arg, "type"),
                        "desc": findTxt(arg, "desc")
                        })
                struct["methods"].append(mstruct)
            case "{.}model":
                mstruct = {
                    "type": "model",
                    "name": findTxt(elem, "name"),
                    "desc": findTxt(elem, "desc"),
                    "args": []
                    }
                for arg in elem.findall("{.}arg"):
                    mstruct["args"].append({
                        "name": findTxt(arg, "name"),
                        "type": findTxt(arg, "type"),
                        "desc": findTxt(arg, "desc")
                        })
                struct["models"].append(mstruct)
            case "{.}xmltag":
                xstruct = {
                    "type": "xmltag",
                    "name": findTxt(elem, "name"),
                    "desc": findTxt(elem, "desc"),
                    "args": []
                    }
                for arg in elem.findall("{.}arg"):
                    xstruct["args"].append({
                        "name": findTxt(arg, "name"),
                        "type": findTxt(arg, "type"),
                        "desc": findTxt(arg, "desc")
                        })
                struct["xmltags"].append(xstruct)
            case "{.}table":
                tstruct = {
                    "type": "table",
                    "name": findTxt(elem, "name"),
                    "header": findTxt(elem, "header"),
                    "rows": []
                }
                for row in elem.findall("{.}row"):
                    tstruct["rows"].append(row.text)
                struct["tables"].append(tstruct)
    return struct

def parseIndex(element, prefix = ""):
    struct = {
        "type": "index",
        "title": findTxt(element, "title"),
        "desc": findTxt(element, "desc"),
        "children": []
    }
    ofp = prefix + "/" + find(element, "path").text
    struct["path"] = ofp
    for elem in element:
        match elem.tag:
            case "{.}folder":
                struct["children"].append(parseIndex(elem, ofp))
            case "{.}file":
                struct["children"].append(parseDoc(elem, ofp))
    return struct

def generateIndex(struct, prefix = ""):
    ret = ""
    if struct["type"] == "index":
        for elem in struct["children"]:
            kp = elem["path"]
            if not kp.endswith(".md"):
                kp += "/index.md"
            ret += "\n%s- [%s](%s)"%(prefix, elem["title"], kp)
            ret += generateIndex(elem, prefix+"- ")
    return ret

def renderArgs(arr, header, item_fstr, item_tuple,  item_vars):
    ofc = ""
    argnames = []
    ftable = [header]
    for arg in arr:
        argnames.append(arg["name"])
        ftable.append(item_fstr%eval(item_tuple, locals=locals(), globals=item_vars))
    argnames = ", ".join(argnames)
    if len(ftable) > 1:
        ofc += "\n"
        ofc += csv2md(ftable)
        ofc += "\n"
    return ofc, argnames

def renderStruct(struct, parent=None):
    print("Rendering: "+struct["path"])
    links = "[Корень](/"+findTxt(ROOT,"path")+"/index.md)"
    if parent == None:
        parent = findTxt(ROOT, "path")
        links = ""
    else:
        links = "[Выше]("+parent+"/index.md) | " + links
    match struct["type"]:
        case "index":
            if not os.path.isdir("."+struct["path"]):
                os.mkdir("."+struct["path"])
            ofc = "# %s\n%s\n\n%s"%(struct["title"], links, struct["desc"])
            ofc += generateIndex(struct)
            ofc += APPENDIX
            ofd = open("."+struct["path"]+ "/index.md", "w+", encoding="utf-8")
            ofd.write(ofc)
            ofd.close()
            for elem in struct["children"]:
                renderStruct(elem, struct["path"])
        case "file":
            ofc = "# %s\n%s\n\n%s"%(struct["title"], links, struct["desc"])
            for method in struct["methods"]:
                cofc, argnames = renderArgs(method["args"], "Параметр;Тип;Описание", "`%s`;`%s`;%s", "(arg['name'], arg['type'], arg['desc'])", {})
                if method["force_args"] != "":
                    argnames = method["force_args"]
                ofc += "\n\n### `%s(%s) -> %s`\n%s"%(method["name"], argnames, method["ret"], method["desc"]) + cofc

            for xmltag in struct["xmltags"]:
                cofc, argnames = renderArgs(xmltag["args"], "Параметр;Тип;Описание", "`%s`;`%s`;%s", "(arg['name'], arg['type'], arg['desc'])", {})
                ofc += "\n\n### `<%s>`\n%s"%(xmltag["name"], xmltag["desc"]) + cofc

            for model in struct["models"]:
                cofc, argnames = renderArgs(model["args"], "Поле;Тип;Описание", "`%s`;`%s`;%s", "(arg['name'], arg['type'], arg['desc'])", {})
                ofc += "\n\n### `%s`\n%s"%(model["name"], model["desc"]) + cofc

            for table in struct["tables"]:
                ofc += "\n\n### %s"%(table["name"])
                ftable = table["rows"]
                ftable.insert(0, table["header"])
                if len(ftable) > 1:
                    ofc += "\n"
                    ofc += csv2md(ftable)

            ofc += APPENDIX
            ofd = open("."+struct["path"], "w+", encoding="utf-8")
            ofd.write(ofc)
            ofd.close()

print("Parsing index")
STRUCT = parseIndex(ROOT)

#print(json.dumps(STRUCT, indent=2, ensure_ascii=False))
renderStruct(STRUCT)
print("Success!")
input()