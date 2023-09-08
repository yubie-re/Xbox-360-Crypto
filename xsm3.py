#!/usr/bin/env python3

from struct import pack_into, unpack_from

from XeCrypt import *

# References:
# https://github.com/oct0xor/xbox_security_method_3

SBOX = bytes([
	0xB0, 0x3D, 0x9B, 0x70, 0xF3, 0xC7, 0x80, 0x60,
	0x73, 0x9F, 0x6C, 0xC0, 0xF1, 0x3D, 0xBB, 0x40,
	0xB3, 0xC8, 0x37, 0x14, 0xDF, 0x49, 0xDA, 0xD4,
	0x48, 0x22, 0x78, 0x80, 0x6E, 0xCD, 0xE7, 0x00,
	0x81, 0x86, 0x68, 0xE1, 0x5D, 0x7C, 0x54, 0x2C,
	0x55, 0x7B, 0xEF, 0x48, 0x42, 0x7B, 0x3B, 0x68,
	0xE3, 0xDB, 0xAA, 0xC0, 0x0F, 0xA9, 0x96, 0x20,
	0x95, 0x05, 0x93, 0x94, 0x9A, 0xF6, 0xA3, 0x64,
	0x5D, 0xCC, 0x76, 0x00, 0xE5, 0x08, 0x19, 0xE8,
	0x8D, 0x29, 0xD7, 0x4C, 0x21, 0x91, 0x17, 0xF4,
	0xBC, 0x6A, 0xB3, 0x80, 0x83, 0xC6, 0xD4, 0x90,
	0x9B, 0xAE, 0x0E, 0xFE, 0x2E, 0x4A, 0xF2, 0x00,
	0x73, 0x88, 0xD9, 0x40, 0x66, 0xC5, 0xD4, 0x08,
	0x57, 0xB1, 0x89, 0x48, 0xDC, 0x54, 0xFC, 0x43,
	0x6A, 0x26, 0x87, 0xB8, 0x09, 0x5F, 0xCE, 0x80,
	0xE4, 0x0B, 0x05, 0x9C, 0x24, 0xF3, 0xDE, 0xE2,
	0x3E, 0xEC, 0x38, 0x8A, 0xA2, 0x55, 0xA4, 0x50,
	0x4E, 0x4B, 0xE9, 0x58, 0x7F, 0x9F, 0x7D, 0x80,
	0x23, 0x0C, 0x4D, 0x80, 0x05, 0x44, 0x26, 0xB8,
	0xE9, 0xD8, 0xBC, 0xE6, 0x76, 0x3A, 0x6E, 0xA4,
	0x19, 0xDE, 0xC2, 0xD0, 0xC4, 0xBC, 0xC3, 0x5C,
	0x59, 0xDF, 0x16, 0x46, 0x39, 0x70, 0xF4, 0xEE,
	0x2D, 0x58, 0x5A, 0xA8, 0x17, 0x86, 0x6B, 0x60,
	0x29, 0x58, 0x4D, 0xD2, 0x5F, 0x28, 0x7A, 0xD8,
	0x8E, 0x79, 0xEA, 0x82, 0x94, 0x33, 0x31, 0x81,
	0xD9, 0x22, 0xD5, 0x10, 0xDA, 0x92, 0xA0, 0x7D,
	0x3D, 0xDA, 0xAC, 0x1C, 0xA2, 0x53, 0x31, 0xB8,
	0x3C, 0x96, 0x52, 0x00, 0x82, 0x6B, 0x56, 0xA0,
	0xD3, 0xC2, 0x40, 0xC7, 0x1B, 0x7F, 0xDC, 0x01,
	0x72, 0x70, 0xB1, 0x8C, 0x01, 0x09, 0x09, 0x36,
	0xFC, 0x97, 0xEA, 0xDE, 0xE3, 0x0D, 0xAE, 0x7E,
	0xE3, 0x0D, 0xAE, 0x7E, 0x33, 0x69, 0x80, 0x40
])

