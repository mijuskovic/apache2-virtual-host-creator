# apache2 virtual host creator 
Script for creating and configuring apache2 virtual hosts on Debian based Linux distributions.
I wrote it to make it easier for me to create virtual hosts for the purpose of developing web applications.
## Installation
To install script globally and use it as terminal command, just run install.py script.
``` python install.py ```
## Usage


``` 
usage: vhcreate [-h] [--ip IP] [--admin ADMIN] [--docroot DOCROOT] domain
    
    positional arguments:
      domain             specify domain name for virtual host, e.g. project.development
    
    optional arguments:
      -h, --help         show this help message and exit
      --ip IP            custom ip address to be added to hosts file for specified
                         domain name, default "127.0.0.1"
      --admin ADMIN      custom server admin e-mail address, default
                         webmaster@localhost
      --docroot DOCROOT  custom document root, default /var/www/project/public
```
## Contributing
If this script is useful for you, feel free to share, comment or contribute.
## History
This is very first version of this tool.
## License
Licensed under the term of MIT License. See attached file LICENSE.txt.
