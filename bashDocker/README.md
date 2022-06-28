# Bash + Docker task

Run next commands:

To build and run container
```
$ docker image build -t my_image .
$ docker run --name my_container -it -d my_image
```

First task:
```
$ docker exec my_container  bash /script_dir/script_1.sh script_dir/dracula.txt
```

Second task:
```
$ docker exec my_container bash /script_dir/script_2.sh script_dir/dracula.txt script_dir/cache
$ docker exec my_container ls script_dir/cache
```