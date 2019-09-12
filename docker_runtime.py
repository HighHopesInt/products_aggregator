def in_docker():
    docker_file = open('/proc/1/cgroup')
    for line in docker_file:
        if 'docker' in line:
            return True
    return False
