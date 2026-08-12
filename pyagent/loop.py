
import litellm
import tools
import json 
MAX_ITERATIONS=10
def run(user_message : str,messages: list= None,emit=None)-> list:
    # dummy emit
    if emit is None:
        emit= lambda event:None
    emit({"type":"agent_start"})
    if messages is None:
        messages=[
            {
                "role":"system", "content": "You are a helpful coding  assistant.",
            },
            {
        "role":"user", "content": user_message,

            }
        ]
    else: 
        messages.append(
            {
                "role":"user", "content": user_message,

            }
        )
    current_iteration=0

    while current_iteration<MAX_ITERATIONS:
        emit({"type": "turn_start"})
        response=litellm.completion(
            model="gemini/gemini-flash-latest",
            messages=messages,
            tools=tools.TOOL_SCHEMAS
        )
        response_message= response.choices[0].message
        messages.append(response_message.model_dump())
        emit({"type": "assistant_message", "message": response_message.model_dump()})
        tools_calls= response_message.tool_calls
        if not tools_calls:
            # print(response_message.content)
            break
        for tool_call in tools_calls:
            tool_name=tool_call.function.name
            fn=tools.TOOL_FUNCTIONS[tool_name]
            tool_args=json.loads(tool_call.function.arguments)
            is_error=False 
            emit({"type": "tool_execution_start", "tool_call_id": tool_call.id, "tool_name": tool_name, "args": tool_args})
            try:
                resp=fn(**tool_args)
            except Exception as e:
                resp=str(e)
                is_error=True
            emit({"type": "tool_execution_end", "tool_call_id": tool_call.id, "tool_name": tool_name, "result":resp, "is_error": is_error})
            messages.append({"role":"tool","tool_call_id": tool_call.id,"content":resp})
        current_iteration+=1
    emit({"type": "agent_end", "messages": messages})
    return messages