import os
import subprocess
import sys
import pandas as pd
from IPython.display import display, HTML
import re
import readline


class dev:
    def inp(self,check):
        if check.lower()=='yes' or check.lower()=='y' or check.lower()=='ye' or check.lower()=='s':
            os.system("rm -rf ./out.csv && rm -rf ./out2.txt && rm -rf ./trash.txt && rm -rf node_check.txt && rm -rf node_free.txt")
            data = ["\033[94m Get help in accessing devcloud nodes \033[00m","\033[94m Check the status of a particular node with node number \033[00m","\033[94m Check similar free nodes \033[00m","\033[94m Change the queue \033[00m"]
            
            # Create the pandas DataFrame with column name is provided explicitly
            df = pd.DataFrame(data, columns=['\033[93m Devcloud Quick Assist \033[00m'])
            df=pd.DataFrame(df).rename_axis('\033[93m Option \033[00m', axis=0)
            # print dataframe.
            print(df.to_markdown())
            print(" ")
            opt=input("\033[95m Enter a option (Enter E to Exit): \033[00m")
            self.option(opt)
        else:
            print('')

    def option(self,opt):
        os.system("rm -rf ./out.csv && rm -rf ./out2.txt && rm -rf ./trash.txt")
        if opt=='0':
            self.access_nodes()

        elif opt=='1':

            node=input("\033[92m Please enter the node number (To Exit this window enter E or B for going back): \033[00m")
            print('')
            
            if node.lower()=='exit' or node.lower()=='e':
                pass
                
            elif node=='b' or node=='B' or node.lower()=='back':
                self.inp('y')
            
            elif re.match(r'[s]0\d{2}[-]n\d{3}',node) and node!='s000-n000' and len(node)<10:
                self.node_check(node)
            else:
                print("Invalid node number ")
                print(' ')
                self.option('1')
#                 print("\033[00m")
#                 print(' ')

#         elif opt=='3':
#             source=input("\033[95m Please enter source path: \033[00m")
#             dest=input("\033[95m Please enter destination path: \033[00m")
#             self.scp(source,dest)
        elif opt=='2':
            node=input("\033[92m Please enter the node number (To Exit this window enter E or B for going back): \033[00m")
            print('')
            
            if node.lower()=='exit' or node.lower()=='e':
                pass
                
            elif node=='b' or node=='B' or node.lower()=='back':
                self.inp('y')
            
            elif re.match(r'[s]0\d{2}[-]n\d{3}',node) and node!='s000-n000' and len(node)<10:
                self.similar_free(node)
            else:
                print("Invalid node number ")
                print(' ')
                self.option('2')
        elif opt=='3':
            self.que()
        
        elif opt.lower()=='exit' or opt.lower()=='e':
            pass
            
        else:
            print(' ')
            print('Invalid Option')
            print('')
            self.inp('y')
        

    def access_nodes(self):

        print("\033[92m Machines Available On DevCloud: ")

        print('')
        print('\033[91m Processor codenames: \033[00m')
        print('\033[00m tgl:Tiger Lake,','cfl:Coffee Lake,','clx:Cascade Lake,','icx:Ice Lake,','skl:Sky Lake,','spr:Sapphire Rapids \033[00m')

        print('\033[92m \n ')

        os.system("pbsnodes | grep properties | sort | uniq -c >> out.csv")

        free_nodes=[]
        no_cpu=[]
        tcpus=[]
        #os.system("cat ./out.txt")

        test = pd.read_csv(r"./out.csv",sep='\s+',header=None)

        for i in list(test[3]):
            free_nodes.append(str(os.popen("pbsnodes | grep -i "+str(i)+" -A 6 -B 4 | grep 'state = free' | wc -l").read())[:-1])
            no_cpu.append(str(os.popen("pbsnodes | grep -i "+str(i)+" -A 4 -B 1 | grep 'ncpus='").read()))

        for i in no_cpu:
            try:
                tcpus.append((i.split('ncpus='))[1].split(',')[0])
            except:
                tcpus.append('0')

        df1=pd.DataFrame({'Properties':list(test[3]),'Total Nodes':list(test[0]),'Free Nodes':free_nodes,'ncpus':tcpus})
        df1=pd.DataFrame(df1).rename_axis('Serial Number', axis=0)

        print(df1.to_markdown())
        print('')
        try:
            def serial():
                print('')
                inp=input("Enter the Serial Number (To Exit this window enter E or B for going back): \033[00m")
                print('')

                if inp=='e' or inp=='E':
                    print("\033[00m")

                elif inp=='b' or inp=='B' or inp.lower()=='back':
                    self.inp('y')

                elif len(inp)<len(df1)-1 and inp.isdigit():
                    code=test[3][int(inp)]
#                     code='.*'.join(code)
                    os.system("pbsnodes | grep -i "+code+" -B 4 | grep 'state = free' -B 1 > out2.txt")

                    Path= os.getcwd()
                                            
                    #print(Path,type(Path))
                    if int(os.popen("cat ./out2.txt | grep 'state = free' | wc -l").read()) == 0:
                        print('Currently there are no free nodes')
                        serial()
                        print("\033[00m")
                    # elif inp=='7':
                    #     os.system('qsub -I -l nodes=1:fpga_compile:ppn=2 ')
                    else:
                        with open('./out2.txt') as f:
                            first_line = f.readline()
                        # print(str(first_line[:-1:]))
                        os.system('qsub -I -l nodes='+str(first_line[:-1:])+':ppn=2')
                else:
                    print('Please enter a value present in the above table')
                    serial()
            serial()

        except:
            print('Please enter a value present in the above table')
            serial()
            print("\033[00m")

        

    def node_check(self,n):
        lines=[]
        free=[]
        os.system("rm -rf node_check.txt && rm -rf node_free.txt")
        os.system("pbsnodes | grep -i "+n+" -A 4 | grep 'state =' -A 3 -B 1 ")
        os.system("pbsnodes | grep -i "+n+" -A 4 | grep 'state =' -A 3 -B 1 >>node_check.txt") ###########
            
        with open('./node_check.txt') as file:
