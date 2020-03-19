#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 4, 2020

@author: ZwareBear
"""
import os
import crypt
import fileinput
import socket

#===========MODIFY THESE=================
usrName = "{USERNAME}" #ansible user to be added ex: ansiblesvc
password ="{PASSWORD}" #any string will work ssh via this password will be disabled later
#========================================

# define vars
dir_path = os.path.dirname(os.path.realpath(__file__))
#logLoc = "{FILE_LOC}" #log file dir (will be mounted if needed)
file_name = "/etc/sudoers"
search = "%sudo	ALL=(ALL:ALL) ALL"
replacement_text = "%sudo	ALL=(ALL:ALL) NOPASSWD: ALL"
disable_pass = "Match User " +usrName +"\n\tPasswordAuthentication no"
hostname = socket.gethostname()

# create user
encPass = crypt.crypt(password,"22")
os.system("useradd -m -p "+encPass+" " + usrName) 

# add to sudoers
os.system("sudo usermod -aG sudo "+ usrName)

#       ( modify sudo to include NOPASSWD: ALL at the end )
with fileinput.FileInput(file_name, inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace(search, replacement_text), end='')

# copy pub ssh key from ansible
"""
Log into Ansible Vm and from the manging user run:
    sudo ssh-copy-id -i ~/.ssh/id_rsa.pub ansiblesvc@{HOSTNAME}
"""
print("Please copy Key over from Ansible host")
print("sudo ssh-copy-id -i ~/.ssh/id_rsa.pub " + usrName+"@"+hostname)
input("\nPress Enter to continue...")

# disable ssh via password
os.system("cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak") 
with open("/etc/ssh/sshd_config", "a") as myfile:
    myfile.write(disable_pass)

# restart ssh service so password disable is enforced
os.system("sudo systemctl restart sshd")

print(usrName + " has been created please try adding to Ansible")
