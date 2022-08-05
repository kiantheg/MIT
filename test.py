
import pickle              # import module first

f = open('/Users/rishita/bwsi22/team5/marathon_0_image.pkl', 'r')   # 'r' for reading; can be omitted
mydict = pickle.load(f)         # load file content as mydict
f.close()                       

print(mydict)