#             lines = [line.rstrip() for line in file]
            for line in file:
                lines.append(line[:-1])
#         print(lines)

        if len(lines)==0:
            print('Invalid node number')
            self.option('1')
        else:
            similar=lines[4].split(' ')[-1]
            os.system("rm -rf node_check.txt && rm -rf node_free.txt")
            
            if lines[1][-4::]=='free':
                check=input(n+' is free, want to access this node? (yes or no): ')

                if check.lower()=='yes' or check.lower()=='y' or check.lower()=='ye' or check.lower()=='s':
                    os.system('qsub -I -l nodes='+n+':ppn=2')
                else:
                    self.inp('y')
            else:
                print(' ')
                print(n+' is currently unavailable, these are the smiliar nodes currently available: ')
    #             print(similar,'yes')
                print(' ')

                os.system("pbsnodes | grep -i "+similar+" -B 4 | grep 'state = free' -B 1 >>node_free.txt") ########

                with open('./node_free.txt') as file:
    #             lines = [line.rstrip() for line in file]
                    for line in file:
                        free.append(line[:-1])
                k=free[::3]
                print('These are the '+'\033[92m Available \033[00m'+' nodes: \n')
                print(*k)
                
                def node():
        #             print(len(k))
                    print('')
                    check=input('\033[92m Enter the node number if you want to access the above node (To Exit this window enter E or B for going back): \033[00m')
                    
                    if check.lower()=='exit' or check.lower()=='e':
                        pass

                    elif check=='b' or check=='B' or check.lower()=='back':
                        self.option('1')

                    elif re.match(r'[s]0\d{2}[-]n\d{3}',check) and check!='s000-n000' and len(check)<10:
                        os.system('qsub -I -l nodes='+check+':ppn=2')
                    else:
                        print(' ')
                        print('Invalid node number')
                        node()
                node()
        return 

    def similar_free(self,n):
        lines=[]
        free=[]
        os.system("rm -rf node_check.txt && rm -rf node_free.txt")
        #os.system("pbsnodes | grep -i "+n+" -A 4 | grep 'state =' -A 3 -B 1 ")
        os.system("pbsnodes | grep -i "+n+" -A 4 | grep 'state =' -A 3 -B 1 >>node_check.txt") ###########
        print('')
        with open('./node_check.txt') as file:
#             lines = [line.rstrip() for line in file]
            for line in file:
                lines.append(line[:-1])
#         print(lines)

        if len(lines)==0:
            print('Invalid node number')
            self.option('2')
        
        else:
            similar=lines[4].split(' ')[-1]
            
            os.system("rm -rf node_check.txt && rm -rf node_free.txt")
            os.system("pbsnodes | grep -i "+similar+" -B 4 | grep 'state = free' -B 1 >>node_free.txt") ########
            with open('./node_free.txt') as file:
#             lines = [line.rstrip() for line in file]
                for line in file:
                    free.append(line[:-1])
            
            k=free[::3]
            if len(k)==0:
                print('Currently there are no free similar nodes available')
            else:
                print('These are the '+'\033[92m Free Similar \033[00m'+' nodes: \n')
            print(*k)
            print('')
            self.option('2')
            
            
#     def scp(self,source,dest):
#         try:
#             pass
#         except:
#             pass
#         return
    
    def que(self):
        data = ["\033[92m OneAPI Queue \033[00m","\033[92m NDA Queue \033[00m","\033[92m FPGA Queue \033[00m"]
        df = pd.DataFrame(data, columns=['\033[92m Queues \033[00m'])
        df=pd.DataFrame(df).rename_axis('\033[92m Option \033[00m', axis=0)
            # print dataframe.
        print(df.to_markdown())
        print(" ")
        pt=input("\033[94m Enter a option (Enter E to Exit): \033[00m")
        
        if pt=='0':
            os.system("""tee > ./job.sh << EOF
#!/bin/bash
export PBS_DEFAULT=v-qsvr-1
EOF""")     
            #os.system("conda deactivate") 
            os.execv("/bin/bash", ["bash", "-c", "source ./job.sh;bash"])

        elif pt=='1':

            os.system("""tee > ./job.sh << EOF
#!/bin/bash
export PBS_DEFAULT=v-qsvr-nda
EOF""")
            #os.system("conda deactivate")
            os.execv("/bin/bash", ["bash", "-c", "source ./job.sh;bash"])

    
        elif pt=='2':
            os.system("""tee > ./job.sh << EOF
#!/bin/bash
export PBS_DEFAULT=v-qsvr-fpga
EOF""")
            #os.system("conda deactivate")
            os.execv("/bin/bash", ["bash", "-c", "source ./job.sh;bash"])
        else:
            print("Invalid option")
            self.que()
            
        #self.inp("yes")


obj=dev()

check=input("\033[95m New to the DevCloud and need help accessing the nodes? (Yes or No): \033[00m")
obj.inp(check)
#host=os.popen('hostname').read()
#if host[:-1]=='login-2':
    #check=input("\033[95m New to the DevCloud and need help accessing the nodes? (Yes or No): \033[00m")
    #obj.inp(check)
#else:
    #pass