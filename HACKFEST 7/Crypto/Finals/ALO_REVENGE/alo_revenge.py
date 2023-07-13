#!/usr/bin/env python3

"""

Author : msalaani
Task : ALO REVENGE - Challenge
Event : Hackfest 7 - Finals

"""

from Crypto.Util.number import *
from secret import *

nbits = 1024
p, q = [getPrime(nbits) for _  in "01"]

N = p * q
phi = (p - 1) * (q - 1)

while True:
    er = getRandomInteger(nbits // 4)
    r = getRandomInteger(nbits // 4)
    if GCD(er, phi) == 1 :
        dr = inverse(er, phi)
        d = dr + r
        if GCD(d, phi) == 1:
            e = inverse(d, phi)
            break

c = pow(bytes_to_long(flag), e, N)

print(f"{N = }")
print(f"{e = }")
print(f"{c = }")


"""
N = 17467481214893706686264907425568641024423948747329849803220540505711741882994201020419267334275928072135607770718575673054022667436927843534612869038355838282302932843012360269846075834519121085585237145107178495749549229011480099302592862529793499242171139861548764486647255246582991889917183532383901281037265354836389715598698732332650298802320298029920024169247746495789471074526414069145826312205525875992558293413995887407696433079706868923088705553097918630396795662265265029232705666774780685845058275972550787174550565076915144575888017217778363879229208396372829144741676068451625311492986985640257375317727
e = 11510661733340982733533878793120292586274701035726574023994365636079720367695755042806936494388202377353335952217812807329420830261126724301187782770267446596583293374843338814415278559221574584540406875244169151233672317813034143259437127161647942947923778947443773592665041961716793016435657059806554179659743488724617206754844439460403976741455327604855036565353239964435280266533191670611555079321938033966406987626990930623180865750218693144391340719359836202417105909484307998021800093724370797914473472568443918921602072272409292100254645798757930418474790800166734717350991663753306969381902753370423505662795
c = 10734148290191221466909514518368015114801896024316006882039213449697716902012731369475976955595544192543160485970461801112223741628024523764227256093949064484882036589333492155275749792296917971987499208569220668524514612519269610676725703663098152673966136668848958007640574259590090615824782894974145001462339082004683947411740391936961429745215620168352488881630461337238661672358179899120017564007954127116043695370634980013995177849609827571878196472113283293712103838219489455434085449869763535166995255883856737526145809741672872434202007584631509500242928075360153554270293981587343570857211929720743227816263
"""