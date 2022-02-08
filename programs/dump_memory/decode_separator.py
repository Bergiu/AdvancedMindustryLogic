from decode_memory_dump import decode_memory_dumps

inp1 = "¬xöJaaaa°RöJaaaa77öJaaaaq_öJaaaa(¢öJaaaaÜfüJaaaaiyüJaaaaKQüJaaaaE#üJaaaa5äüJaaaa3gÄJaaaa<yÄJaaaarPÄJaaaar8ÄJaaaaR#ÄJaaaa`äÄJaaaaÜ¢ÄJaaaakgÖJaaaaIyÖJaaaa)QÖJaaaa[7ÖJaaaaħ'ÖJaaaaEäÖJaaaa1¢ÖJaaaa.fÜJaaaa¼xÜJaaaaiQÜJaaaaU7ÜJaaaa?'ÜJaaaa€}ÜJaaaad¢ÜJaaaaIf€Jaaaa"
inp2 = "3x€Jaaaa>P€Jaaaaþ6€Jaaaa5]€Jaaaa<½€Jaaaa½d»Jaaaajw»Jaaaas6»JaaaaK+»Jaaaa$]»Jaaaaö½»Jaaaaæd«Jaaaaxw«JaaaaWO«Jaaaa·´«Jaaaa?]«JaaaaQ¼«Jaaaaje·JaaaaYw·Jaaaa§O·Jaaaaö5·Jaaaaы*·Jaaaa_{·Jaaaa3½·Jaaaa:d…Jaaaa2u…JaaaaßM…JaaaaV5…Jaaaa`*…Jaaaa·[…Jaaaas½…JaaaaJdøJaaaa"

example_data = decode_memory_dumps([inp1, inp2])


decoded = []

for x in example_data:
    filt = 2**52 - 4
    timestamp = x & filt
    timestamp = timestamp >> 2
    itemtype = x & 0b11
    decoded.append((itemtype, timestamp))


counted = []
counts = {}
for itemtype, timestamp in decoded:
    if itemtype in counts:
        counts[itemtype] += 1
    else:
        counts[itemtype] = 1
    counted.append((timestamp, counts[itemtype], itemtype))


print(counts)
