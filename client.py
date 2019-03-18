import asyncio
import keyboard

message = ' '
HOST = input('Provide IP address: ')
BUDDY = input('Provide a username for the remote chat user: ')

reader = None
writer = None

def key_press(key):
    if len(key.name) == 1:
        print(key.name, end="", flush=True)
    elif key.name == 'space':
        print(' ', end="", flush=True)
    elif key.name == 'backspace':
        print('\b', end="", flush=True)
    #elif key.name =='enter':
    #    print('\n')
    

keyboard.on_press(key_press)

async def msg_type():
        global message, writer
        while True:
            message = " ".join(keyboard.get_typed_strings(keyboard.record('\n')))
            if len(message) > 1:    #use "enter" to pass execution to sRead
                writer.write(message.encode())
            await asyncio.sleep(1)
            message = ''

async def sRead():
        global reader
        while True:
            #await asyncio.sleep(2)
            data = await reader.read(100)
            #if(type(data) is str):
            print('\n ' + BUDDY + ' - %r' % data.decode())

async def tcp_echo_client():
    global reader, writer
    reader, writer = await asyncio.open_connection(HOST, 2410)
    try:
        
        await asyncio.gather(sRead(), msg_type())
    except KeyboardInterrupt:
        pass
    finally:
        print('Closing the socket...')
        writer.close()


asyncio.run(tcp_echo_client())
