import subprocess
def read_file(path: str)-> str:
    with open(path, "r") as f:
        return f.read()


READ_FILE_SCHEMA={
    "type":"function",
    "function":{
        "name":"read_file",
        "description":"Reads a file and returns its content",
        "parameters":{
            "type":"object",
            "properties":{
                "path":{
                    "type":"string"
                }
            },
            "required":[
                "path"
            ]
        },
        "returns":{
            "type":"string"
        }
    }
}

def write_file(path: str, content: str)-> str:
    with open(path, "w") as f:
        f.write(content)
    return f"Wrote {len(content)} bytes to {path}"

WRITE_FILE_SCHEMA={
    "type":"function",
    "function":{
        "name":"write_file",
        "description":"Writes content to a file",
        "parameters":{
            "type":"object",
            "properties":{
                "path":{
                    "type":"string"
                },
                "content":{
                    "type":"string"
                }
            },
            "required":[
                "path",
                "content"
            ]
        }
    }
}


def command_execute(command: str)-> str:
    return subprocess.check_output(command, shell=True,timeout=30).decode("utf-8")


COMMAND_EXECUTE_SCHEMA={
    "type":"function",
    "function":{
        "name":"command_execute",
        "description":"Executes a command and returns its output",
        "parameters":{
            "type":"object",
            "properties":{
                "command":{
                    "type":"string"
                }
            },
            "required":[
                "command"
            ]
        },
        "returns":{
            "type":"string"
        }
    }
}

# send it to the LLM 
TOOL_SCHEMAS=[
    READ_FILE_SCHEMA,
    WRITE_FILE_SCHEMA,
    COMMAND_EXECUTE_SCHEMA
]

# used by the application tto map 
TOOL_FUNCTIONS={
    "read_file":read_file,
    "write_file":write_file,
    "command_execute":command_execute
}