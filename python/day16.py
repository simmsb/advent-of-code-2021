from __future__ import annotations

from dataclasses import dataclass

import struct
import bitstring
from bitstring import BitArray



fmt = "uint:3, uint:3"

lit_fmt = "uint:5"

opthree_fmt = "bool, uint:11"

@dataclass
class Packet:
    version: int
    type: int
    value: int | None
    subpackets: list[Packet] | None

    def vsum(self):
        if self.value is not None:
            return self.version
        if self.subpackets is not None:
            return sum(p.vsum() for p in self.subpackets) + self.version
        raise Exception("oops")

    def eval(self):
        if self.value is not None:
            return self.value

        assert(self.subpackets is not None)

        if self.type == 0:
            return sum(p.eval() for p in self.subpackets)
        if self.type == 1:
            v = 1
            for p in self.subpackets:
                v *= p.eval()
            return v
        if self.type == 2:
            return min(p.eval() for p in self.subpackets)
        if self.type == 3:
            return max(p.eval() for p in self.subpackets)
        if self.type == 5:
            a, b = [p.eval() for p in self.subpackets]
            return int(a > b)
        if self.type == 6:
            a, b = [p.eval() for p in self.subpackets]
            return int(a < b)
        if self.type == 7:
            a, b = [p.eval() for p in self.subpackets]
            return int(a == b)

        raise Exception(f"No clue {self.version=}, {self.type=}, {self}")


def parse(pkt: BitArray):
    v, t = pkt.unpack(fmt)

    print(v, t, pkt.bin)
    pkt = pkt[6:]

    out = []

    if t == 4:
        n = 0
        plen = 0
        while True:
            print(f"chunk {pkt.bin=}")
            [x] = pkt.unpack("uint:5")
            pkt = pkt[5:]
            n |= x & 0b1111
            plen += 5
            if x & 0b10000:
                n <<= 4
            else:
                break
        # pkt = pkt[(16 - plen) % 16:]

        print(f"read lit, remaining = {pkt.bin=}, read {plen=}")

        return [Packet(v, t, n, None)], pkt
    else:
        [i] = pkt.unpack("bool")
        pkt = pkt[1:]

        print(i, pkt.bin)

        if not i:
            [ln] = pkt.unpack("uint:15")

            print(f"reading bit len pkts {ln}")

            pkt = pkt[15:]
            pkt_after = pkt[ln:]
            pkt = pkt[:ln]

            pkts = []

            while len(pkt) > 0:
                r, pkt = parse(pkt)
                pkts.extend(r)

            return [Packet(v, t, None, pkts)], pkt_after
        else:
            [ln] = pkt.unpack("uint:11")
            pkt = pkt[11:]

            print(f"reading given len pkts {ln}, {pkt.bin=}")

            pkts = []

            for _ in range(ln):
                r, pkt = parse(pkt)
                print("returned len", len(pkt))
                pkts.extend(r)

            return [Packet(v, t, None, pkts)], pkt

pkt = BitArray("0xE20D79005573F71DA0054E48527EF97D3004653BB1FC006867A8B1371AC49C801039171941340066E6B99A6A58B8110088BA008CE6F7893D4E6F7893DCDCFDB9D6CBC4026FE8026200DC7D84B1C00010A89507E3CCEE37B592014D3C01491B6697A83CB4F59E5E7FFA5CC66D4BC6F05D3004E6BB742B004E7E6B3375A46CF91D8C027911797589E17920F4009BE72DA8D2E4523DCEE86A8018C4AD3C7F2D2D02C5B9FF53366E3004658DB0012A963891D168801D08480485B005C0010A883116308002171AA24C679E0394EB898023331E60AB401294D98CA6CD8C01D9B349E0A99363003E655D40289CBDBB2F55D25E53ECAF14D9ABBB4CC726F038C011B0044401987D0BE0C00021B04E2546499DE824C015B004A7755B570013F2DD8627C65C02186F2996E9CCD04E5718C5CBCC016B004A4F61B27B0D9B8633F9344D57B0C1D3805537ADFA21F231C6EC9F3D3089FF7CD25E5941200C96801F191C77091238EE13A704A7CCC802B3B00567F192296259ABD9C400282915B9F6E98879823046C0010C626C966A19351EE27DE86C8E6968F2BE3D2008EE540FC01196989CD9410055725480D60025737BA1547D700727B9A89B444971830070401F8D70BA3B8803F16A3FC2D00043621C3B8A733C8BD880212BCDEE9D34929164D5CB08032594E5E1D25C0055E5B771E966783240220CD19E802E200F4588450BC401A8FB14E0A1805B36F3243B2833247536B70BDC00A60348880C7730039400B402A91009F650028C00E2020918077610021C00C1002D80512601188803B4000C148025010036727EE5AD6B445CC011E00B825E14F4BBF5F97853D2EFD6256F8FFE9F3B001420C01A88915E259002191EE2F4392004323E44A8B4C0069CEF34D304C001AB94379D149BD904507004A6D466B618402477802E200D47383719C0010F8A507A294CC9C90024A967C9995EE2933BA840")
# pkt = BitArray("0xA0016C880162017C3686B18A3D4780")
[ppkt], _ = parse(pkt)
print(ppkt)
print(ppkt.eval())
