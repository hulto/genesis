import engine

class Host:
    resources={}
    networking={}
    access={}
    image=''
    name='default'
    def __init__(self, name: str, \
                        image: str, \
                        mem=1024, cpu=1, \
                        ip=None, hostname: str = 'hultyboi', network: str='vmnet', \
                        ssh_key=None, winrm: bool=False):
        self.name=name
        self.image=image 
        self.resources = {}
        self.resources['mem']=mem
        self.resources['cpu']=cpu
        self.networking = {}
        self.networking['ip']=ip
        self.networking['hostname']=hostname
        self.networking['network']=network
        self.access = {}
        self.access['ssh_key']=ssh_key
        self.access['winrm']=winrm

    def generateConfig(self):
        res = "Vagrant.configure(\"2\") do |config|\n"
        res+= "  config.vm.box = \"%s\"\n" % self.image
        if self.networking['ip'] is not None:
            res+="  config.vm.network \"private_network\", ip: \"%s\", virtualbox__intnet: \"%s\"\n" % (self.networking['ip'], self.networking['network'])
        else:    
            res+="  config.vm.network \"private_network\", type: \"dhcp\"\n"
        res+="  config.vm.provider \"virtualbox\" do |vb|\n"
        res+="    vb.memory = %d\n" % self.resources['mem']
        res+="    vb.cpus = %d\n" % self.resources['cpu']
        res+="  end\n"
        res+='  config.vm.provision "file", source: "~/.ssh/id_rsa.pub", destination: "~/.ssh/me.pub"\n'
        res+=' config.vm.provision "shell", inline: "cat ~vagrant/.ssh/me.pub >> ~vagrant/.ssh/authorized_keys"\n'
        res+="end\n"
        
        return res
         

def createHost():
    print("Creating host")

def tagHost():
    print("tagging host")   

def createPlay():
    print("Creating play")

def createPlaybook():
    print("Creating playbook")


if __name__ == "__main__":
    hultokovm = Host('HultyBoi', \
                    'ubuntu/xenial64', \
                    mem=2048, cpu=2, \
                    ip='10.0.0.4', hostname='hultyboi', network='vmnet') 
    print(hultokovm.generateConfig())
