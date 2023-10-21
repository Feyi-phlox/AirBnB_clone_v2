#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack.
"""
from fabric.api import local
from datetime import datetime
from os import path



def do_pack():
    """ generates a .tgz archive from the contents of the web static folder
    Returns:
        the path of the created archive if creation is successfull, else None.
    """
    if not path.exists('versions'):
        local('mkdir -p versions')
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    file = "web_static_{}".format(time)

    archive = local("tar -cvzf versions/{}.tgz web_static".format(file))

    if archive.succeeded:
        return "versions/{}.tgz".format(file)
    else:
        return None
