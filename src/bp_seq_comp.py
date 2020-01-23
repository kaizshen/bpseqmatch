#base_pair comparison
#11/29/2019 v1 => issue with speed

def read_parse (text_fl, bp_length):
    with open(text_fl,"r") as fp:
        for cnt, line in enumerate(fp):
            if cnt == 2:
                seq_string = line

    bp_seqList = []
    for i in range( len(seq_string) - (bp_length-1) ):
        bp_tuple = (i, seq_string[i:i+bp_length])
        bp_seqList.append(bp_tuple)

    return bp_seqList

def bpSeq_comp (sp_diff, bp_seqList):
    bpSeq_matchList = []
    i = 0
    comp_checkList = []
    for seq in bp_seqList:
        compSeq = seq
        compSeqList = [seq]
        comp_check = False
        if (compSeq[1] in comp_checkList):
            continue
        for seq_2 in bp_seqList[i+sp_diff:]:
            if compSeq[1] == seq_2[1] and (seq_2[0]-compSeq[0]) >= sp_diff:
                comp_check = True
                compSeqList.append(seq_2)
                compSeq = seq_2
        if comp_check == True:
            bpSeq_matchList.append(compSeqList)
            comp_checkList.append(compSeq[1])    
        i = i+1
    return bpSeq_matchList

def write_file (outp_file, min_match, bpSeq_matchList):
    with open(outp_file, 'w+') as fp:
        counter = 0
        for elm in bpSeq_matchList:
            if len(elm) < min_match:
                continue
            fp.write(elm[0][1] + ': %d' % len(elm) + ' matches; Starting positions: ')
            fp.write(' '.join('%s' % x[0] for x in elm))
            fp.write('\n')
            counter = counter + 1
        fp.seek(0)
        content = fp.read()
        fp.seek(0)
        fp.write('Total matched sequences: %d' % counter + '\n\n' + content)

def main():
    text_fl = input('Input sequence file path: ')
    bp_length = int(input("Enter desired bp length: "))
    sp_diff = int(input("Enter desired start point difference: "))
    outp_file = input('Output file path: ')
    min_match = int(input("Enter minimum matches: "))

    bp_seqList = read_parse(text_fl, bp_length)
    bpSeq_matchList = bpSeq_comp (sp_diff, bp_seqList)
    # print(bp_seqList)
    # print
    # print(bpSeq_matchList)

    write_file(outp_file, min_match, bpSeq_matchList)

if __name__ == "__main__":
    main()
