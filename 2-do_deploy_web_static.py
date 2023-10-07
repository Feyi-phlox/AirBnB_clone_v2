#!/usr/bin/python3
"""This module contains do_deploy function for distributing
web_static archive to the servers.
"""
from fabric.api import run, env, put
from os import path


env.hosts = ['100.25.45.230', '54.175.100.32']


def do_deploy(archive_path):
    """distributes an archive to your web servers.

    args:
       archive_path: pathname to the archive to distribute.

    Functionality:
      - Uploads the archive to the /tmp/ directory of the web server
      - Uncompresses the archive to the folder /data/web_static/releases/
            <archive filename without extension> on the web server
      - Deletes the archive from the web server
      - Deletes the symbolic link /data/web_static/current from the web server
      - Creates a new the symbolic link /data/web_static/current on the
            web server, linked to the new version of your code
            (/data/web_static/releases/<archive filename without extension>)

    Returns:
       True if all operations have been done correctly, otherwise returns False
    """
    if not path.exists(archive_path):
        return False

    filename = str(archive_path).split("/")[-1]
    releases = "/data/web_static/releases"
    uncompfile = str(filename).split('.')[0]

    put(archive_path, '/tmp/{}'.format(filename))

    try:
        run('mkdir -p /data/web_static/releases/{}/'.format(uncompfile))
        run('tar -xzf /tmp/{} -C {}/{}/'.format(filename,
                                                releases,
                                                uncompfile))
        run('rm /tmp/{}'.format(filename))
        run('rsync -a {}/{}/web_static/ {}/{}'.format(releases,
                                                      uncompfile,
                                                      releases,
                                                      uncompfile))
        run('rm -rf {}/{}/web_static/'.format(releases, uncompfile))

        run('rm -rf /data/web_static/current')
        run('ln -s {}/{} /data/web_static/current'.format(releases,
                                                          uncompfile))
        return True
    except Exception:
        return False