UsbdSecPlainTextData = bytes([
	0xD1, 0xD2, 0xF2, 0x80, 0x6E, 0xBA, 0x0C, 0xC0,
	0xB6, 0xC4, 0xC9, 0xD8, 0x61, 0x75, 0x1D, 0x1A,
	0x3F, 0x95, 0x58, 0xBE, 0xD8, 0x0D, 0xE2, 0xC0,
	0xD0, 0x21, 0x79, 0x20, 0x65, 0x2D, 0x99, 0x40,
	0x3C, 0x96, 0x52, 0x00, 0x1B, 0x7F, 0xDC, 0x01,
	0x82, 0x1C, 0x13, 0xD8, 0x33, 0x69, 0x80, 0x40,
	0xFC, 0x97, 0xEA, 0xDE, 0x08, 0xEA, 0x14, 0xDC,
	0xEB, 0x0F, 0x6A, 0x18, 0x6F, 0x78, 0x2C, 0xB0,
	0xD3, 0xC2, 0x40, 0xC7, 0x82, 0x6B, 0x56, 0xA0,
	0x19, 0x09, 0x36, 0xE0, 0x72, 0x70, 0xB1, 0x8C,
	0xE3, 0x0D, 0xAE, 0x7E, 0x50, 0xA5, 0x2B, 0xE2,
	0xC9, 0xAF, 0xC7, 0x70, 0x1C, 0x29, 0x80, 0x56,
	0x24, 0xF0, 0x66, 0xFA, 0x02, 0x2B, 0x58, 0x98,
	0x8F, 0xE4, 0xD1, 0x3C, 0x6E, 0x38, 0x2A, 0xFF,
	0xB8, 0xFA, 0x35, 0xB0, 0x52, 0x49, 0xC5, 0xB4,
	0x66, 0xFA, 0x47, 0x55, 0x6C, 0x8D, 0x40, 0x08
])

UsbdSecXSM3GetIdentificationProtocolData = bytes([
	0x49, 0x4B, 0x00, 0x00, 0x17, 0x04, 0xE1, 0x11,
	0x54, 0x15, 0xED, 0x88, 0x55, 0x21, 0x01, 0x33,
	0x00, 0x00, 0x80, 0x02, 0x5E, 0x04, 0x8E, 0x02,
	0x03, 0x00, 0x01, 0x01, 0xC1
])

UsbdSecXSM3SetChallengeProtocolData = bytes([
	0x09, 0x40, 0x00, 0x00, 0x1C, 0x0A, 0x0F, 0x6B,
	0x0B, 0xA1, 0x18, 0x26, 0x5F, 0x83, 0x3C, 0x45,
	0x13, 0x49, 0x53, 0xBD, 0x18, 0x61, 0x73, 0xCF,
	0x29, 0xDE, 0x2C, 0xD8, 0x66, 0xE4, 0xAE, 0x34,
	0xA9, 0x9C
])

UsbdSecXSM3GetResponseChallengeProtocolData = bytes([
	0x49, 0x4C, 0x00, 0x00, 0x28, 0x81, 0xBD, 0x7C,
	0xB3, 0x70, 0xBD, 0x76, 0x1A, 0x2F, 0x28, 0x6E,
	0xD1, 0xF2, 0xC3, 0x8E, 0xF9, 0x0B, 0xB2, 0x83,
	0x49, 0xCB, 0x4B, 0x24, 0xA2, 0x90, 0x6C, 0x27,
	0xB1, 0x05, 0x0A, 0xB0, 0x47, 0x09, 0x75, 0x16,
	0x07, 0xE1, 0xD7, 0xE8, 0xAF, 0x57
])

UsbdSecXSM3SetVerifyProtocolData1 = bytes([
	0x09, 0x41, 0x00, 0x00, 0x10, 0x5A, 0xDD, 0x1B,
	0xA0, 0x74, 0x87, 0xB7, 0x62, 0xB7, 0xA5, 0x8F,
	0x34, 0xFF, 0xE3, 0xD1, 0xD9, 0xA7
])

UsbdSecXSM3GetResponseVerifyProtocolData1 = bytes([
	0x49, 0x4C, 0x00, 0x00, 0x10, 0x5A, 0x9C, 0xD6,
	0x72, 0xB3, 0x70, 0x8D, 0xA7, 0x57, 0x01, 0x06,
	0x50, 0x20, 0x60, 0xA9, 0xBC, 0xDE
])

