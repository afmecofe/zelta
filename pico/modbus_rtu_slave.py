"""
Modbus RTU Slave — Raspberry Pi Pico (MicroPython)
===================================================
Runs on the Pico's USB CDC port (/dev/ttyACM0 on Linux).
Copy this file to the Pico as main.py, then reset.

  mpremote cp modbus_rtu_slave.py :main.py + reset

Supports:
  FC01  Read Coils           (addresses 0-63)
  FC03  Read Holding Regs    (addresses 0-63)

Default device address: 1
Default baud rate: 9600 (the USB CDC ignores baud, but set the same
  in the extension so the CRC is the only check that matters)

Extension settings:
  Baud rate:     9600
  Device addr:   1
  Start address: 0
  Count:         10
"""

import sys
import select

DEVICE_ADDR = 1

# ── Demo data ──────────────────────────────────────────────────────────────────
# 64 holding registers: 100, 110, 120, … (address × 10 + 100)
HOLDING_REGS = [100 + i * 10 for i in range(64)]

# 64 coils: alternating 0/1
COILS = [i % 2 for i in range(64)]


# ── CRC-16/Modbus ──────────────────────────────────────────────────────────────
def crc16(data: bytes | bytearray) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc


def append_crc(data: bytearray) -> bytes:
    c = crc16(data)
    return bytes(data) + bytes([c & 0xFF, c >> 8])


# ── Response builders ──────────────────────────────────────────────────────────
def exception_response(addr: int, fc: int, code: int) -> bytes:
    body = bytearray([addr, fc | 0x80, code])
    return append_crc(body)


def fc03_response(addr: int, start: int, count: int) -> bytes:
    if count < 1 or count > 125:
        return exception_response(addr, 3, 3)  # Illegal data value
    byte_count = count * 2
    body = bytearray([addr, 3, byte_count])
    for i in range(count):
        idx = start + i
        val = HOLDING_REGS[idx] if 0 <= idx < len(HOLDING_REGS) else 0
        body.append(val >> 8)
        body.append(val & 0xFF)
    return append_crc(body)


def fc01_response(addr: int, start: int, count: int) -> bytes:
    if count < 1 or count > 2000:
        return exception_response(addr, 1, 3)  # Illegal data value
    byte_count = (count + 7) // 8
    body = bytearray([addr, 1, byte_count])
    for i in range(byte_count):
        byte_val = 0
        for bit in range(8):
            idx = start + i * 8 + bit
            if 0 <= idx < len(COILS) and COILS[idx]:
                byte_val |= 1 << bit
        body.append(byte_val)
    return append_crc(body)


# ── Frame dispatcher ───────────────────────────────────────────────────────────
def handle_frame(frame: bytes):
    """
    Validate and dispatch an 8-byte RTU read-request frame.
    Returns response bytes, or None if the frame should be ignored.
    """
    if len(frame) < 8:
        return None

    addr = frame[0]
    fc   = frame[1]

    # Not addressed to us
    if addr != DEVICE_ADDR:
        return None

    # Validate CRC (last 2 bytes, little-endian)
    crc_recv = frame[6] | (frame[7] << 8)
    if crc16(frame[:6]) != crc_recv:
        return None

    start = (frame[2] << 8) | frame[3]
    count = (frame[4] << 8) | frame[5]

    if fc == 3:
        return fc03_response(addr, start, count)
    elif fc == 1:
        return fc01_response(addr, start, count)
    else:
        return exception_response(addr, fc, 1)  # Illegal function


# ── Main loop ──────────────────────────────────────────────────────────────────
buf = bytearray()

import time
time.sleep_ms(200)  # Let USB CDC settle after boot

poller = select.poll()
poller.register(sys.stdin, select.POLLIN)

# Flush any bytes already in stdin (e.g. REPL boot echo)
while poller.poll(0):
    sys.stdin.buffer.read(1)

while True:
    events = poller.poll(10)  # 10 ms poll interval
    if not events:
        continue

    b = sys.stdin.buffer.read(1)
    if not b:
        continue

    buf += b

    # All FC01/FC03 read requests are exactly 8 bytes
    while len(buf) >= 8:
        resp = handle_frame(bytes(buf[:8]))
        buf = buf[8:] if resp is not None else buf[1:]

        if resp is not None:
            sys.stdout.buffer.write(resp)
            sys.stdout.flush()
            break  # One request at a time
