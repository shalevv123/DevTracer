**DevTracer – User Guide** 

**Query(\*, visualize=False, file\_name='visualization')** 

Decorator for query functions that connects to the database and runs the query. The decorator can be applied to functions of the following format: 

(\*args, \*\*kwargs) -> query: str  Parameters: 

- Visualize: bool, default=False. 

indicates whether to visualize the result of the query or not. 

If set to True, an html file of the visualization will be created in the working directory and opened in the default browser. 

- file\_name: str, default='visualization'. 

If visualize is true, specifies the file name for the output html file. 

Returns:  

A list that represents the output of running the query on the database. Example: 

![](Aspose.Words.b973b0b5-eaa6-439d-aeef-4b965df0e98c.001.png)

**InitData(file\_path)** 

Loads the data from a JSON file into the database. Parameters: 

- file\_path: str. 

Specifies the path to the input JSON file. 

**resetDatabase()** 

Deletes all the data inside the database. 

**LookObject(id)** 

Returns all the paths to all the objects connected to the object with the given id. An html file of the visualization named “lookup\_query” will be created in the working directory and opened in the default browser. 

Parameters: 

- id: str. 

The id of the desired object. 

Returns:  

A list that represents the output of running the query on the database. 

**unimplementedReq(node\_type)** 

Returns all the unimplemented requirements of type node\_type. Parameters: 

- node\_type: [“SysReq” , “HLR” , “LLR”]. The type of the desired requirement. 

Returns:  

A list that represents the output of running the query on the database. 

**untestedReq(node\_type)** 

Returns all the untested requirements of type node\_type. Parameters: 

- node\_type: [“SysReq”, “HLR” , “LLR”]. The type of the desired requirement. 

Returns:  

A list that represents the output of running the query on the database. 

**unlinkedTests()** 

Returns all the tests that are not connected to any object. 

Returns:  

A list that represents the output of running the query on the database. 

**completeSysReq()** 

Returns all the system requirements that are fully implemented, verified, and tested. 

Returns:  

A list that represents the output of running the query on the database. 
