from IPython.core.display import display, HTML
import os
import json
import pprint

def updateFsTreeFile(srcpath, destfile):
    nodePathMap = {}    
    nodePathMap[srcpath] = {}
    for dirname, dirs, files in os.walk(srcpath, topdown=True):        
        if len(dirs) + len(files) > 0:
            nodePathMap[dirname]['children'] = []

        for d in dirs:
            fullpath = os.path.join(dirname, d)            
            newDir = {                
                "name": d
            }
            nodePathMap[fullpath] = newDir
            nodePathMap[dirname]["children"].append(newDir)

        """  
        for f in files:
            fullfile = os.path.join(dirname, f)            
            nodePathMap[dirname]["children"].append({                
                "name": f
            })
        """
    
    with open(destfile, 'w') as outfile:
        json.dump(nodePathMap[srcpath], outfile, indent=4)

def showFsTree():
    filename = 'fstree'
    updateFsTreeFile('dist/data/stackoverflow/', 'dist/visualisations/hierarchies/fstree.d3.json')
    iframe = """
        <iframe width="100%" 
                height="700"
                frameBorder="0" 
                src="http://localhost:3000/dist/visualisations/tree.html?f=fstree"
        </iframe>"""
    display(HTML(iframe))