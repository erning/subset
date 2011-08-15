# -*- coding: utf-8 -*-
import subset
import zmq
import msgpack
import time
import os
import sys

VERSION=r'APS10'

socket = None

def loop():
    process_heartbeat()

    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    while True:
        events = poller.poll(1000)
        if os.getppid() == 1:
            break

        if events:
            process_request()
        else:
            process_heartbeat()

def process_request():
    frames = socket.recv_multipart()
    i = frames.index('', 1)

    sequence, timestamp, expiry = msgpack.unpackb(frames[i+1])
    method = frames[i+2]
    a, b = msgpack.unpackb(frames[i+3])

    ret = subset.is_subset(a, b)
    frames = frames[:i+1]
    now = int(round(time.time() * 1000))
    frames.append(msgpack.packb([sequence, now, 200]))
    frames.append(msgpack.packb(ret))

    socket.send_multipart(frames)
    

def process_heartbeat():
    now = int(round(time.time() * 1000))
    socket.send_multipart(['', VERSION, '\x01', msgpack.packb(now)])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        endpoint = 'ipc:///tmp/gsd-{0}.ipc'.format(os.getppid())
    else:
        endpoint = sys.argv[1]

    socket = zmq.Socket(zmq.Context.instance(), zmq.XREQ)
    socket.setsockopt(zmq.LINGER, 0)
    socket.setsockopt(zmq.IDENTITY, str(os.getpid()))
    socket.connect(endpoint)

    print "Running..."
    loop()

