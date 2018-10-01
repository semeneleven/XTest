import subprocess
import venv
import os
import urllib.request as request

env_folder= os.path.join(os.path.dirname(os.path.abspath(__file__)),'xtest-env')


if not os.path.exists(env_folder):
     print("-"*10+"Creating virtual enviroment...")
     venv.create(env_folder)
     
if os.name=='nt':
     try:
           subprocess.run([os.path.join(env_folder, 'Scripts', 'python'),'-m','pip','freeze'], check=True)
     except subprocess.CalledProcessError:          
          if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),'get-pip.py')):
               print("-"*10+"Downloading get-pip.py...")
               with request.urlopen('https://bootstrap.pypa.io/get-pip.py') as url_get:
                    with open('get-pip.py','wb') as file:
                         file.write(url_get.read())
               print("-"*10+"Downloading pip...")
               subprocess.run([os.path.join(env_folder, 'Scripts', 'python'),'get-pip.py'])

     print("-"*10+"Downloading requered libraries...")
     subprocess.run([os.path.join(env_folder, 'Scripts', 'python'),'-m','pip','install','-r','requirements.txt'])               
               
    
else:
     print("-"*10+"Downloading requered libraries...")
     subprocess.run([os.path.join(env_folder, 'bin', 'pip3'),'install','-r','requirements.txt'])
print("-"*32)
print("-"*32)
print("Virtual enviroment ready for use.")
print("-"*32)
print("-"*32)
