#base_pair comparison
#12/16/2019 v3 => issue with speed
#Used dictionary instead of arrays as data structure to improve speed
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


def read_parse (seq, bp_length, sp_diff):
    bp_seqList = {}
    seq_string = seq[1]
    for i in range( len(seq_string) - (bp_length-1) ):
        if seq_string[i:i+bp_length] in bp_seqList:
            temp = bp_seqList.get(seq_string[i:i+bp_length])
            if i - temp[-1] >= sp_diff:
                temp.append(i)
            bp_seqList[seq_string[i:i+bp_length]] = temp
        else:
            temp = [i]
            bp_seqList[seq_string[i:i+bp_length]] = temp
    return bp_seqList

def bpSeq_comp (min_match, bp_seqList):
    bpSeq_matchList = []
    for key, val in bp_seqList.items():
        if len(val) >= min_match:
            temp = (key, val)
            bpSeq_matchList.append(temp)
    return bpSeq_matchList

def write_file (fp, bpSeq_matchList, seq):
    fp.write(seq[0])
    fp.write('Total matched sequences: %d' % len(bpSeq_matchList) + '\n\n')
    for elm in bpSeq_matchList:
        fp.write('%s : %d matches; Starting positions: ' % (elm[0], len(elm[1])))
        fp.write(' '.join(map(str,elm[1])))
        fp.write('\n')
    fp.write('\n\n')

def main():
    user_input = input('(input_file, bp_length, start_diff, min_matches, #_of_misaligns, output_file): ').split()
    text_fl = './Input/' + user_input[0]
    bp_length = int(user_input[1])
    sp_diff = int(user_input[2])
    min_match = int(user_input[3])
    mis_align = int(user_input[4])
    outp_file = './Output/' + user_input[5]

    seq_array = read_into(text_fl)
    fp = open(outp_file, 'w+')
    fp.write('bp_length: %d; starting point difference: %d; minimum matches accounted: %d: # of bp misalignment checked: %d' % (bp_length, sp_diff, min_match, mis_align))
    fp.write('\n\n')
    for seq in seq_array:
        bp_seqList = read_parse(seq, bp_length, sp_diff)
        bpSeq_matchList = bpSeq_comp (min_match, bp_seqList)
        write_file(fp, bpSeq_matchList, seq)
    #print(bp_seqList)
    #print
    #print(bpSeq_matchList)
    fp.close()

if __name__ == "__main__":
    main()
