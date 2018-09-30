import subprocess
import venv;
import os;

env_folder= os.path.join(os.path.dirname(os.path.abspath(__file__)),'xtest-env')


if not os.path.exists(env_folder):
     venv.create(env_folder);

subprocess.run([os.path.join(env_folder, 'bin', 'pip3'),'install','-r','requirements.txt'])
