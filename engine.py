from typing import Union
import types


class Tag:
    parent = None
    children = []
    hosts = None
    name = 'default'
    def __init__(self, name: str, parent=None, children=[], hosts=[]):
        self.name = name
        self.parent = parent
        if parent is not None:
            self.parent.addChild(self)
        self.children = []
        self.hosts = hosts
   
    def setParent(self, parent):
        self.parent = parent

    def addChild(self, child):
        self.children.append(child)
   
    def addHost(self, host: str):
        self.hosts.append(host)

class Action:
    name = 'default'
    module = 'default'
    args = None 
    options = None
    def __init__(self, name: str, module: str, options: Union[str,dict] = None, args: Union[str,dict] = None):
        print("[i] Creating new %s action: %s" % (module, name))
        self.name = name
        self.module = module
        self.args = args
        self.options = options

class Play:
    actions = []
    tags = []
    name = 'default'
    def __init__(self, name: str):
        print("[i] Creating play %s" % name)
        self.name = name
        self.actions = []
        self.hosts = []

    def addTag(self, tag: Tag):
        self.tags.append(tag)
        print("[i] Adding Tag %s" % tag.name)

    def addAction(self, action: Action):
        self.actions.append(action)
        print("[i] Adding action %s" % action.name)

class Playbook:
    playPairs = {}
    plays = []
    name = 'default'
    def __init__(self, name: str):
        self.name = name
        self.plays = []
        self.playPairs = {}

    def addPlay(self, tag: Tag, play: Play):
        print("[i] Adding play %s to playbook %s with tag %s" % (play.name, self.name, tag.name))
        self.plays.append(play)
        self.playPairs[tag] = []
        self.playPairs[tag].append(play)

def recurseGen(parent :Tag, indent :str) -> str:
    res = "%s%s:\n" % (indent, parent.name)    
    indent += "  "
    if len(parent.hosts) > 0:
        res += "%s%s\n" % (indent, "hosts:")
    for host in parent.hosts:
        res += "%s%s\n" % ("  "+indent, host)

    for child in parent.children:
        res += "%s%s\n" % (indent, "children:")
        indent += "  "
        res += recurseGen(child, indent)
    return res


def GenerateInventory(playbook: Playbook, alltag: Tag, teams=False):
    res = "---\n"
    res += recurseGen(alltag, "")
    
    if teams:
        '''Generate teams'''
    return res

def GeneratePlaybook(playbook: Playbook):
    res = "---\n"
    for tag in playbook.playPairs:
        res += "- hosts: %s\n" % tag.name
        res += "  roles:\n"
        for play in playbook.playPairs[tag]:
            res += "    - %s\n" % play.name
        res += "\n"
    return res
    
def GeneratePlays(playbook: Playbook) -> str:
    res = ""
    for play in playbook.plays:
        res += "\n"
        res += GeneratePlay(play)
    return res
     

def GeneratePlay(play: Play) -> str:
    res = ""
    res += "# ./roles/%s/tasks/main.yml\n" % play.name
    res += "---\n"
    for i in play.actions:
        res += "- name: %s\n" % i.name
        res += "  %s:\n" % i.module
        if isinstance(i.args, str):
            res += "  %s: %s\n" % (i.module,i.args)
        else:
            if i.args is not None:
                for k in i.args:
                    if k is not None and k is not '':
                        v = i.args[k]
                        if isinstance(v, list):
                            res += "    %s: %s\n" % (k, "\"{{ item }}\"")
                            i.options['with_items'] = v
                        elif isinstance(v, str):
                            res += "    %s: %s\n" % (k,v)
                        else:
                            res += ""
        if i.options is not None:
            for k in i.options:
                if k is not None and k is not '':
                    v = i.options[k]
                    if isinstance(v, str):
                        res += "  %s: %s\n" % (k,v)
                    else:
                        res += "  %s:\n" % k
                        for x in v:
                            res += "    - %s\n" % x
        res+= "\n"
    return res
            

