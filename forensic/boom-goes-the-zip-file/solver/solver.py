

from subprocess import Popen
import time

buf = b""
ans = ''

class BitBuffer:
    def __init__(self):
        self.done = []
        self.current = 0
        self.bit_pos = 0

    def push(self, x, n):
        assert x == x % (1<<n), (bin(x), n)
        while n >= (8 - self.bit_pos):
            self.current |= (x << self.bit_pos) & 0xff
            x >>= (8 - self.bit_pos)
            n -= (8 - self.bit_pos)
            self.done.append(self.current)
            self.current = 0
            self.bit_pos = 0
        self.current |= (x << self.bit_pos) & 0xff
        self.bit_pos += n

    def push_rev(self, x, n):
        mask = (1<<n)>>1
        while mask > 0:
            self.push(x&mask != 0 and 1 or 0, 1)
            mask >>= 1

    def bytes(self):
        out = bytes(self.done)
        if self.bit_pos != 0:
            out += bytes([self.current])
        return out

for i in range(1, 46):
	f = open(f"zipbombs/{i}.zip", "rb")
	buf = f.read(2)
	while(buf != b"\xec\xc0"):
		buf = buf[1:] + f.read(1)
	while(buf != b"\xe0\x76"):
		buf = buf[1:] + f.read(1)
	buf = buf + f.read()
	f.close()
	buf = buf[:buf.index(b"PK")]
	real_last_deflate_block = BitBuffer()
	real_last_deflate_block.push(1, 1)
	for i in buf[1:]:
		real_last_deflate_block.push(i, 8)
	with open('temp', "wb") as f:
		f.write(real_last_deflate_block.bytes())
	Popen(['node', 'inflate.js']).wait()
	with open('ans', 'r') as f:
		ans += f.read().strip('\x00')[0]
	print(ans)

print(ans)