kv_key_1 = bytes([
	0xF1, 0x9D, 0x6F, 0x2C, 0xB1, 0xEE, 0x6A, 0xC4,
	0x63, 0x53, 0x36, 0xA5, 0x4C, 0x11, 0x00, 0x7D
])

kv_key_2 = bytes([
	0xC4, 0x55, 0x82, 0xC8, 0x9F, 0xC3, 0xDA, 0xD2,
	0x8C, 0x1F, 0xBB, 0xCF, 0x3D, 0x04, 0x9B, 0x6F
])

def cksum(cmd: bytes | bytearray) -> int:
	size = cmd[4]
	csum = 0
	for i in range(size):
		csum ^= cmd[i + 5]
	if csum != cmd[size + 5]:
		return -1
	return 0

def UsbdSecGetIdentificationComplete(data: bytes | bytearray) -> bytes:
	proto_data = bytearray(0x20)
	proto_data[:0xF] = data[5:5 + 0xF]
	(v0, v1, v2, v4, v3) = unpack_from(">2HBHB", data, 5 + 0xF)
	pack_into(">2H2BH", proto_data, 0x10, v0, v1, v2, v3, v4)
	return proto_data

def UsbdSecXSM3AuthenticationCrypt(key: bytes | bytearray, data: bytes | bytearray, mode: int) -> bytes:
	c = XeCryptDes3((key * 2)[:0x18], XeCryptDes3.MODE_CBC, bytes(8))
	if mode == 1:
		return c.encrypt(data)
	else:
		return c.decrypt(data)

def UsbdSecXSM3AuthenticationMac(key: bytes | bytearray, salt: bytes | bytearray | None, data: bytes | bytearray, mode: int) -> tuple[bytes, bytes]:
	temp = bytearray(8)
	if mode:
		e = XeCryptDes(key[:8])
		d = XeCryptDes(key[8:8 + 8])
		if salt:
			v0 = int.from_bytes(salt, "big", signed=False)
			v0 += 1
			salt = v0.to_bytes(8, "big", signed=False)
			temp = e.encrypt(salt)

	if len(data) >= 8:
		for i in range(0, len(data), 8):
			v0 = int.from_bytes(temp, "big", signed=False)
			v1 = int.from_bytes(data[i:i + 8], "big", signed=False)
			temp = (v0 ^ v1).to_bytes(8, "big", signed=False)

			if mode:
				temp = e.encrypt(temp)
			else:
				temp = XeCryptDes(key[:8]).encrypt(temp)

	temp = bytearray(temp)
	temp[0] ^= 0x80

	if mode:
		temp = e.encrypt(temp)
		temp = d.decrypt(temp)
		output = e.encrypt(temp)
	else:
		output = XeCryptDes3((key * 2)[:0x18], XeCryptDes3.MODE_CBC, bytes(8)).encrypt(temp)
	return (salt, output)

def UsbdSecXSMAuthenticationAcr(key: bytes | bytearray, cert: bytes | bytearray, data: bytes | bytearray) -> bytes:
	block = data[:4] + cert[:4]

	iv = XeCryptParveEcb(key, SBOX, data[0x10:])
	cd = XeCryptParveEcb(key, SBOX, block)
	ab = XeCryptParveCbcMac(key, SBOX, iv, UsbdSecPlainTextData[:0x80])
	output = XeCryptChainAndSumMac(cd, ab, UsbdSecPlainTextData[:0x80])

	v0 = int.from_bytes(output, "big", signed=False)
	v1 = int.from_bytes(ab, "big", signed=False)
	output = (v0 ^ v1).to_bytes(8, "big", signed=False)

	return output

