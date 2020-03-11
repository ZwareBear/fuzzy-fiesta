#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 4, 2020

@author: ZwareBear
"""
import os
import crypt
import fileinput

# define vars
dir_path = os.path.dirname(os.path.realpath(__file__))

ssh_pub = "{path to public key}"
logLoc = dir_path + "/logs/" #log file dir (will be mounted if needed)
usrName = "{username}" #ansible user to be added
password ="{password}" 
file_name = dir_path + "/sudoers.txt"


search = "%sudoALL=(ALL:ALL) ALL"
replacement_text = "%sudoALL=(ALL:ALL) NOPASSWD: ALL"

# create user
encPass = crypt.crypt(password,"22")
os.system("useradd -m -p "+encPass+" " + usrName)
# add to sudoers 
os.system("usermod -aG sudo "+ usrName)

#       ( modify sudo to include NOPASSWD: ALL at the end )
# cat /etc/sudoers
with fileinput.FileInput(file_name, inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace(search, replacement_text), end='')

# copy pub ssh key from ansible 
os.system("mkdir /home/"+usrName+"/.ssh/")
os.system("cp "+ ssh_pub +" /home/"+usrName+"/.ssh/authorized_keys")

print("\n"+ usrName + " has been created please try adding to Ansible")
