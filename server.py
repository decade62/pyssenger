import asyncio
import keyboard


BUDDY = input('Provide a username for the remote chat user: ')
incoming = ""

def key_press(key):
    if len(key.name) == 1:
        print(key.name, end="", flush=True)
    elif key.name == 'space':
        print(' ', end="", flush=True)
    elif key.name == 'backspace':
        print('\b', end="", flush=True)
    elif key.name =='enter':
        print('\n', end="", flush=True)

keyboard.on_press(key_press)

async def get(reader, writer):
    global incoming
    while True:
        data = await reader.read(100)
        incoming = data.decode()
        #addr = writer.get_extra_info('peername')
        #print("Received %r from %r" % (incoming, addr))
        print(' '+BUDDY, " - ", incoming)
    
async def put(writer):
    while True:
        message = " ".join(keyboard.get_typed_strings(keyboard.record('\n')))
        if len(message) > 1:
            #print("Send: %r" % message)
            writer.write(message.encode())
            await writer.drain()
        message = ""
        await asyncio.sleep(1)

async def handle_echo(reader, writer):
    await asyncio.gather(get(reader, writer), put(writer))
    print("Close the client socket")
    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '', 2410, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()