from PyMimircache import Cachecow
import sys, os

def main(data_dir):

    output_dir = sys.argv[2]
    file_list = os.walk(data_dir).__next__()[2]

    for file_name in file_list:
        if 'vscsi' in file_name:
            file_path = os.path.join(data_dir, file_name)

            c = Cachecow()

            try:
                    if 'vscsi1' in file_name:
                            reader = c.vscsi(file_path)
                    else:
                            reader = c.vscsi(file_path, vscsi_type=2)
                    stat = c.stat()
                    reuse_distance = c.get_reuse_distance()
                    print(stat)
                    output_file_path = os.path.join(output_dir, file_name)
                    with open(output_file_path, 'w+') as f:
                        for r in reuse_distance:
                            f.write("{}\n".format(r))
            except Exception as inst:
                    print(type(inst))    # the exception instance
                    print(inst.args)     # arguments stored in .args
                    print(inst)          # __str__ allows args to be printed directly,


            print("Done {}".format(file_name))



if __name__ == "__main__":
    data_dir = sys.argv[1]
    main(data_dir)