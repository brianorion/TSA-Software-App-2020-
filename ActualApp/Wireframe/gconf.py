from base64 import b64decode as nreji
from time import time
from json import loads as fie

a = int(time())

feirjafo = (((a * 4) - (a * (15 % 6))) ^ a) + (a * 23) - (a - 1) * 23

fas = "V2lzbsKbdMKOeW9pfnbCg3lywoDCosKSwpt6wpnCosKeZ8KKwoxmwobCmHp8wojCk3LCgcKOwqVywoTCiMKjenR7wqZ9wod5UmrCj3HCncKQwqB0wqFywpd5wqN+YMKIwpt3dsKAwqxnUW7CiXh3cltvfsKCXMKawpV5X2/CmX5mwoPCncKBUGx0cFN0wo50wp5wa3JgdG/Ch3hxeMKUwpp9d2fCkmnCim9VZcKPdFx5wpN3XXnCgX1gwoHCm3vCmsKjwohowovCjcKNwobCkHfCk8KJwpR3W8KFwqHCmWDCicKYf2XClsKgT8KMacKIwpnCjG3CmV9ZwoHCnntewo7CpHx3wpPCqHjCoMKAwollUm5UfHtxVlx/woPCnm1fwo/CocKFwp3ClcKewoXCi2rCi2p5e1Z2wpPCgMKddsKBdsKTenXCksKYccKawoHCnMKFdnnCkm95wodne1jCgcKQc13CjVx7wpx4wpfCqMKbfMKfZFFtU3t6cFVbfsKCwp1sXsKOwqDChMKcwpTCncKEworCgMKKaXh6VXXCkn/CnHXCgHXCknl0wpHCl3DCmcKAwpvChMKLcU9ueHzClF3CksKJwp5ybHPCnnXCgMKQwqV+wp5+wqnCoHV5wppnwo98wpBvfsKIwpVebcKFwpR7wph9wp1idcKXwql0dsKCwphbasKGwpHCgH/CgsKUW37ChsKmdGHClGHCjGXClsKYUHN6wpx1V3HCnMKWwqLCjMKhfXTCkcKdeXN6aHx3cnJ2d3zCnWrCkn/Cj3rCgcKDwpZ2cHfConnChMKUwqnCgsKLa8KXY3p8wpBzfsKAwpF/wpfCjsKcwofCm3vCm3dkwoBmd3ZsUVd6fsKZaFrCisKcwoDCmMKQwpnCgMKGfMKdfMKLwo1RccKOe8KYcXxxwo51cMKNwpNswpV8wpdjwofCksKaZGbCgGTCiGjChlRqwpJvwo7Cn8KSc1tkdMKSwqPCmMKGwpbCmXbCjMKBb8KFdnxWwohWdMKTwpFcf8KXwqHCg8KEYMKZeMKVfGBzdsKUwo57eGjCkn95XnjCgcKFY8KawoTCgcKac8KcwoPCh8KKeHtuwo9rwojCjnHCocKO"


config = nreji(fas.encode("utf-8")).decode("utf-8")

config = "".join(chr(ord(afew) - (bre % feirjafo) - (feirjafo + 7)) for bre, afew in enumerate(config))

config = "".join(ke for ke in reversed(config))
config = nreji(config.encode("utf-8")).decode("utf-8")
config = fie(config)