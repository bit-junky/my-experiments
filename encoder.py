# python file encoder
# 20200429 mbr

def encode(buf):
	res = []
	h = 0
	for i in range(len(buf)):
		h = (h << 8) | buf[i]
		if i%6 == 5:
			res.append(h)
			h = 0
	if len(buf)%6 != 0:
		h = h << (8*(6-(len(buf)%6)))
		res.append(h)
	return { "entries": len(buf), "series": res }

def decode(d):
	res = bytes()
	for x in d["series"]:
		res.append((x>>40)&255)
		res.append((x>>32)&255)
		res.append((x>>24)&255)
		res.append((x>>16)&255)
		res.append((x>>8)&255)
		res.append(x&255)
	return res[:d["entries"]]

import sys
import json

if len(sys.argv) == 4:
	if sys.argv[1] == "encode":
		with open(sys.argv[2], "rb") as infile:
			buf = infile.read()
		with open(sys.argv[3], "w") as outfile:
			outfile.write(json.dumps( { "header": "mbot 0.91", "owner": "mbr", "date": 20200429, "data": encode(buf[::-1]) } ))
	elif sys.argv[1] == "decode":
		with open(sys.argv[2], "r") as infile:
			data = json.loads(infile.read())
		with open(sys.argv[3], "wb") as outfile:
			outfile.write(decode(data["data"])[::-1])
	else:
		print("invalid command")
else:
	print("usage: {} encode|decode src dest".format(sys.argv[0]))
