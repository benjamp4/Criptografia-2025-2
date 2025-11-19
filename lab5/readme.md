open -a Wireshark capture_c1.pcap capture_c2.pcap capture_c3.pcap capture_c4.pcap

**Ver solo SSH:**
```
ssh
```

**Ver Key Exchange Init:**
```
ssh.message_code == 20
```

**Ver Protocol Exchange:**
```
ssh.protocol