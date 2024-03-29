# This file is part of PyFlaSQL.
# Original author: Raphael Viera (raphael.viera@emse.fr)
# Contribution : ISMIN student X (ismin.student@etu.emse.fr)
# License: check the LICENSE file.
"""
Implements the logic for TP2 - Scanning Networks
"""
from flask import Flask, render_template, url_for, redirect
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from ....models.sql import db, UserDB
from ...utils import get_shell_output
from ....models.srie.tp2_scanning_networks.forms import PingAddrForm, NmapForm, PortsForm, NessusButton, TraceRouteForm, DnsForm1, DnsForm2
import os


@login_required
def srie_tp2_scanning_networks():
    """
        Logic for /srie/tp2_scanning_networks/home
        Login is required to view this page

        Args:
            - None.

        Returns:
            - rendered template view/templates/srie/tp2_scanning_networks/home.html
        """
    username = current_user.username
    return render_template(url_for('blueprint.srie_tp2_scanning_networks')+'.html', username=username)

@login_required
def srie_tp2_pingaddr():
    """
        Handles the logic for view/templates/srie/tp2_scanning_networds/pingaddr.html
        Login is required to view this page

        Print in the user interface private and public IP addresses.

        Args:
            - None.

        Returns:
            - rendered template view/templates/srie/tp2_scanning_networds/pingaddr.html with content passed as a context variable
        """
    # Create a dict to store the formulary and the shell output. This dict is passed to the .html file.
    content = {"form": PingAddrForm(),
               "command_executed": "Waiting ...",
               "command_output": "Waiting ..."
               }
    
    if content["form"].validate_on_submit():
        # Get IP address and number of pings from the user interface (UI)
        ip_address = content["form"].ip_address.data
        npings = content["form"].npings.data
        content["command_executed"] = f"ping -c {npings} {ip_address}"
        content["command_output"] = get_shell_output(content["command_executed"])
        # print(content["shell_output"])  # for debug only
        return render_template(url_for('blueprint.srie_tp2_pingaddr')+'.html', content=content)

    return render_template(url_for('blueprint.srie_tp2_pingaddr')+'.html', content=content)

@login_required
def srie_tp2_nmap():
    content = {
        "form" : NmapForm(),
        "command_executed": "Waiting ...",
        "command_output" : "Waiting ...",
    }

    if content["form"].validate_on_submit():
        range_ip = content["form"].range_ip.data
        content["command_executed"] = f"nmap -T3 -sn {range_ip}"
        content["command_output"] = get_shell_output(content["command_executed"])

    return render_template(url_for('blueprint.srie_tp2_nmap')+'.html', content = content)

@login_required
def srie_tp2_ports():
    content = {
        "form" : PortsForm(),
        "command_executed": "Waiting ...",
        "command_output" : "Waiting ...",
    }

    if content["form"].validate_on_submit():
        ip = content["form"].ip.data
        content["command_executed"] = f"nmap -sV {ip}"
        content["command_output"] = get_shell_output(content["command_executed"])
    return render_template(url_for('blueprint.srie_tp2_ports')+'.html', content = content)


@login_required
def srie_tp2_nessus():
    content = {
        "button" : NessusButton(),
    }
    if content["button"].validate_on_submit():
        os.system('/bin/systemctl start nessusd.service')
    return render_template(url_for('blueprint.srie_tp2_nessus')+'.html', content= content)

@login_required
def srie_tp2_traceroute():
    content = {
        "form" : TraceRouteForm(),
        "command_executed": "Waiting...",
        "command_output": "Waiting...", 
    }

    if content["form"].validate_on_submit():
        ip = content["form"].ip.data
        content["command_executed"] = f"traceroute {ip}"
        content["command_output"] = get_shell_output(content["command_executed"])
    return render_template(url_for('blueprint.srie_tp2_traceroute')+'.html', content = content)

@login_required
def srie_tp2_dns():
    content = {
        "form1" : DnsForm1(),
        "form2" : DnsForm2(),
        "command_executed": "Waiting...",
        "command_output": "Waiting...", 
    }

    if content["form1"].validate_on_submit():
        domain1= content["form1"].domain1.data
        content["command_executed"] = f"dnsrecon -d {domain1}"
        content["command_output"] = get_shell_output(content["command_executed"])
    
    if content["form2"].validate_on_submit():
        domain2= content["form2"].domain2.data
        content["command_executed"] = f"dnsenum -w {domain2}"
        content["command_output"] = get_shell_output(content["command_executed"])
   
    return render_template(url_for('blueprint.srie_tp2_dns')+'.html', content = content)