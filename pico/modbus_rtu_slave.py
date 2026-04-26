"""
Modbus RTU Slave — Raspberry Pi Pico (MicroPython)
===================================================
Works on any MicroPython firmware version (no 3.10+ syntax).

Flash:  mpremote connect /dev/ttyACM0 cp modbus_rtu_slave.py :main.py + reset

Supports FC01, FC03 (read) and FC05, FC06, FC15, FC16 (write).
Writes update the in-memory tables — a subsequent read reflects the change.

Extension settings: Baud 9600 · Unit ID 1 · Start 0 · Count 10
"""

import sys
import uos
import time
import machine

_vcp = machine.USB_VCP()
uos.dupterm(None, 1)   # Detach REPL from USB CDC — pure binary pipe, no echo, no prompt

DEVICE_ADDR   = 1
HOLDING_REGS  = [100 + i * 10 for i in range(64)]   # r/w
COILS         = [i % 2         for i in range(64)]   # r/w


# ── CRC-16/Modbus ──────────────────────────────────────────────────────────────
def crc16(data):
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc


def append_crc(body):
    c = crc16(body)
    return bytes(body) + bytes([c & 0xFF, c >> 8])


# ── Exception ──────────────────────────────────────────────────────────────────
def exception_response(addr, fc, code):
    return append_crc(bytearray([addr, fc | 0x80, code]))


# ── Read responses ─────────────────────────────────────────────────────────────
def fc03_response(addr, start, count):
    if count < 1 or count > 125:
        return exception_response(addr, 3, 3)
    body = bytearray([addr, 3, count * 2])
    for i in range(count):
        idx = start + i
        v = HOLDING_REGS[idx] if 0 <= idx < len(HOLDING_REGS) else 0
        body.append(v >> 8)
        body.append(v & 0xFF)
    return append_crc(body)


def fc01_response(addr, start, count):
    if count < 1 or count > 2000:
        return exception_response(addr, 1, 3)
    byte_count = (count + 7) // 8
    body = bytearray([addr, 1, byte_count])
    for i in range(byte_count):
        byte_val = 0
        for bit in range(8):
            idx = start + i * 8 + bit
            if 0 <= idx < len(COILS) and COILS[idx]:
                byte_val |= (1 << bit)
        body.append(byte_val)
    return append_crc(body)


# ── Frame dispatcher ───────────────────────────────────────────────────────────
def handle_frame(frame):
    if len(frame) < 8:
        return None

    addr = frame[0]
    fc   = frame[1]

    if addr != DEVICE_ADDR:
        return None

    # CRC check — over all bytes except the last two
    crc_recv = frame[-2] | (frame[-1] << 8)
    if crc16(frame[:-2]) != crc_recv:
        return None

    start = (frame[2] << 8) | frame[3]

    if fc == 3:
        return fc03_response(addr, start, (frame[4] << 8) | frame[5])

    elif fc == 1:
        return fc01_response(addr, start, (frame[4] << 8) | frame[5])

    elif fc == 5:
        if 0 <= start < len(COILS):
            COILS[start] = 1 if frame[4] == 0xFF else 0
        # Echo request as response (built fresh to avoid dupterm byte corruption)
        return append_crc(bytearray([addr, 0x05, frame[2], frame[3], frame[4], frame[5]]))

    elif fc == 6:
        v = (frame[4] << 8) | frame[5]
        if 0 <= start < len(HOLDING_REGS):
            HOLDING_REGS[start] = v
        # Echo request as response (built fresh to avoid dupterm byte corruption)
        return append_crc(bytearray([addr, 0x06, frame[2], frame[3], frame[4], frame[5]]))

    elif fc == 0x0F:
        count      = (frame[4] << 8) | frame[5]
        byte_count = frame[6]
        for i in range(count):
            bidx = i // 8
            if bidx < byte_count and 0 <= start + i < len(COILS):
                COILS[start + i] = (frame[7 + bidx] >> (i % 8)) & 1
        return append_crc(bytearray([addr, 0x0F, frame[2], frame[3], frame[4], frame[5]]))

    elif fc == 0x10:
        count = (frame[4] << 8) | frame[5]
        for i in range(count):
            if 0 <= start + i < len(HOLDING_REGS):
                HOLDING_REGS[start + i] = (frame[7 + i * 2] << 8) | frame[8 + i * 2]
        return append_crc(bytearray([addr, 0x10, frame[2], frame[3], frame[4], frame[5]]))

    else:
        return exception_response(addr, fc, 1)


# ── Main loop ─────────────────────────────────────────────────────────────────
import micropython
micropython.kbd_intr(-1)   # Disable Ctrl+C so 0x03 (FC03) doesn't kill the script

time.sleep_ms(500)         # let USB CDC settle after boot / soft-reset
_vcp.read(256)             # drain any buffered bytes (REPL banner etc.)

buf = bytearray()

while True:
    b = _vcp.recv(1, timeout=10000)   # BLOCKING — waits up to 10s for a byte
    if not b:
        continue

    buf.extend(b)

    # Dispatch when we have a complete frame
    while len(buf) >= 2:
        fc = buf[1]

        if fc in (0x01, 0x03, 0x05, 0x06):
            if len(buf) < 8:
                break
            frame    = bytes(buf[:8])
            consumed = 8

        elif fc in (0x0F, 0x10):
            if len(buf) < 7:
                break
            total = 9 + buf[6]
            if len(buf) < total:
                break
            frame    = bytes(buf[:total])
            consumed = total

        else:
            buf = buf[1:]
            continue

        resp = handle_frame(frame)
        buf  = buf[consumed:] if resp is not None else buf[1:]

        if resp is not None:
            _vcp.write(resp)
            sys.stdout.flush()
            break