def main() -> int:
	kv = XECRYPT_KEYVAULT.from_buffer_copy(read_file("KV/banned.bin"))

	k1 = bytes(kv.global_dev_2des_key_1)
	k2 = bytes(kv.global_dev_2des_key_2)

	print("UsbdSecXSM3GetIdentificationProtocolData")

	if cksum(UsbdSecXSM3GetIdentificationProtocolData):
		return -1

	proto_data = UsbdSecGetIdentificationComplete(UsbdSecXSM3GetIdentificationProtocolData)

	print("UsbdSecXSM3AuthenticationChallenge")

	if cksum(UsbdSecXSM3SetChallengeProtocolData):
		return -1

	dec_data = UsbdSecXSM3AuthenticationCrypt(k1, UsbdSecXSM3SetChallengeProtocolData[5:5 + 0x18], 0)

	# random = bytearray(0x10)
	random = bytearray(dec_data[:0x10])

	# random_0 = dec_data[:0x10]
	cert = dec_data[0x10:0x10 + 8]
	mac_copy = UsbdSecXSM3SetChallengeProtocolData[29:29 + 4]

	random_enc = UsbdSecXSM3AuthenticationCrypt(kv_key_1, random, 1)

	random_swap = random[8:8 + 8] + random[:8]

	random_swap_enc = UsbdSecXSM3AuthenticationCrypt(kv_key_2, random_swap, 1)

	(salt, mac) = UsbdSecXSM3AuthenticationMac(k2, None, UsbdSecXSM3SetChallengeProtocolData[5:5 + 0x18], 0)

	if mac[4:] != mac_copy:
		print("MAC is wrong!")
		return -1

	print("UsbdSecXSM3GetResponseChallengeProtocolData")

	if cksum(UsbdSecXSM3GetResponseChallengeProtocolData):
		return -1

	dec_data = UsbdSecXSM3AuthenticationCrypt(random_enc, UsbdSecXSM3GetResponseChallengeProtocolData[5:5 + 0x20], 0)

	usb_random = dec_data[:0x10]
	rnd = dec_data[0x10:0x10 + 0x10]
	acr_copy = UsbdSecXSM3GetResponseChallengeProtocolData[37:37 + 8]

	(salt, mac) = UsbdSecXSM3AuthenticationMac(random_swap_enc, None, UsbdSecXSM3GetResponseChallengeProtocolData[5:5 + 0x20], 1)

	acr = UsbdSecXSMAuthenticationAcr(mac, cert, proto_data)

	if random != rnd:
		print("Random is wrong!")
		return -1

	if acr != acr_copy:
		print("ACR is wrong!")
		return -1

	usb_cmd_hash = XeCryptSha(dec_data[:0x20])

	pack_into("4s4s", random, 0, usb_random[0xC:0xC + 4], random[0xC:0xC + 4])

	print("UsbdSecXSM3SetVerifyProtocolData1")

	if cksum(UsbdSecXSM3SetVerifyProtocolData1):
		return -1

	dec_data = UsbdSecXSM3AuthenticationCrypt(usb_random, UsbdSecXSM3SetVerifyProtocolData1[5:5 + 8], 0)

	pack_into("8s", random, 8, dec_data[:8])

	mac_copy = UsbdSecXSM3SetVerifyProtocolData1[5 + 8:5 + 8 + 8]

	(salt, mac) = UsbdSecXSM3AuthenticationMac(usb_cmd_hash, random[:8], UsbdSecXSM3SetVerifyProtocolData1[5:5 + 8], 1)
	random[:8] = salt

	if mac != mac_copy:
		print("MAC is wrong!")
		return -1

	print("UsbdSecXSM3GetResponseVerifyProtocolData1")

	if cksum(UsbdSecXSM3GetResponseVerifyProtocolData1):
		return -1

	dec_data = UsbdSecXSM3AuthenticationCrypt(random_enc, UsbdSecXSM3GetResponseVerifyProtocolData1[5:5 + 8], 0)

	acr_copy = dec_data[:8]
	mac_copy = UsbdSecXSM3GetResponseVerifyProtocolData1[5 + 8:5 + 8 + 8]

	(salt, mac) = UsbdSecXSM3AuthenticationMac(random_swap_enc, random[:8], UsbdSecXSM3GetResponseVerifyProtocolData1[5:5 + 8], 1)
	random[:8] = salt

	acr = UsbdSecXSMAuthenticationAcr(random[8:8 + 8], cert, proto_data)

	if mac != mac_copy:
		print("MAC is wrong!")
		return -1

	if acr != acr_copy:
		print("ACR is wrong!")
		return -1

	return 0

if __name__ == "__main__":
	exit(main())