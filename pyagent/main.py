import loop 


# print the events

def print_event(event):
    kind=event["type"]
    if kind == "tool_execution_start":
        print(f"[tool] {event['tool_name']}({event['args']})")

    elif kind == "tool_execution_end":
        status = "ERROR" if event["is_error"] else "ok"
        result = str(event["result"])
        if len(result) > 300:
            result = result[:300] + "...(truncated)"
        print(f"[tool result: {status}] {result}")

    elif kind == "assistant_message":
        content = event["message"].get("content")
        if content:
            print(content)

message=None
while True:
    prompt=input("> ")
    message=loop.run(prompt,message,emit=print_event)


