#!/bin/bash

# Prepare Android SDK for Buildozer

mkdir -p /home/runner/.buildozer/android/platform
rm -rf /home/runner/.buildozer/android/platform/android-sdk
ln -s /usr/local/lib/android/sdk /home/runner/.buildozer/android/platform/android-sdk

# Create tools/bin directory with compatibility
mkdir -p /home/runner/.buildozer/android/platform/android-sdk/tools/bin
cd /home/runner/.buildozer/android/platform/android-sdk/tools/bin

# Create sdkmanager wrapper
cat > sdkmanager << 'EOF2'
#!/bin/bash
cd /usr/local/lib/android/sdk/cmdline-tools/latest/bin
./sdkmanager --sdk_root=/home/runner/.buildozer/android/platform/android-sdk "$@"
EOF2
chmod +x sdkmanager

# Copy other tools if present
for tool in adb aidl dx d8; do
    if ls /usr/local/lib/android/sdk/build-tools/*/$tool 2>/dev/null; then
        cp /usr/local/lib/android/sdk/build-tools/*/$tool . 2>/dev/null || true
    fi
done

echo "SDK tools prepared"
ls -la /home/runner/.buildozer/android/platform/android-sdk/tools/bin/
