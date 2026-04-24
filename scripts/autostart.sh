#!/bin/bash
# scripts/autostart.sh
# Auto-start SignBridge on Raspberry Pi boot
# Run once: bash scripts/autostart.sh

echo "Setting up autostart..."

# Create autostart script
cat > /tmp/signbridge_start.sh << 'INNER'
#!/bin/bash
sleep 10
cd /home/khaled/sign_project
source bin/activate
python3 src/main.py >> /home/khaled/signbridge.log 2>&1
INNER

chmod +x /tmp/signbridge_start.sh
sudo mv /tmp/signbridge_start.sh /usr/local/bin/signbridge_start.sh

# Add to rc.local
if ! grep -q "signbridge" /etc/rc.local; then
    sudo sed -i 's/exit 0/\/usr\/local\/bin\/signbridge_start.sh \&\nexit 0/' /etc/rc.local
    echo "OK - Added to rc.local"
else
    echo "OK - Already in rc.local"
fi

echo ""
echo "=================================="
echo "  Autostart configured!"
echo "  SignBridge will start on boot"
echo "  Log: /home/khaled/signbridge.log"
echo "=================================="
