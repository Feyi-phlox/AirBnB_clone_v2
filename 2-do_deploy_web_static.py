#!/usr/bin/python3
""" Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers, using the function do_deploy
"""
from fabric.api import env, run, put
from os import path

env.hosts = ['54.84.85.121', '54.237.5.69']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """ Distributes an archive to the web servers and deploys it
    args: archive_path(str)
    Returns: true if successful, else False.
    """
    if not path.exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")
        archive = archive_path.split("/")[1]
        file = archive.split(".")[0]
        release = "/data/web_static/releases/"
        folder = "/data/web_static/releases/{}".format(file)
        run("mkdir -p {}".format(folder))
        run(" tar -xzf /tmp/{} -C {}".format(archive, folder))
        run("rm /tmp/{}".format(archive))
        run("mv {}{}/web_static/* {}{}/".format(release, file, release, file))
        run("rm -rf /data/web_static/releases/{}/web_static".format(file))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder))
        print("New version deployed!")
        return True
    except Exception:
        return False
