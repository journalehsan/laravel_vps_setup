# VPS Setup Script For Laravel 

## Overview

This script automates the setup of a Virtual Private Server (VPS) for hosting a Laravel application. It performs a series of tasks including system updates, installation of necessary software (Apache, PHP, MariaDB, NGINX), configuration of services, and performance tuning.

## Prerequisites

- A VPS running a compatible Linux distribution (e.g., CentOS, Fedora).
- Root or sudo access to the server.
- Basic knowledge of command-line operations.

## Features

- Updates the system and installs essential utilities.
- Installs and configures Apache and NGINX as a reverse proxy.
- Installs PHP 8.3 and necessary PHP extensions.
- Installs and secures MariaDB (MySQL).
- Configures Apache to serve the Laravel application.
- Sets up performance tuning with ZRAM and swappiness adjustments.
- Installs the XanMod kernel for improved performance.
- Configures Gzip compression for Apache.
- Sets up basic security measures with a firewall and Fail2Ban.

## Installation

1. **Clone the repository** (if applicable) or copy the script to your server.
2. **Make the script executable**:
   ```bash
   chmod +x setup_vps.py
   ```
3. **Run the script** with root privileges:
   ```bash
   sudo python3 setup_vps.py
   ```

## Usage

The script will execute a series of commands to set up the VPS. You can monitor the progress through the console output. The script includes a progress bar for each task, providing visual feedback on the installation process.

### Configuration

- **NGINX Configuration**: Update the `server_name` directive in the NGINX configuration block to match your domain.
- **Apache Configuration**: Ensure the `DocumentRoot` points to the correct location of your Laravel application.

## Important Notes

- The script assumes that the Laravel application zip file (`laravel_app.zip`) is present in the current directory. Ensure that this file is available before running the script.
- After the script completes, you may need to adjust additional settings based on your specific application requirements.
- Always back up your server and data before running automated scripts.

## Troubleshooting

If you encounter any errors during the execution of the script, the error message will be displayed in the console. Common issues may include:

- Missing dependencies: Ensure that your system is up to date and that you have internet access.
- Permission issues: Make sure you are running the script with sufficient privileges (as root or using sudo).

## Conclusion

Once the script has completed successfully, your VPS will be set up and ready to host your Laravel application. You can access your application through the configured domain or IP address.

For further customization or advanced configurations, refer to the official documentation of the respective software components (Apache, NGINX, PHP, MariaDB, etc.).
