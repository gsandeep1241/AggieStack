while True:
    cmd = raw_input('Enter your command: ')
    cmd_parts = cmd.split(" ")
    
    if cmd_parts[0] == "quit":
        print("Goodbye!")
        break;