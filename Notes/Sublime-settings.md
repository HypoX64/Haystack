[toc]
# Sublime-settings
## ubuntu
### python
#### anaconda
```json
{
    "python_interpreter": "/home/hypo/anaconda3/envs/pytorch/bin/python3",
    "supress_word_completions": true,
    "supress_explicit_completions": true,
    "complete_parameters": true,
    "anaconda_linting": false
}
```
#### build system
```json
{
	"cmd":["python", "$file"],
	"path":"/home/hypo/anaconda3/envs/pytorch/bin", 
	"file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
	"selector": "source.python",
	"encoding": "utf-8"
}
```
## windows
### python
#### anaconda
```json
{
    "python_interpreter": "C:/Users/hypo/Anaconda3/envs/pytorch_0.4.1/python.exe",
    "supress_word_completions": true,
    "supress_explicit_completions": true,
    "complete_parameters": true,
    "anaconda_linting": false
}
```
#### build system
```json
{
	"cmd":["python", "$file"],
	"path":"C:/Users/hypo/Anaconda3/envs/pytorch_0.4.1", 
	"file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
	"selector": "source.python",
	"encoding": "utf-8"
}
```
### java
```json
{  
"cmd": ["javac","-encoding","gbk","-d",".","$file"],  
"file_regex": "^(...*?):([0-9]*):?([0-9]*)",  
"selector": "source.java",  
"encoding":"gbk",  
  
"variants":  
    [  
        {  
            "name": "Run",  
            "shell": true,  
            "cmd" :  ["start","cmd","/c", "java ${file_base_name}&pause"],  
            "working_dir": "${file_path}",  
            "encoding":"gbk"  
        }  
    ]  
}  
```
### c
```json
{
	"working_dir": "$file_path",
	"cmd": "gcc -Wall \"$file_name\" -o \"$file_base_name\"",
	"file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$",
	"selector": "source.c",
 
	"variants": 
	[
		{	
		"name": "Run",
        	"shell_cmd": "gcc -Wall \"$file\" -o \"$file_base_name\" && start cmd /c \"\"${file_path}/${file_base_name}\" & pause\""
		}
	]
}

```
### c++
```json
{
	"encoding": "utf-8",
	"working_dir": "$file_path",
	"shell_cmd": "g++ -Wall -std=c++11 \"$file_name\" -o \"$file_base_name\"",
	"file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$",
	"selector": "source.c++",
 
	"variants": 
	[
		{	
		"name": "Run in sublime",
        	"shell_cmd": "g++ -Wall -std=c++11 \"$file_name\" -o \"$file_base_name\" && cmd /c \"${file_path}/${file_base_name}\""
		},
		{	
		"name": "CMD Run",
        	"shell_cmd": "g++ -Wall -std=c++11 \"$file\" -o \"$file_base_name\" && start cmd /c \"\"${file_path}/${file_base_name}\" & pause\""
		}
	]
}
```
### matlab
```json
{
    "cmd": ["C:/Program Files/MATLAB/R2015b/bin/matlab.exe", "-nodesktop", "-nosplash", "-r", "\"run('$file')\""],
    "selector": "source.m",
    "working_dir": "${project_path:${folder}}"
}
```