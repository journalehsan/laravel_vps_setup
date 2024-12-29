import os
import subprocess
from tqdm import tqdm
import time

def run_command(command, description=""):
    """
    Run a shell command and handle errors. Show a progress bar for each task.
    """
    print(f"\n{description}")
    with tqdm(total=100) as pbar:
        try:
            subprocess.check_call(command, shell=True)
            for _ in range(100):
                time.sleep(0.01)
                pbar.update(1)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            exit(1)


def setup_vps():
    # Step 1: Update the system and install basic tools
    run_command("dnf update -y", "Updating system packages...")
    run_command("dnf install -y epel-release wget curl unzip nano", "Installing basic utilities...")

    # Step 2: Install Apache
    run_command("dnf install -y httpd", "Installing Apache...")
    run_command("systemctl enable --now httpd", "Enabling and starting Apache...")

    # Step 3: Install PHP 8.3 and necessary extensions
    run_command("dnf module enable php:8.3 -y", "Enabling PHP 8.3 module...")
    run_command("dnf install -y php php-cli php-mysqlnd php-xml php-mbstring php-curl php-zip php-bcmath", "Installing PHP 8.3...")

    # Step 4: Install MySQL (MariaDB)
    run_command("dnf install -y mariadb-server", "Installing MariaDB server...")
    run_command("systemctl enable --now mariadb", "Starting and enabling MariaDB...")
    run_command("mysql_secure_installation", "Running MySQL secure installation wizard...")

    # Step 5: Configure NGINX as a reverse proxy
    run_command("dnf install -y nginx", "Installing NGINX...")
    nginx_config = """
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ~ \.php$ {
        return 404;
    }

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_proxied any;
}
"""
    with open("/etc/nginx/conf.d/laravel.conf", "w") as f:
        f.write(nginx_config)
    run_command("systemctl enable --now nginx", "Starting and enabling NGINX...")

    # Step 6: Configure Apache to listen on port 8080
    apache_config = """
<VirtualHost *:8080>
    DocumentRoot "/srv/laravel/public"
    <Directory "/srv/laravel/public">
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
"""
    with open("/etc/httpd/conf.d/laravel.conf", "w") as f:
        f.write(apache_config)
    run_command("systemctl restart httpd", "Restarting Apache to apply changes...")

    # Step 7: Tune system performance (Swappiness and ZRAM)
    run_command("sysctl vm.swappiness=10", "Tuning swappiness to 10...")
    with open("/etc/sysctl.d/99-swappiness.conf", "w") as f:
        f.write("vm.swappiness=10\n")

    run_command("dnf install -y zram-generator-defaults", "Installing ZRAM generator...")
    zram_config = """
[zram0]
zram-size = ram / 2
compression-algorithm = zstd
"""
    with open("/etc/systemd/zram-generator.conf", "w") as f:
        f.write(zram_config)
    run_command("systemctl restart systemd-zram-setup@zram0", "Configuring ZRAM...")

    # Step 8: Install XanMod kernel
    run_command("dnf copr enable -y rmnscnce/kernel-xanmod", "Adding XanMod kernel repository...")
    run_command("dnf install -y kernel-xanmod", "Installing XanMod kernel...")

    # Step 9: Install and configure Laravel application
    run_command("rm -rf /srv/laravel && mkdir -p /srv/laravel", "Preparing Laravel directory...")
    run_command("dnf install -y unzip", "Installing unzip tool...")
    run_command("unzip laravel_app.zip -d /srv/laravel", "Extracting Laravel application...")
    run_command("chown -R apache:apache /srv/laravel", "Setting permissions for Laravel app...")
    run_command("chmod -R 775 /srv/laravel/storage /srv/laravel/bootstrap/cache", "Setting file permissions...")

    # Step 10: Enable Gzip compression in Apache
    apache_gzip_config = """
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css application/javascript application/json
</IfModule>
"""
    with open("/etc/httpd/conf.d/gzip.conf", "w") as f:
        f.write(apache_gzip_config)
    run_command("systemctl restart httpd", "Restarting Apache to enable Gzip...")

    # Step 11: Harden the system (Basic tweaks)
    run_command("firewall-cmd --permanent --add-service=http --add-service=https", "Configuring firewall for HTTP/HTTPS...")
    run_command("firewall-cmd --reload", "Reloading firewall...")
    run_command("dnf install -y fail2ban", "Installing Fail2Ban...")
    run_command("systemctl enable --now fail2ban", "Enabling Fail2Ban...")

    print("\nVPS setup completed! Your Laravel application should now be available.")

if __name__ == "__main__":
    setup_vps()
