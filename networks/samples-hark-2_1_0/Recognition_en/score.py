#!/usr/bin/python
# encoding=utf_8
import sys, os, re, numpy, math
import codecs

def conv_encoding(data, to_enc='utf_8'):
    lookup = ('utf_8', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'shift_jis')
    for enc in lookup:
        try:
            data = data.decode(enc)
            break
        except:
            pass
    
    if isinstance(data, unicode):
        return data.encode(to_enc)
    else:
        return data


def recog_dp(recog_result, gt):
    cost = numpy.zeros((len(recog_result),len(gt)))
    cost[0,0] = 0 if recog_result[0] == gt[0] else 1
    #cost[:,0] = numpy.r_[:len(recog_result)] # the 1st column
    #cost[0,:] = numpy.r_[:len(gt)] # the 1st row
    for i in numpy.r_[1:cost.shape[0]]:
    	cost[i,0] = cost[i-1,0] + (0 if recog_result[i] == gt[0] else 1)
    for j in numpy.r_[1:cost.shape[1]]:
    	cost[0,j] = cost[0,j-1] + (0 if recog_result[0] == gt[j] else 1)
    
    cat = numpy.zeros((len(recog_result), len(gt)))
    cat[0,:] = numpy.zeros((1,cat.shape[1]))
    cat[:,0] = numpy.ones((1,cat.shape[0]))
    cat[0,0] = -1 # the start point is kept -1
    
    for i in numpy.r_[1:cost.shape[0]]:
        for j in numpy.r_[1:cost.shape[1]]:
            cost[i,j] = numpy.hstack([cost[i,j-1],cost[i-1,j],cost[i-1,j-1]]).min() + (0 if recog_result[i] == gt[j] else 1)
            cat[i,j] = numpy.hstack([cost[i,j-1],cost[i-1,j],cost[i-1,j-1]]).argmin()

    cost[-1,:] += numpy.r_[cost.shape[1]-1:-1:-1]
    cost[:,-1] += numpy.r_[cost.shape[0]-1:-1:-1]
    # retrive the path
    #i = cat.shape[0]-1
    #j = cat.shape[1]-1
    if cost[-1,:].min() < cost[:,-1].min():
    	i = cat.shape[0]-1
    	j = cost[-1,:].argmin()
    else:
    	i = cost[:,-1].argmin()
    	j = cat.shape[1]-1
   
    path = numpy.array([i,j])
    status = []
    # go backward
    while cat[i,j] != -1:
        status.append(cat[i,j])
        if cat[i,j] == 0:
            j -= 1
        elif cat[i,j] == 1:
            i -= 1
        elif cat[i,j] == 2:
            i -= 1
            j -= 1
        path = numpy.vstack([path, numpy.array([i,j])])
    
    #status.append(2.0)
    return cost, numpy.flipud(path), status[-1::-1]



def parse_julius_result(julius_result):
    id_list = [] # list for recognized ids
    dir_list = [] # list for the directions
    utter_list = [] # list for the content of utterances

    re_id = re.compile("source_id = [0-9]+")
    re_dir = re.compile(", azimuth = -?[0-9.]+")
    #re_utter = re.compile("pass1_best: .*")
    re_utter = re.compile("sentence1: .*")
    for line in open(julius_result, 'r'):
        if re_id.search(line):
            # append id
            m = re_id.search(line)
            id_list.append(int(m.group()[12:]))
        if re_dir.search(line):
            # append direction
            m = re_dir.search(line)
            dir_list.append(float(m.group()[12:]))
                
        if re_utter.search(line):
            # append utterance
            m = re_utter.search(line)
            if(re.compile("</s>").search(line)):
                utter_list.append(conv_encoding(m.group()[15:-5])) # <s> ###### </s>
            else:
                utter_list.append(conv_encoding(m.group()[15:]))

    return id_list, dir_list, utter_list

def parse_trans_file(trans_file):
    trans_list = []
    for line in open(trans_file, 'r'):
        if len(line) > 0:
            trans_list.append(conv_encoding(line[0:-1]))

    return trans_list

def stamp(recog, gt, status):
	if status == 0:
		return 'Deletion'
	elif status == 1:
		return 'Insertion'
	elif status == 2 and recog == gt:
		return 'Correct'
	else:
		return 'Wrong'

if __name__ == '__main__':
	if len(sys.argv) < 5:
		print "usage: score.py julius_result transcription_file direction margin_of_dir"
		quit()

	julius_result = sys.argv[1]
	trans = sys.argv[2]
	dir = float(sys.argv[3])
	dir_margin = float(sys.argv[4])

	#dir = math.fmod(dir+180, 360.0) - 180.0

	[id_list, dir_list, utter_list] = parse_julius_result(julius_result)
	trans_list = parse_trans_file(trans)

	check_utter_list = []
	for (id, d, utter) in zip(id_list, dir_list, utter_list):
		if dir - dir_margin <= d and d <= dir + dir_margin:
		    check_utter_list.append(utter)

	#check_utter_list = [x[2] for x in sorted(zip(id_list, dir_list, utter_list), key=lambda x:x[0]) if abs(x[1]-dir) < dir_margin]
	
	if len(check_utter_list) == 0:
		print "no utterance from " + sys.argv[3] + " [degree]"
		quit()

	[cost,path,status] = recog_dp(check_utter_list, trans_list)
	status.append(2.0)
	
	num_correct = 0
	print u'ground truth\t\trecognition result\t\tstatus'.encode('utf_8')
	for i in range(path.shape[0]):
		rec = check_utter_list[path[i,0]]
		gt = trans_list[path[i,1]]
		
		str_stamp = stamp(rec,gt,int(status[i]))

		if str_stamp == 'Deletion':
			rec = ''
		if str_stamp == 'Insertion':
			gt = ''
		if str_stamp == 'Correct':
			num_correct += 1
			
		print '"'+gt+'"'+reduce(lambda x,y:x+y,[' ' for p in range(21-len(gt))], '')+ '"%s"'%(rec)+ reduce(lambda x,y:x+y, [' ' for p in range(23-len(rec))], '')+str_stamp
		

	hit_num = float(num_correct)
	all_num = float(len(trans_list))
	print int(hit_num), ' / ' + str(int(all_num)) + ' (' + str(hit_num/all_num*100) + ' %)'

