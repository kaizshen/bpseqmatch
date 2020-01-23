#base_pair comparison
#11/29/2019 v2 => issue with speed
#Added ability to read multiple sequences in a file and ignore new lines
from itertools import filterfalse

def read_into (text_fl):
    seq_array_temp = []
    with open(text_fl,"r") as fp:
        for cnt, line in enumerate(fp):
            if line == '\n':
                continue
            seq_array_temp.append(line)
    it = iter(seq_array_temp)
    seq_array = list(zip (it, it))
    return seq_array


def read_parse (seq, bp_length):
    bp_seqList = []
    seq_string = seq[1]
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

def write_file (fp, min_match, bpSeq_matchList, seq):
    bpSeq_matchList = list(filterfalse(lambda x: len(x) < min_match, bpSeq_matchList))
    fp.write(seq[0])
    fp.write('Total matched sequences: %d' % len(bpSeq_matchList) + '\n\n')
    for elm in bpSeq_matchList:
        fp.write('%s : %d matches; Starting positions: ' % (elm[0][1], len(elm)))
        fp.write(' '.join('%s' % x[0] for x in elm))
        fp.write('\n')
    fp.write('\n\n')

def main():
    text_fl = input('Input sequence file path: ')
    bp_length = int(input("Enter desired bp length: "))
    sp_diff = int(input("Enter desired start point difference: "))
    outp_file = input('Output file path: ')
    min_match = int(input("Enter minimum matches: "))

    seq_array = read_into(text_fl)
    fp = open(outp_file, 'w+')
    fp.write('bp_length: %d; starting point difference: %d; minimum matches accounted: %d' % (bp_length, sp_diff, min_match))
    fp.write('\n\n')
    for seq in seq_array:
        bp_seqList = read_parse(seq, bp_length)
        bpSeq_matchList = bpSeq_comp (sp_diff, bp_seqList)
        write_file(fp, min_match, bpSeq_matchList, seq)
    # print(bp_seqList)
    # print
    # print(bpSeq_matchList)
    fp.close()

if __name__ == "__main__":
    main()
