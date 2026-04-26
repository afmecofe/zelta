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
    Validate and dispatch an RTU frame.
    Fixed-length (8 bytes): FC01, FC03, FC05, FC06.
    Variable-length:        FC15, FC16 (caller passes full frame).
    Returns response bytes, or None if the frame should be ignored.
    """
    if len(frame) < 8:
        return None

    addr = frame[0]
    fc   = frame[1]

    # Not addressed to us
    if addr != DEVICE_ADDR:
        return None

    # Validate CRC (last 2 bytes, little-endian, over all preceding bytes)
    crc_recv = frame[-2] | (frame[-1] << 8)
    if crc16(frame[:-2]) != crc_recv:
        return None

    start = (frame[2] << 8) | frame[3]

    # ── Read functions ─────────────────────────────────────────────
    if fc == 3:
        count = (frame[4] << 8) | frame[5]
        return fc03_response(addr, start, count)
    elif fc == 1:
        count = (frame[4] << 8) | frame[5]
        return fc01_response(addr, start, count)

    # ── Write single coil (FC05) ───────────────────────────────────
    elif fc == 5:
        val_on = frame[4] == 0xFF  # 0xFF00 = ON, 0x0000 = OFF
        if 0 <= start < len(COILS):
            COILS[start] = 1 if val_on else 0
        return bytes(frame)  # Echo request

    # ── Write single register (FC06) ─────────────────────────────
    elif fc == 6:
        value = (frame[4] << 8) | frame[5]
        if 0 <= start < len(HOLDING_REGS):
            HOLDING_REGS[start] = value
        return bytes(frame)  # Echo request

    # ── Write multiple coils (FC15 = 0x0F) ──────────────────────
    elif fc == 0x0F:
        count      = (frame[4] << 8) | frame[5]
        byte_count = frame[6]
        for i in range(count):
            byte_idx = i // 8
            bit_idx  = i % 8
            if byte_idx < byte_count and 0 <= start + i < len(COILS):
                COILS[start + i] = (frame[7 + byte_idx] >> bit_idx) & 1
        body = bytearray([addr, 0x0F, frame[2], frame[3], frame[4], frame[5]])
        return append_crc(body)

    # ── Write multiple registers (FC16 = 0x10) ──────────────────
    elif fc == 0x10:
        count = (frame[4] << 8) | frame[5]
        for i in range(count):
            if 0 <= start + i < len(HOLDING_REGS):
                HOLDING_REGS[start + i] = (frame[7 + i * 2] << 8) | frame[8 + i * 2]
        body = bytearray([addr, 0x10, frame[2], frame[3], frame[4], frame[5]])
        return append_crc(body)

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

    # Dispatch once we have enough bytes for the current FC
    while len(buf) >= 2:
        fc = buf[1]
        if fc in (0x01, 0x03, 0x05, 0x06):
            # Fixed 8-byte frame
            if len(buf) < 8:
                break
            resp = handle_frame(bytes(buf[:8]))
            buf = buf[8:] if resp is not None else buf[1:]
        elif fc in (0x0F, 0x10):
            # Variable-length: need 7+ bytes to read byte_count
            if len(buf) < 7:
                break
            total = 9 + buf[6]  # header(7) + data(byte_count) + crc(2)
            if len(buf) < total:
                break
            resp = handle_frame(bytes(buf[:total]))
            buf = buf[total:] if resp is not None else buf[1:]
        else:
            buf = buf[1:]
            continue

        if resp is not None:
            sys.stdout.buffer.write(resp)
            sys.stdout.flush()
            break  # One request at a time
