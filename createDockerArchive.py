import tarfile

with tarfile.open('skinbaronDockerArchive.tar', 'w') as archive:
    archive.add('skinbaron.py')
    archive.add('Dockerfile')
    archive.add('requirements.txt')