if __name__ == "__main__":
    deploy_churchill_play = Play('churchill-deployment')
    deploy_churchill_play.addAction(Action( \
        name='Install prerequiste packages', \
        module='apt', \
        args={'name': ['apt-transport-https', 'ca-certificates', 'curl', 'software-properties-common'], 'update_cache': 'yes'}, \
        options={'become':'yes'}
    ))
    deploy_churchill_play.addAction(Action( \
        name='Add docker GPG key', \
        module='apt_key', \
        args={'url': 'https://download.docker.com/linux/ubuntu/gpg', 'state': 'present', 'id': '0EBFCD88'}, \
        options={'become':'yes'}
    ))
    deploy_churchill_play.addAction(Action( \
        name='Add docker repo', \
        module='apt_repository', \
        args={'repo':'deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable','state':'present'}, \
        options={'become':'yes'}
    ))
    deploy_churchill_play.addAction(Action( \
        name='Install docker', \
        module='apt', \
        args={'name':'docker-ce', 'update_cache':'yes'}, \
        options={'become':'yes'}
    ))
    deploy_churchill_play.addAction(Action( \
        name='Create service directory', \
        module='file', \
        args={'path':'/etc/systemd/system/docker.service.d','state':'directory'}, \
        options={'become':'yes'}
    ))
    deploy_churchill_play.addAction(Action( \
        name='Configure docker service', \
        module='copy', \
        args={'src':'startup_options.conf','dest':'/etc/systemd/system/docker.service.d/startup_options.conf'}, \
        options={'become':'yes'}
    ))
    deploy_churchill_play.addAction(Action( \
        name='reload daemon', \
        module='systemd', \
        args={'state':'restarted', 'name':'docker.service', 'daemon_reload':'yes'}, \
        options={'become':'yes'}
    ))
    
    deploy_linux_standard_play = Play('linux_standards')
    deploy_linux_standard_play.addAction(Action( \
        name='Add user accounts - Linux', \
        module='user', \
        args={'name':['bob','joe','dan'],'password':'password123','state':'present'}, \
        options={'become':'yes','when':'ansible_system == "Linux"'}
    ))
    deploy_linux_standard_play.addAction(Action( \
        name='Add local admin accounts - Linux', \
        module='user', \
        args={'name':['admin','sysadmin','whiteteam'],'password':'password123','state':'present','groups':"sudo"}, \
        options={'become':'yes','when':'ansible_os_family == "Debian"'}
    ))
    
    all_tag = Tag('all')
    linux_tag = Tag('linux', parent=all_tag)
    churchill_tag = Tag('churchill', parent=linux_tag, hosts=['churchill.team0.ists.io'])

    deploy_playbook = Playbook('deploy') 
    deploy_playbook.addPlay(churchill_tag, deploy_churchill_play)
    deploy_playbook.addPlay(all_tag, deploy_linux_standard_play)

    print(GeneratePlays(deploy_playbook))
    print(GeneratePlaybook(deploy_playbook))
    print(GenerateInventory(deploy_playbook, all_tag))

'''
    deployHulto_play = Play('deploy_hulto')
    deployHulto_play.addAction(Action( \
        'enable ipv6 forwarding', \
        'sysctl', \
        options={'tags':['install','uninstall'],'failed_when':'false','when':['not ci_build','manage_firewall_rules']}, \
        args={'name':'net.ipv4.ip_forward','value':1,'ignoreerrors':'yes'})
    )
    deployHulto_play.addAction(Action( \
        'Generate client configs', \
        'include_tasks', \
        options={'tags':['install','uninstall'],'failed_when':'false','when':['not ci_build','manage_firewall_rules']}, \
        args='client_keys.yml'
    ))

    deployJack_play = Play('deploy_jack')
    deployJack_play.addAction(Action( \
        'enable ipv6 forwarding', \
        'sysctl', \
        options={'tags':['install','uninstall'],'failed_when':'false','when':['not ci_build','manage_firewall_rules']}, \
        args={'name':'net.ipv4.ip_forward','value':1,'ignoreerrors':'yes'})
    )
    deployJack_play.addAction(Action( \
        'Generate client configs', \
        'include_tasks', \
        options={'tags':['install','uninstall'],'failed_when':'false','when':['not ci_build','manage_firewall_rules']}, \
        args='client_keys.yml'
    ))
    
    playbookDeploy = Playbook('deploy')

    all_tag = Tag('all', hosts=['10.80.100.1'])
    jack_tag = Tag('jack', parent=all_tag, hosts=['127.0.0.1','127.0.1.1'])
    hulto_tag = Tag('hulto', parent=jack_tag)
    nick_tag = Tag('nick', parent=hulto_tag, hosts=['172.16.8.1','172.16.8.2'])
    alexander_tag = Tag('alexander', parent=jack_tag, hosts=['alexander.team0.ists.io'])
    for i in range(1,13):
        alexander_tag.addHost('alexander.team%d.ists.io' % i)
    

    playbookDeploy.addPlay(all_tag, deployHulto_play)
    playbookDeploy.addPlay(jack_tag, deployJack_play)

    print(GeneratePlays(playbookDeploy))
    print(GeneratePlaybook(playbookDeploy))
    print(GenerateInventory(playbookDeploy, all_tag))
'''
