#!/usr/bin/env python3

from engine import *
from db import *



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

